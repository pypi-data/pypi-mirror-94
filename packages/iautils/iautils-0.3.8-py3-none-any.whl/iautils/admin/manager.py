
import os, shutil
from datetime import datetime
from functools import partial
import numpy as np
import pandas as pd
import cv2
import dask.dataframe as dd
import h5py
from sqlalchemy_utils import database_exists, create_database
from tqdm.notebook import tqdm
from nptdms import TdmsFile

from .config import MDB, ROOT, HOST, MDB_TABLES, PROJECTDB_TABLES, PROJECT_SUBDIRS, EXTENSIONS, ASSETS
from .dbio import read_table, init_database, create_table, update_table, delete_rows
from ..common.utils import gen_project_db_dirs, get_project, project_parser, list_lots, list_subdirs, list_trees, list_files, count_extensions, infer_duplicates
from ..common.utils import load_rawdata, load_features, encode_labels, split_train_test
from ..audio import transforms as iat
from ..audio.utils import save_waveform, save_spectrogram, save_rms
from ..ml import others as imo


########################################################################################################################################
## CREATE NEW PROJECT
######################################################################################################################################## 

################################################################
## init_project
################################################################
def init_project(project, local_db_forced_init=False):
    '''
    신규 프로젝트 등록 시 1회 실행
    ROOT, SERVER, MOTHER는 iautils.mangeer 모듈에 전역으로 설정되어 있음
    (1) 신규 프로젝트의 정보를 사용자에게 입력 받음
    (2) 신규 프로젝트의 정보를 Mother Database에 업데이트
    (3) 신규 프로젝트의 Directory Strucutre 생성
    (4) 신규 프로젝트의 Local Database 초기화
    
    params
      project   등록할 프로젝트의 코드 (예: airpurifier, dishwasher)
      
    return
      sqlite database engine of project's database
    '''

    # project's directories
    DB, DIRS = gen_project_db_dirs(project)    
    
    ################
    # check mother database
    ################
    print('Check Mother Database:')    
    
    # create mother database
    if not database_exists(MDB.url):
        create_database(MDB.url)
        print(f"  - Mother Database Not Found, Create New Mother Database.")

    # create table 'projects' if not exist
    if not MDB.has_table('projects'):
        with MDB.connect() as conn:
            create_table(MDB, 'projects', MDB_TABLES['projects'], )
        print(f"  - Table 'project' Not Found, Create New Table 'project'.")
    
    # ask user if project is already exist in mother database
    if project in read_table(MDB, 'projects')['code'].tolist():
        re_init = None
        while re_init not in ['yes', 'no']:
            re_init = input(f"  - Project {project} is already initiated, re-initiate? (yes or no)").lower()
        if re_init=='yes':
            with MDB.connect() as conn:
                delete_rows(MDB, 'projects', {'code': project})
        else:
            print('\n  - [EXIT] Project is already initiated!')
    
    # message
    print(f"  - Mother Database is OK.")
    print('')
    
    ################
    # Manual Input Project Information
    ################
    print(f'Initialize Project {project}:')
    
    # user inputs
    chk = 'no'
    project_info = dict()
    while chk != 'yes':
        for field, attrs in MDB_TABLES['projects'].items():
            if field == 'code':
                project_info[field] = project
            elif 'form' in attrs.keys():
                v = input(f"  - {attrs['form']}:")
                if (field == 'opened') & (v == ''):
                    v = datetime.now().strftime('%Y-%m-%d')
                project_info[field] = v
        chk = input(f"  - Confirm All Inputs (yes or no):").lower()

    # auto-
    project_info['site_url'] = os.path.join(HOST, project)
    project_info['project_dir'] = os.path.join(ROOT, project)
    
    # linebreak
    print('')

    ################
    # create subdirs
    ################
    print(f'Create Directory Structure for {project}:')
    
    # create subdirs
    for d in [d for d in DIRS.values() if d not in ['root']]:
        if not os.path.exists(d):
            print(f"  - Directory '{d.replace(ROOT, '<ROOT>')}' is not exists, create new.")
            os.makedirs(d)
            os.chmod(d, 0o775)
        else:
            print(f"  - Directory '{d.replace(ROOT, '<ROOT>')}' is already exists.")
    
    # linebraek
    print('')
    
    ################
    # add write revisions_sample.csv
    ################
    print(f"Write 'revisions_sample.csv' into revisions directory.")
    
    # write revisions_sample.csv
    revisions_sample = get_revisions_sample()
    revisions_sample.to_csv(os.path.join(DIRS['revisions'], 'revisions_sample.csv'), index=False)
    print(f"  - Add 'revision_xxx.csv' when label revision is required.")
    
    # linebraek
    print('')

    ################
    # init project database
    ################
    init_database(DB, forced=local_db_forced_init)
    project_info['project_db'] = str(DB.url)

    ################
    # update mother database
    ################
    # append row
    print(f'Update Mother Database:')
    try:
        (
            pd.DataFrame.from_records([project_info])
            .to_sql('projects', MDB, if_exists='append', index=False)
        )
        print(f"  - Project {project} updated.")
    except Exception as ex:
        print(f"  - [ERROR] {ex}")
    print('')
        

########################################################################################################################################
## SUB-FUNCTIONS - SUBMIT, EXTRACTION, ...
########################################################################################################################################

################################################################
## get_revisions_sample
################################################################
def get_revisions_sample():
    revisions_sample = {
        'confirmed': '2020-12-01',
        'filename': 'super_noisy_cooktop_audio.tdms',
        'label': 'label_origin',
        'label_before': 'OK',
        'label_revised': 'NG_spark',
        'confirmer': 'Woojin Cho',
        'note': "When upload it to '<revisions>/revisions_xxx.csv', prefix 'revisions' must be kept."
    }
    revisions_sample = pd.DataFrame.from_records([revisions_sample])
    return revisions_sample
    
################################################################
## submit revisions
################################################################
def submit_revisions(project, revisions, csvname=None):
    '''
    label revisions를 upload하는 스크립트
    label revisions를 inventory에 반영하기 위해서는 revisions upload 후 update_inventory()를 실행해야 함
    '''
    if csvname is None:
        csvname = f"revisions_{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}.csv"
    else:
        if not csvname.startswith("revisions"):
            print("[EXIT] .csv name must start with 'revisions_'. Please re-try.")
            return
        if not csvname.endswith(".csv"):
            print("[EXIT] revisions should be a .csv. Please re-try.")
            return
        
    # get project
    project, DB, DIRS = project_parser(project)
    
    print("Submit label revisions:")
    csvpath = os.path.join(DIRS['revisions'], csvname)
    revisions.to_csv(csvpath, index=False)
    print(f"  - Done - '{csvpath}' saved.")
    print(f"  - NOTE! Execute 'update_inventory(project)' manually required after submit revisions.")
    
    # linebreak
    print("")
    
    # update revisions
    update_revisions(project)

    
################################################################
## update_revisions
################################################################
def update_revisions(project):
    '''
    Read revisions*.csv from revisions directory, and update table reivisions in project's database
    
    params
      DB
      directory   
    '''

    # get project
    project, DB, DIRS = project_parser(project)
    
    # current revisions
    revisions = read_table(DB, 'revisions')
    n_old = len(revisions)
    print(f"Update Revisions:")
    
    # read revisions.csv from disk
    files = [
        f.path for f in os.scandir(DIRS['revisions']) if f.name.startswith('revisions') and f.name.endswith('.csv') and "revisions_sample.csv" not in f.name
    ]
    # dask dataframe은 단순히 복수 개의 파일 read를 위해 사용됨
    if len(files) > 0:
        revisions_ = dd.read_csv(files).compute()
    else:
        print(f"  - [EXIT] No 'revisions*.csv' Found!")
        print('')
        return
    
    # append revisions
    revisions = pd.concat([revisions, revisions_])
    revisions = revisions.drop_duplicates(['filename'], keep='last')
    n_new = len(revisions)
    
    # update revisions
    revisions.to_sql('revisions', DB, if_exists='replace', index=False)
    print(f"  - [DONE] Table 'revisions' are updated. {n_new - n_old} revisions are added.")
    print('')


################################################################
## extract tdms
################################################################
def extract_tdms(project, translate=None, n_samples=None, chunk_size=None, forced=False, save=True, return_=False):
    '''
    extract tdms data
    
    params
      DB
      DIRS
      translate
      chunk_size
      forced
      return_
      
    return
      <pd.DataFrame> if return_ is True else void
    '''
    
    # init
    project, DB, DIRS = project_parser(project)
    
    # Start
    print("Extract Data:")
        
    # load inventory
    inventory = read_table(DB, 'inventory')
    history = read_table(DB, 'history')
        
    # translate
    if translate is None:
        translate={'': ''}
    
    # timestamp
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # select lots to update
    status = None if forced else 'modified'
    lots_to_update = list_lots(project, process='extract', status=status)
    
    # check lots_to_update
    if len(lots_to_update) == 0:
        print("  - [EXIT] Nothing to update. Data already extracted. Try 'forced=True'.")
        return
    
    # filter and chunk
    inventory_ = inventory.loc[inventory['status']!=0, :]
    indices = dict()
    if n_samples is not None:
        if n_samples > len(inventory_):
            print(f"  - [WARNING] n_samples {n_samples} is larger than population {len(inventory_)}. - n_smaples is changed to no. of data.")
            n_samples = len(inventory_)
        indices['sample'] = [inventory_.sample(n_samples).sort_index().index, ]
    else:
        for lot in lots_to_update:
            indices_ = inventory_.loc[inventory['lot'] == lot, :].index
            if (chunk_size is None) or (chunk_size < len(indices_)):
                indices[lot] = [indices_]
            else:
                indices[lot] = np.split(indices_, np.arange(chunk_size, len(indices_), chunk_size), )    
    
    # order of columns
    head_ = [c for c in ['split', 'lot', 'filepath', 'filename', 'label_origin'] if c in inventory_.columns]
    body_ = ['tsm', 'group', 'channel', 'y', 'sr', 'offset', 'duration', 'dt']
    
    # chunk by chunk
    for lot, chunked_indices in indices.items():
        print(f"  - Extracting LOT {lot}.")
        
        if save:
            # clean up
            old_files = [f.path for f in os.scandir(DIRS['extract']) if f"extracted_{lot}" in f.name]
            if len(old_files) > 0:
                print(f"  - Clean up {len(old_files)} old parquets before save.")
                for f in old_files:
                    os.remove(f)
            
        for i, indices_ in enumerate(chunked_indices):
            # chunked df placeholder -원천데이터 structure가 변할 수 있으므로, 속도가 느리지만 df.append를 사용함
            extracted = pd.DataFrame()
            for idx in tqdm(indices_):
                r = inventory.loc[idx, :]
                f = TdmsFile(r['filepath'])
                # 1 row per group, n channels per group
                for group in f.groups():
                    # row placeholder
                    row = {x: r[x] for x in head_}
                    # update group name
                    group_name = group.name
                    row['group'] = group_name
                    # update group properties
                    for group_property_key, group_property_value in group.properties.items():
                        group_property_name = group_property_key
                        if group_property_key in translate.keys():
                            group_property_name = translate[group_property_key]
                        row[group_property_name] = group_property_value
                    # update channel
                    for channel in group.channels():
                        # update channel name
                        channel_name = channel.name
                        if channel_name in translate.keys():
                            channel_name = translate[channel_name]
                        row[channel_name] = channel[:]
                        # update channel properties
                        for channel_property_key, channel_property_value in channel.properties.items():
                            channel_property_name = f"{channel_name}_{channel_property_key}"
                            if channel_property_name in translate.keys():
                                channel_property_name = translate[channel_property_name]
                            row[channel_property_name] = channel_property_value
                # append row
                extracted = extracted.append(
                    pd.DataFrame.from_records([row]),
                    ignore_index=True
                )
                
            #### 예약된 변수명에 대한 사전 처리 #### - 추후 별도 FORM으로 분리
            # sr = int(1/dt)
            if 'dt' in extracted.columns:
                extracted['sr'] = (1/extracted['dt']).astype(int)
            # duration
            if all([e in extracted.columns for e in ['y', 'sr']]):
                extracted['duration'] = extracted['y'].apply(len) / extracted['sr']
            
            # reorder
            ordered = head_ + [c for c in body_ if c in extracted.columns]
            extracted = extracted.loc[:, ordered + [c for c in extracted.columns if c not in ordered]]

            # save parquet
            if save:
                # generate seqeuntial name
                if len(chunked_indices) == 1:
                    savepath = os.path.join(DIRS['extract'], f"extracted_{lot}.parquet")
                elif 'tsm' in extracted.columns:
                    savepath = os.path.join(DIRS['extract'], f"extracted_{lot}_{row['tsm'].item().strftime('%Y-%m-%dT%H:%H:%S')}.parquet")
                else:
                    savepath = os.path.join(DIRS['extract'], f"extracted_{lot}_{str(i).zfill(3)}.parquet")
                # save parquet
                extracted.to_parquet(savepath, engine='pyarrow', )
                
        if save:
            # message
            print(f"  - Save extracted data from LOT {lot} - {i+1} parquets are saved.")
        
    # check parquet size and remove parquet
    if n_samples is not None:
        if save:
            estimated_size_gb = os.path.getsize(savepath)/1024/1024/1024 / n_samples * len(inventory_)
            required_memory_gb = extracted.memory_usage(index=True, deep=True).sum()/1024/1024 / n_samples * len(inventory_)
            n_rows_per_parquet = int(len(inventory_)/estimated_size_gb)
            if required_memory_gb > 10:
                print(f'  - Partitioning with chunk_size {n_rows_per_parquet} is recommended - 1 GB per a parquet.')
            else:
                print(f'  - Partitioning is not recommended - a {estimated_size_gb:.1f} GB parquet will be saved.')
            print(f'  - If you load all dataset at once {required_memory_gb:.1f} GB memory will be used.')
            os.remove(savepath)
            
    # remain saved parquet and update history
    else:
        # update history
        history_ = pd.DataFrame({
            'lot': lots_to_update,
            'extracted': TIME,
            'translate': ', '.join([f"{k}: {v}" for k, v in translate.items()]),
        })
        update_table(DB, 'history', history_, key='lot')
        print(f"  - Project history updated. (extracted datetime updated)")
        
    if return_:
        if chunk_size is not None:
            print(f"  - [NOTE] It returns last chunk only.")
        print(f'')
        return extracted

    # line break
    print('')
    

########################################################################################################################################
## DATA IMPORT PROCESS
########################################################################################################################################

################################################################
## 1. explore origin
################################################################
def explore_origin(project, lots=None):
    '''
    explore origin directory (upload directory), and print list of lots
    '''
    
    project, DB, DIRS = project_parser(project)
    history = read_table(DB, 'history')    
    print(f"Explore '{project}' Origin:")
    
    if lots is not None:
        lots = lots if type(lots) is list else [lots]
        print(f"  - Explore lot {', '.join(lots)} only ")
    else:
        lots = list_subdirs(DIRS['origin'])
        print(f"  - {len(lots)} lots are uploaded: {lots}")
   
    lots = {lot: os.path.join(DIRS['origin'], lot) for lot in lots}
    print('')
    
    lots_inventoried = list_lots(DB, 'inventory', 'complete')
    
    for lot, d in lots.items():
        extension_counts = count_extensions(d)
        exts = [ext for ext in extension_counts.index if ext in ('tdms', 'wav', 'png', 'jpg', 'gif', 'bmp')]
        trees = list_trees(d, exts)
        print(f"Lot {lot}:")
        print(f"  - {'Already' if lot in lots_inventoried else 'Noy yet'} inventoried.")
        print(f"  - Extensions are {', '.join([f'{extension_counts[k]} {k}' for k in extension_counts.index])}")
        print(f"  - Subdirs are, ")
        for tree in trees:
            print(f"    . {tree.replace(str(d), '').strip('/')}")
        
        # lot end line break
        print('')

        
################################################################
## 2. make table of files in lot
################################################################
def load_lot(project, lot=None, hrchy='label_origin', exts='all', invalid_duplicates=True, return_dup_flags=False):
    '''
    data lot 단위 update를 강제하는 이유는 각 lot의 폴더 구조가 불일치하는 경우가 많기 때문이다. - 특히 label 추가/세분화
    
    params
      directory (or DIRS)   origin directory
      lot                   lot name (name of subdir in origin)
      hrchy                 hierarchy of subdirs (field 명으로 사용됨)
      exts                  list of file extensions to include
    
    return
      <pd.DataFrame>        table of files in given lot
    '''    
    
    ################
    ## INIT
    ################
    project, DB, DIRS = project_parser(project)
    
    # print lots if lot is None
    subdirs = list_subdirs(DIRS['origin'])
    if lot not in subdirs:
        print(f"[EXIT] {lot} not in '{project}'s origin! You have {sorted(subdirs)}")
        return
    
    # start message
    print('Make list of files in given LOT directory:')
    
    # lot directory
    LOT_DIR = os.path.join(DIRS['origin'], lot)
    
    # get timestamp
    ADDED = datetime.fromtimestamp(os.path.getmtime(LOT_DIR)).strftime('%Y-%m-%d %H:%M:%S')
    MODIFIED = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # extensions to serach
    if exts in EXTENSIONS.keys():
        exts = EXTENSIONS[exts]
    if type(exts) is not list:
        exts = [exts]
    
    # check hierarchy
    if type(hrchy) is not list:
        hrchy = hrchy.strip('/').split('/')
    if 'label' in hrchy:
        hrchy = ['label_origin' if e == 'label' else e for e in hrchy]
        print(f"  - [WARNING] You cannot use field name 'label'. It will be renamed 'label_origin'.")   
          
    ################
    ## search 
    ################
    files = list_files(LOT_DIR, exts=exts, posix=True)

    # make labels
    # None fields는 단지 field 순서 맞추려는 목적임
    filepaths = pd.DataFrame({
        'lot': lot,
        'originpath': [str(f) for f in files],
        'filepath': None,
        'filename': [f.name for f in files],
        'status': 1,
        'log': None,
        'added': ADDED,
        'modified': MODIFIED,
        'note': None,
    })
    
    ################
    ## check duplicated data
    ################
    # check duplicated and add flag column
    n_dups = 0
    dup_flags = infer_duplicates(filepaths['filename'])
    if dup_flags is not None:
        for idx in dup_flags.loc[dup_flags['is_copied'], :].index:
            filepaths.at[idx, 'log'] = 'augmented'
            if invalid_duplicates:
                filepaths.at[idx, 'status'] = 0 
            filepaths.at[idx, 'modified'] = MODIFIED
            n_dups += 1
        
        if return_dup_flags:
            return dup_flags
    
    ################
    ## make table
    ################
    # set field names
    fields = pd.DataFrame({'field': [str(f).replace(LOT_DIR, '').strip('/') for f in files]})
    fields = fields['field'].str.split('/', expand=True).iloc[:, :len(hrchy)]
    fields.columns = hrchy
    tbl = pd.concat([filepaths, fields], axis=1)
    
    # all label_origin will be 'unlabeled' if labels are not given
    if not any([x for x in tbl.columns if 'label_origin' in x]):
        tbl['label_origin'] = 'unlabeled'

    ################
    ## split train test
    ################
    tbl_valid = tbl.loc[tbl['status']!=0, :]
    tbl_invalid = tbl.loc[tbl['status']==0, :]
    tbl_valid = split_train_test(tbl_valid, by='label_origin', )
    tbl = pd.concat([tbl_valid, tbl_invalid], axis=0).sort_index()
    
    ################
    ## print results
    ################
    if invalid_duplicates:
        print(f"  - {n_dups} duplicates are found - status of duplicates are marked as 0.")
    else:
        print(f"  - {n_dups} duplicates are found - but status are remained 1 (invalid_duplicates={str(invalid_duplicates)})")
    tbl_valid = tbl[tbl['status'] == 1]
    for h in hrchy:
        cnt = tbl_valid[h].value_counts()
        if len(cnt.index) < 5:
            print(f"  - Field '{h}' has {len(cnt)} factors: {', '.join([f'{cnt[k]} {k}' for k in cnt.index])}")
        else:
            print(f"  - Field '{h}' has {len(cnt)} factors:")
            for idx in cnt.index:
                print(f"    . {idx}: {cnt[idx]} files")
    print(f"  - [DONE] {len(tbl)} files are found, {len(tbl_valid)} are valid and tabled.")
    
    # line break
    print('')
    
    return tbl


################################################################
## 3. update inventory
################################################################
def update_inventory(project, tbl=None, if_exists='skip', verbose=True, return_=False):
    '''
    새 데이터를 inventory에 추가하거나, revised label을 반영함
    
    params
      DB         sqlalchemy engine of local database
      tbl        table of files in lot (to insert into inventory)
      if_exists  'skip' or 'replace' when data is already in inventory
      verbose
      return_
      
    return
      <pd.DataFrame>   return updated inventory as dataframe if return_ is True
    '''
    
    #### init
    project, DB, DIRS = project_parser(project)
    
    # update revisions
    update_revisions(DB)
    
    # get tables
    inventory = read_table(DB, 'inventory')
    history = read_table(DB, 'history')
    revisions = read_table(DB, 'revisions')
        
    # 이미 inventory에 입고된 데이터가 재입력 되었을 때 - default 'skip'
    map_if_exists = {'skip': 'first', 'replace': 'last', 'overwrite': 'last'}
    if if_exists not in map_if_exists.keys():
        print(f"[EXIT] option 'if_exists' {if_exists} not in {[i for i in map_if_exists.keys()]}")
        return
    agg_option = map_if_exists[if_exists]
    
    # timestamp
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    ################################
    ## Update Inventory
    ################################
    # 1-1. 새 데이터 입력되었을 때 - 데이터 추가
    if tbl is not None:
        print(f"Add Data to Project Inventory:")
        
        # 집계
        n_old, n_old_valid = len(inventory), len(inventory[inventory['status'] != 0])
        n_add, n_add_valid = len(tbl), len(tbl[tbl['status'] != 0])
        
        # Add inventoried timestamp into new table
        tbl['inventoried'] = TIME
        
        # Concatenate
        inventory = pd.concat([inventory, tbl], axis=0).reset_index(drop=True)
    
        # 1-1. 이미 있는 데이터 추가된 경우 처리 - originpath 기준 
        drop_indices_origin = inventory.duplicated(['originpath'], keep=agg_option)
        inventory = inventory[~drop_indices_origin]
        
        # 1-2. 추가된 data와 기존 data 중복되는 것 확인 - filename 기준, 중복되는 것은 삭제하지 않고 status만 0으로 변경
        n_repeat = 0
        drop_indices = inventory.duplicated(['filename'], keep='first')
        drop_indices = inventory[drop_indices].index
        for i in drop_indices:
            if inventory.at[i, 'status'] != 0:
                inventory.at[i, 'status'] = 0
                inventory.at[i, 'log'] = 'duplicated'
                inventory.at[i, 'modified'] = TIME
                n_repeat += 1
        
        # 최종 집계
        n_new, n_new_valid = len(inventory), len(inventory[inventory['status'] != 0])
        
        # 데이터 추가 결과 출력
        rj = len(str(n_new))
        print(f"  - ( Now) {str(n_old_valid).rjust(rj)} valid / {str(n_old).rjust(rj)} total data")
        print(f"  - ( Add) {str(n_add_valid).rjust(rj)} valid / {str(n_add).rjust(rj)} total data")
        if drop_indices_origin.sum() > 0:
            print(f"           {str(drop_indices_origin.sum()).rjust(rj)} data already updated - {if_exists} all.")
        if n_repeat > 0:
            print(f"           {str(n_repeat).rjust(rj)} data is repeated - set status 0")
        print(f"  - [DONE] {str(n_new_valid).ljust(rj)} valid / {str(n_new).rjust(rj)} total data")
        
        # add data line break
        print('')
    
    # 2. inventory w/ valid data only
    inventory_ = inventory[inventory['status'] != 0]
    
    # 3. Label 교정
    print("Revise Labels:")
    if len(revisions) > 0:
        n_already_revised = 0
        n_revised = 0
        for i in revisions.index:
            fname = revisions.at[i, 'filename']       # filename to revise
            lname = revisions.at[i, 'label']          # label name to revise
            lnew = revisions.at[i, 'label_revised']   # new label
            j = inventory_[inventory_['filename'] == fname].index
            if len(j) > 0:
                j = j[0]
                if inventory.at[j, lname] != lnew:
                    inventory.at[j, lname] = lnew
                    inventory.at[j, 'status'] = 2
                    inventory.at[j, 'log'] = 'revised'
                    inventory.at[j, 'modified'] = TIME
                    n_revised += 1
                else:
                    n_already_revised += 1
        # message
        print(f"  - {len(revisions)} revisions ordered, {n_already_revised} already revised.")
        print(f"  - [DONE] {n_revised} labels are newly revised.")
    else:
        print(f"  - [DONE] No revisions exist.")
        
    # revisions line break
    print('')
                
    # update inventory - rewrite!
    #   - DB에 insert하고 중복을 처리하지 않고, DB의 inventory를 통째로 rewrite함
    #   - 새로운 LOT에 신규 fields가 추가되어 있을 수 있기 때문에 append 할 수 없음 (RDB 사용)
    print(f"Update Project Inventory:")
    inventory.to_sql('inventory', DB, if_exists='replace', index=False)
    print(f"  - [DONE] Inventory Updated.")
    
    # update inventory line break
    print('')
    
    
    ################################
    ## Update History
    ################################
    print(f"Update Project History:")
    history_ = (
        inventory
        .groupby(['lot', 'status'])['originpath'].count().reset_index()
        .pivot(index='lot', columns='status', values='originpath').fillna(0)
        .assign(
            n_origin = lambda x: x.loc[:, [c for c in x.columns if c in [0, 1, 2]]].sum(axis=1).astype(int),
            n_valid = lambda x: x.loc[:, [c for c in x.columns if c in [1, 2]]].sum(axis=1).astype(int),
            n_invalid = lambda x: x.loc[:, 0].astype(int) if 0 in x.columns else 0,
            n_revised = lambda x: x.loc[:, 2].astype(int) if 2 in x.columns else 0
        )
        .filter(['n_origin', 'n_valid', 'n_invalid', 'n_revised'])
    )

    # add stamps
    stamps = {
        'added': True,           # True: oldest stamp remains
        'inventoried': True,     # True: oldest stamp remains,
        'modified': False,       # False: latest stamp remains
    }
    
    for lot in history_.index:
        # add history stamp
        for field, ascending in stamps.items():
            stamp = inventory.loc[inventory['lot']==lot, field].sort_values(ascending=ascending).iat[0]
            if type(stamp) is not str:
                stamp = str(stamp)
            history_.at[lot, field] = stamp
        # add extensions - 유효한 파일 'inventory_'에 대해서만
        extensions = set([x.rsplit('.')[-1] for x in inventory_.loc[inventory_['lot']==lot, 'filename']])
        history_.at[lot, 'extensions'] = ', '.join(sorted(extensions))        

    # null 값 overwrite 되지 않도록 drop, update_table이 key를 column에서 받아가야 함으로 reset_index()
    history_ = history_.dropna(axis=1)
    history_ = history_.reset_index()

    # update history in database
    update_table(DB, 'history', history_, key='lot')
    print(f"  - [DONE] history updated.")
    
    # update history line break
    print(' ')
    
    if return_:
        return inventory

    
################################################################
## 4. update dataset
################################################################    
def update_dataset(project, hrchy='split/label_origin', forced=False):
    '''
    dataset 폴더(학습용)에 hardlink를 생성함
    symlink 생성에는 시간이 적게 소요됨으로 inventory의 모든 lot들을 일괄 처리함
    
    params
      DB
      DIRS
      hrchy   subdirs의 구조 (예: hrchy='label_origin'이면 ./NG ./OK subdirs 생성됨)
      forced  모든 dataset 강제로 갱신
      
    return
      (void)
    '''
    #### init
    project, DB, DIRS = project_parser(project)
    
    print(f"Update Project Dataset:")
    
    # read inventory, history
    inventory = read_table(DB, 'inventory')
    history = read_table(DB, 'history')
    
    # timestamp
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # FORCED - remove all dataset
    if forced:
        print(f"  - Remove all current links.")
        inventory['filepath'] = None
        current_files = os.scandir(DIRS['dataset'])
        for f in current_files:
            if f.is_dir():
                shutil.rmtree(f)
            else:
                os.remove(f)
        
    # subdirectory structure
    if type(hrchy) is not list:
        hrchy = hrchy.strip('/').split('/')
        
    print(f"  - Subdirs will be dataset/{'/'.join([h for h in hrchy])}")

    # init counter & subdirs
    N = {'created': 0,
         'moved': 0,
         'exists': 0,
         'missing': 0, 
         'removed': 0, }
    
    # create symlink
    subdirs = set()
    for idx in inventory.index:
        
        # select row
        r = inventory.loc[idx, :]
        is_valid = r.status != 0
        
        # link valied files
        if is_valid:
            # create path (makedir if dir not exist)
            dst = DIRS['dataset']
            for h in hrchy:
                dst = os.path.join(dst, inventory.at[idx, h])
            subdirs.update([dst])
            if is_valid and not os.path.exists(dst):
                os.makedirs(dst, 0o775)
            dst = os.path.join(dst, r.filename)
        
            # create or move links
            if r.filepath is None:
                if not os.path.exists(dst):
                    os.link(r.originpath, dst, )
                    N['created'] += 1
                else:
                    # debug 시 편의를 위해서 else 조건 추가되었음, (실제로는 error 조건)
                    N['exists'] += 1
            else:
                if not os.path.exists(r.filepath):
                    if r.status != 0:
                        os.link(r.originpath, dst)
                        N['created'] += 1; N['missing'] += 1
                else:
                    if dst != r.filepath:
                        shutil.move(r.filepath, dst)
                        N['moved'] += 1
                    else: 
                        N['exists'] += 1
            
        # unlink invalid files
        else:
            if r.filepath is not None:
                if os.path.exists(r.filepath):
                    os.remove(r.filepath)
                    N['removed'] += 1
            
        # update links in inventory
        inventory.at[idx, 'filepath'] = dst if is_valid else None
        
    # print results
    print(f"  - Project dataset updated. ({len(inventory.loc[inventory['status']!=0,: ])} valid / {len(inventory)} total)")
    rj = len(str(max(N.values())))
    for k, v in N.items():
        if v != 0:
            print(f"    . {str(v).rjust(rj)} {k if k != 'exists' else 'already exists'}")
    
    # update inventory
    # row by row UPDATE SET 하면 너무 느림 (sqlite connection 때문에) ~ 따라서 한 번에 overwrite
    inventory.to_sql('inventory', DB, if_exists='replace', index=False)
    print(f"  - Project inventory updated. (filepaths updated)")
  
    # update history
    history_ = pd.DataFrame({
        'lot': sorted(inventory['lot'].unique()),
        'copied': TIME
    })
    update_table(DB, 'history', history_, key='lot')
    print(f"  - Project history updated. (copied datetime updated)")
      
    # update label.csv
    cols = [c for c in inventory.columns if c not in ['originpath', 'status', 'log', 'added', 'modified']]
    allcsv = inventory.loc[~inventory['filepath'].isna(), cols]
    allcsv.to_csv(os.path.join(DIRS['dataset'], 'all.csv'), index=False)
    for split in ['train', 'test']:
        allcsv.loc[allcsv['split']==split, :].to_csv(os.path.join(DIRS['dataset'], f'{split}.csv'), index=False)
    print(f"  - dataset/all.csv, train.csv and test.csv is updated.")
    
    # line break
    print('')
    

################################################################
## 5. explore tdms
################################################################
def explore_tdms(project, translate=None, n_samples=1000, check_size=True):
    '''
    sample check before extraction - fields 확인, parquet partitioning 검토
    
    params
      DB
      DIRS
      translate   dict(current field name: new field name)
      n_samples
      check_size
      
    return
      <pd.DataFrame>
    '''
    
    return extract_tdms(project, translate=translate, n_samples=n_samples, chunk_size=None, forced=True, return_=True, save=check_size)


################################################################
## 6. update_rawdata
################################################################
def update_rawdata(project, translate=None, chunk_size=None, forced=False, save=True):
    extract_tdms(
        project=project, translate=translate, chunk_size=chunk_size, forced=forced, save=save,
    )
    
    
################################################################
## 6-2. update_metadata ~ when data is just jpg, png, wav, ...
################################################################
def update_metadata(project, forced=False):
    
    # init
    DB, DIRS = get_project(project)
    
    print(f"Extract Meta from Data:")
    
    # select lots to update
    inventory = read_table(DB, 'inventory')
    status = None if forced else 'modified'
    lots_to_update = list_lots(project, process='extract', status=status)
    
    # check lots_to_update
    if len(lots_to_update) == 0:
        print("  - [EXIT] Nothing to update. Data already extracted. Try 'forced=True'.")
        return
    
    # filter lots
    inventory = inventory.loc[inventory['lot'].isin(lots_to_update), :]
    
    # meta directly from inventory
    base_fields = ['split', 'lot', 'filepath', 'filename', 'label_origin']
    metadata = inventory.loc[inventory['status']!=0, base_fields].copy()
    
    # timestamp
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # test 1 files - is image or audio
    test_fp = metadata.at[0, 'filepath']
    if test_fp.rsplit('.', 1)[-1] in EXTENSIONS['image']:
        project_type = 'image'
    else:
        project_type = None   # audio project 아직 작성 안 됨 - 쓸 일이 없음
    print(f"  - The project type is '{project_type}' - extract {project_type }'s meta.")
    
    ################################
    # IMAGE META EXTRACTION
    ################################
    if project_type in ['image']:
        
        # define image's meta data
        image_fields = ['format', 'height', 'width', 'channels', 'depth', 'brightness', 'black', 'white', 'histogram']
        metadata[image_fields] = None

        # extract meta
        for idx in tqdm(metadata.index):
            fp = metadata.at[idx, 'filepath']
            img = cv2.imread(fp)

            # Extensions
            metadata.at[idx, 'format'] = fp.rsplit('.', 1)[-1]

            # H x W x C - remain None if Image's ndim is not 3
            if img.ndim == 2:
                img = np.expand_dims(img, -1)

            metadata.loc[idx, ['height', 'width', 'channels']] = img.shape

            # depth
            depth = int(
                str(img.dtype).replace('uint', '').replace('int', '').replace('float', '')
            )
            depth = 10 if depth == 16 else depth
            metadata.at[idx, 'depth'] = f"{depth}-bit"

            # brightness - center of gravity / depth
            metadata.at[idx, 'brightness'] = img.mean()/(2**depth - 1)

            # share of black
            flat = img.min(axis=-1).flatten()
            metadata.at[idx, 'black'] = flat[flat==0].shape[0] / flat.shape[0]

            # share of white
            flat = img.max(axis=-1).flatten()
            metadata.at[idx, 'white'] = flat[flat==(2**depth - 1)].shape[0] / flat.shape[0]

            # histogram - as 8-bit histogram
            flat = img.mean(axis=-1).flatten()
            metadata.at[idx, 'histogram'], _ = np.histogram(flat, np.linspace(0, 2**depth, 2**8))
    
    ################################
    # write parquet
    ################################
    
    # save parquet
    for lot in lots_to_update:
        metadata_lot = metadata.loc[metadata['lot']==lot, :]
        savepath = os.path.join(DIRS['extract'], f"meta_{lot}.parquet")
        save = 'yes'
        if os.path.exists(savepath):    
            save = ''
            while save not in ['yes', 'no']:
                save = input(f"  - '{savepath}' exists, overwrite? (yes or no)")
            if save == 'yes':
                os.remove(savepath)
        if save == 'yes':
            metadata_lot.to_parquet(savepath, engine='pyarrow', )
            print(f"  - Meta data of LOT {lot} is saved.")
        else:
            print(f"  - Meta data of LOT {lot} is already exists and not saved.")

    # update history
    history_ = pd.DataFrame({
        'lot': lots_to_update,
        'extracted': TIME,
    })
    update_table(DB, 'history', history_, key='lot')
    print(f"  - Project history updated. (extracted datetime updated)")
    
    # line break
    print('')
    
    
    
################################################################
## 7. update_features
################################################################
def update_features(project, savepath=None, specs=None):
    '''
    update features - octave band pressure, stft, mel, and save hdf5
    
    params
      project    proejct code (e.g. airpurifier, dishwasher)
      savepath   default os.path.join(DIRS['extract'], features.hdf5) if savepath in None
      specs      default will be used if specs is None
    '''
    
    project, DB, DIRS = project_parser(project)
    
    ################################################################
    # load extracted data
    ################################################################
    
    # load history, extracted (rawdata)
    history = read_table(DB, 'history')
    extracted = load_rawdata(project, )
    
    # timestamp
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #start
    print(f"Extract Audio Features:")
    
    # check consistency - length
    y_lengths = np.array([len(y) for y in extracted['y']])
    chk = sorted(set(y_lengths))
    if len(chk) > 1:
        cnts, edges = np.histogram(y_lengths, bins=3)
        N = np.array(chk).min()
        print(f"  - PCM length not fixed - PCMs are sliced into the shortest length, {N}")
        for i, cnt in enumerate(cnts):
            print(f"    . Length {edges[i]:.0f} ~ {edges[i+1]:.0f}: {cnt} files")
        extracted['y'] = [x[:N] for x in extracted['y']]
    
    # check consistency - sampling rate
    chk = sorted({x for x in extracted['sr']})
    if len(chk) > 1:
        print(f"  - [EXIT] All sampling rates should be same!")
        return
    
    # set sr
    sr = chk[0]
        
    ################################################################
    # set specs & load hdf5
    ################################################################
    # specs
    if specs is None:
        specs = {'height': 224, 'hop_sec': 0.01, 'fft_sec': 0.08, 'unit': 'amplitude', }
        
    # load or crate hdf5
    src = os.path.join(DIRS['extract'], 'features.hdf5') if savepath is None else savepath
        
    if os.path.exists(src):
        with h5py.File(src, 'r') as f:
            try:
                n_hdf5 = f['filename'].shape[0]
            except:
                n_hdf5 = 0
        n_extracted = len(extracted)
        loop, loop_max, forced = 0, 5, 'nothing'
        while forced not in ['yes', 'no'] and loop < loop_max:
            loop += 1
            forced = input(f"  - HDF5 exists w/ {n_hdf5} data vs. currently {n_extracted} data ready - remove HDF5 and retry? (yes or no)").lower()
        if forced in ['yes']:
            os.remove(src)
        else:
            print(f"  - EXIT!")
            return
    f = h5py.File(src, 'a')
    
    # set hdf5 attribute
    for k, v in specs.items():
        f.attrs[k] = v

    ################################################################
    # 1st extraction
    ################################################################
    print(f"  - Start 1st feature extraction.")
    
    ################################
    # set feature transforms
    ################################
    get_features = iat.RecipeGeneral(sr, specs)
     
    ################################
    # create dataset
    ################################    
    # estimated from shape of first output
    N = len(extracted)
    y, sr = extracted.at[0, 'y'], extracted.at[0, 'sr']
    features = get_features(y)
    
    # set X holders
    X_holders = {
        k: {
            'dtype': v.dtype,
            'shape': (N, ) + v.shape, 
            'maxshape': (None, ) + v.shape,
        } for k, v in features.items()
    }
    
    # set Y holders (filename, labels)
    Y_holders = {
        # filename
        'filename': {
            'dtype': h5py.string_dtype(),
            'shape': (N, ),
            'maxshape': (None, )
        },
        # encoded label
        'Y': {
            'dtype': np.int,
            'shape': (N, ),
            'maxshape': (None, )
        },
        # encoded test flag
        'test': {
            'dtype': np.int,
            'shape': (N, ),
            'maxshape': (None, )
        }        
    }
    
    # groups for features
    for name, kwargs in X_holders.items():
        f.require_dataset(name, **kwargs)
        
    # groups for Ys
    for name, kwargs in Y_holders.items():
        f.require_dataset(name, **kwargs)
    
    ################################
    # extract
    ################################
    
    #### dataset in Y_holders
    # filename
    f['filename'][:] = np.array(extracted.loc[:, 'filename'])
    
    # Y (encoded labels)
    Y, encoder, decoder = encode_labels(extracted.loc[:, 'label_origin'], verbose=False)
    Y = np.array(Y)
    f['Y'][:] = Y
    f['Y'].attrs['decoder'] = str(decoder)
    
    # test (encoded test flag)
    encoder = {'train': 0, 'test': 1}
    decoder = {v: k for k, v in encoder.items()}
    test = [encoder[s] for s in extracted['split']]
    f['test'][:] = np.array(test)
    f['test'].attrs['decoder'] = str(decoder)
    
    # features (1/2)
    for idx in tqdm(extracted.index):
        y, sr = extracted.at[idx, 'y'], extracted.at[idx, 'sr']
        features = get_features(y)
        for feature, value in features.items():
            f[feature][idx] = value
    
    # set attribute
    print(f"  - Write specifications into dataset attribute.")
    for feature in X_holders.keys():
        specs_ = {'sr': sr}
        if feature in ['rms']:
            specs_.update({k: v for k, v in specs.items() if k in ['sr', 'hop_sec', 'fft_sec']})
        elif feature in ['stft', 'mel']:
            specs_.update(specs)
        for spec, value in specs_.items():
            f[feature].attrs[spec] = value
    
    ################################################################
    # 2nd extraction - 1st extraction의 통계량을 바탕으로 계산되는 features
    ################################################################
    print(f"  - Start 2nd feature extraction.")
    
    ################################
    # set feature transforms
    ################################
    get_obf = iat.OctaveBandLevel(sr)
    get_stft = iat.STFT(sr, **specs)
    get_mel = iat.MelSpectrogram(sr, **specs)
    
    ################################
    # create dataset
    ################################
    # estimated from shape of prev. features
    features2 ={
        'obps': 'obp',
        'zstft': 'stft',
        'zmel': 'mel',
    }
    
    # set X2 holders
    X2_holders = {
        k: {
            'shape': f[v].shape, 
            'dtype': f[v].dtype,
            'maxshape': f[v].maxshape,
        } for k, v in features2.items()
    }
    
    # create dataset
    for name, kwargs in X2_holders.items():
        f.require_dataset(name, **kwargs)
        
    ################################
    # get statistics from previous extraction
    ################################    
    # SSR - steady-state range
    print(f"    . Estimate steady state range...", end=" ")
    bkpts, states, steady = imo.estimate_changepoints(f['rms'][:][Y==0], verbose=False)
    SSR = np.repeat(False, f['pcm'].shape[1])
    if steady == 0:
        ssr_start_sec = 0
        ssr_end_sec = bkpts[steady] * specs['hop_sec']
        SSR[:int(ssr_end_sec * sr)] = True
    else:
        ssr_start_sec = bkpts[steady-1] * specs['hop_sec']
        ssr_end_sec = bkpts[steady] * specs['hop_sec']
        SSR[int(ssr_start_sec * sr):int(ssr_end_sec * sr)] = True
    print(f"Done! SSR {ssr_start_sec:.1f} ~ {ssr_end_sec:.1f} sec.")
    
    # stft mean, std
    print(f"    . Calcuate STFT's spectral mean and std within SSR...", end=" ")
    stft_m = f['stft'][:][Y==0][:, :, states==steady].mean(axis=(0, 2)).reshape(-1, 1)
    stft_a = f['stft'][:][Y==0][:, :, states==steady].std(axis=(0, 2)).reshape(-1, 1)
    print(f"Done!")
    
    # mel mean, std
    print(f"    . Calcuate MelSpec's spectral mean and std within SSR...", end=" ")
    mel_m = f['mel'][:][Y==0][:, :, states==steady].mean(axis=(0, 2)).reshape(-1, 1)
    mel_a = f['mel'][:][Y==0][:, :, states==steady].std(axis=(0, 2)).reshape(-1, 1)
    print(f"Done!")
    
    ################################
    # extract
    ################################
    
    #### features (2/2)
    X = f['pcm'][:]
    for idx, x in enumerate(tqdm(X)):
        f['obps'][idx] = get_obf(x[SSR])
        f['zstft'][idx] = (get_stft(x) - stft_m) / stft_a
        f['zmel'][idx] = (get_mel(x) - mel_m) / mel_a
    
    #### set attribute
    print(f"  - Write specifications into dataset attribute.")
    
    # 이전 feature로부터 attributes 상속
    for feat2, feat1 in features2.items():
        for attr in f[feat1].attrs.keys():
            f[feat2].attrs[attr]= f[feat1].attrs[attr]
    
    # 새 feature에 추가되는 attribute
    f['obp'].attrs['freqs'] = get_obf.freqs
    f['obps'].attrs['freqs'] = get_obf.freqs
    f['zstft'].attrs['mean'] = stft_m
    f['zstft'].attrs['std'] = stft_a
    f['zmel'].attrs['mean'] = mel_m
    f['zmel'].attrs['std'] = mel_a   
    
    #### supplemnet dataset - ssr, states, steady
    f.create_dataset('ssr', data=SSR)
    f.create_dataset('states', data=states)
        
    #### set attributes
    f['states'].attrs['bkpts'] = np.array(bkpts)
    f['states'].attrs['steady'] = np.array(steady)
    
    # close
    f.close()
    print(f"  - [DONE] Features are saved as hdf5 format: '{src}'")
    
    ################################################################
    # udatate history
    ################################################################
    history_ = pd.DataFrame({
        'lot': sorted(extracted['lot'].unique()),
        'featured': TIME,
    })
    update_table(DB, 'history', history_, key='lot')
    print(f"  - Project history updated. (featured datetime updated)")
    
    
################################################################
## 8. update_assets
################################################################
def update_assets(project):
    '''
    update assets (save .wav, .png)
    '''
    
    project, DB, DIRS = project_parser(project)
    
    # start
    print(f"Prepare Assets for '{project}':")
    
    # history & timestamp
    history = read_table(DB, 'history')
    TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    ################################
    # Prep features
    ################################
    print(f"  - Get project features...", end=" ")
    # load featres
    features = load_features(project, verbose=False)
    
    #### load data
    # encoded label
    Y = features['Y'][:]
    
    # label
    if 'decoder' in features['Y'].attrs.keys():
        decoder = eval(features['Y'].attrs['decoder'])
        Labels = np.array([decoder[y] for y in Y])
    else:
        Labels = Y
        
    # test flag
    if 'decoder' in features['test'].attrs.keys():
        decoder = eval(features['test'].attrs['decoder'])
        Tests = np.array([decoder[s] for s in features['test'][:]])
    else:
        Tests = 'no_split'

    # filenames
    Files = np.array(
        [f.decode('utf-8') for f in features['filename'][:]]
    )

    # states
    States = features['states'][:]
    steady = features['states'].attrs['steady']

    print("Done!")

    # assets.csv placeholder
    list_assets = pd.DataFrame({
        'split': Tests,
        'filename': Files,
        'label_origin': Labels,
    })
    
    # unit_converter 
    def unit_converter(x, scale, unit):
        if scale in ['log']:
            if unit in ['amplitude', 'amp']:
                x = 20*np.log10(x)
            elif unit in ['power']:
                x = 10*np.log10(x)
        return x
    
    ################################
    # Set graph params
    ################################
    print(f"  - Prepare plotting parameters...", end=" ")
    PARAMS = dict()
    for asset, specs in ASSETS.items():
        PARAMS[asset] = dict()
        # set colormap
        if 'colormap' in specs.keys() and specs['colormap'] is not None:
            if specs['type'] in ['spectrogram']:
                PARAMS[asset]['cmap'] = specs['colormap']
        # set cutoff min, max
        if 'cutoff_percentile' in specs.keys() and specs['cutoff_percentile'] is not None:        
            # Spectrogram
            if specs['type'] in ['spectrogram']:
                # load S
                S = features[asset][:][Y==0][:, :, States==steady]
                # convert unit to dB
                scale = specs['scale']
                unit = features[asset].attrs['unit']
                S = unit_converter(S, scale, unit)
                # set cutoffs
                lim = np.percentile(S, specs['cutoff_percentile'])
                PARAMS[asset]['vmin'] = lim[0] if asset not in ['zstft', 'zmel'] else -lim[1]
                PARAMS[asset]['vmax'] = lim[1]
            # RMS
            elif specs['type'] in ['rms']:
                # set cutoffs
                lim = np.percentile(features[asset][:][Y==0][:, States==steady], specs['cutoff_percentile'])
                PARAMS[asset]['ylim'] = tuple(lim)
                PARAMS[asset]['States'] = States
                PARAMS[asset]['steady'] = steady
    print("Done!")

    ################################
    # Create
    ################################
    print(f"  - Create subdirs...", end=" ")
    # craete dirs if not exists
    for asset in ASSETS.keys():
        subdir = os.path.join(DIRS['assets'], asset)
        if not os.path.exists(subdir):
            os.makedirs(subdir, 0o775)
    print("Done!")
    
    ################################
    # Prep features
    ################################
    print(f"  - Start saving assets... ")
    for asset, specs in ASSETS.items():
        print(f"    . '{asset}' is processing.")
        
        # X, sr, etc
        X_asset = features[asset][:]
        sr = features[asset].attrs['sr']
        
        # change unit
        if specs['type'] in ['spectrogram']:
            scale = specs['scale']
            unit = features[asset].attrs['unit']
            X_asset = unit_converter(X_asset, scale, unit)
            
        # set function
        if asset in ['pcm']:
            func = partial(save_waveform, sr=sr, **PARAMS[asset])
        elif asset in ['stft', 'mel', 'zstft', 'zmel']:
            func = partial(save_spectrogram, **PARAMS[asset])
        elif asset in ['rms']:
            func = partial(save_rms, **PARAMS[asset])
        
        # parse specs
        ext = specs['extension']
        
        # execute
        for idx, f in enumerate(tqdm(Files)):
            # set destpath
            dstpath =  os.path.join(DIRS['assets'], asset, f"{f.rsplit('.', 1)[0]}.{ext}")
            # execute
            func(X_asset[idx], savepath=dstpath)
            # append dstpath
            list_assets.at[list_assets['filename']==f, asset] = dstpath.replace(DIRS['root'], '').strip('/')
            
    print("  - Saving assets done!")
    
    ################################################################
    # udatate history
    ################################################################
    # update history
    history_ = pd.DataFrame({
        'lot': sorted(history['lot'].unique()),
        'posted': TIME,
    })
    update_table(DB, 'history', history_, key='lot')
    print(f"  - Project history updated. (posted datetime updated)")    
    
    # update label.csv
    list_assets.to_csv(os.path.join(DIRS['assets'], 'assets.csv'), index=False)
    print(f"  - assets/assets.csv is updated.")
    
    # lienbreak
    print("")
