import os
from pathlib import Path
import numpy as np
import pandas as pd
import dask.bag as db
import dask.dataframe as dd
import h5py
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
import shutil
import random
from tqdm import tqdm

from ..admin.config import ROOT, MDB, PROJECT_SUBDIRS, MAP_TIMESTAMP, EXTENSIONS
from ..admin.dbio import read_table


################################################################################################################################
## FILES management
################################################################################################################################

################################################################
## list_subdirs
################################################################
def get_directory_size(root='.'):
    '''
    directory의 size를 반환
    
    Arguments
    ---------
    root : string or path
    
    Returns
    -------
    total_size : int (bytes)
    '''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
            
    return total_size

################################################################
## list_subdirs
################################################################
def list_subdirs(root, fullname=False, reverse=False):
    '''
    directory의 1차 하위 디렉토리 목록을 정렬하여 반환
    '''
    
    # do
    if fullname:
        subdirs = sorted(
            [d.path for d in os.scandir(root) if d.is_dir()],
            reverse = reverse
        )
    else:
        subdirs = sorted(
            [d.name for d in os.scandir(root) if d.is_dir()],
            reverse = reverse
        )
    
    return subdirs

################################################################
## list_trees
################################################################
def tree(root, exts=EXTENSIONS['all'], verbose=False):
    '''
    두 개 이상의 파일(지정된 확장자를 포함한)이 있는 root의 tree를 반환 - root structure 파악할 때 사용
    
    params
      root    탐색할 루트 디렉토리
      ext     탐색할 확장자, default ['tmds', 'wav', 'jpg', 'png', 'gif', 'bmp'], 모든 파일/폴더 구조 보려면 exts=None
      
    return
      <list>      root structure
    '''
    
    return list_trees(root, exts=exts, verbose=verbose)


def list_trees(root, exts=None, verbose=False):
    '''
    두 개 이상의 파일(지정된 확장자를 포함한)이 있는 root의 tree를 반환 - root structure 파악할 때 사용
    
    params
      root   탐색할 루트 디렉토리
      ext         탐색할 확장자
      
    return
      <list>      root structure
    '''
    # set extensions
    if exts is not None:
        # to list if not list
        if type(exts) is not list:
            exts = [exts]
        # strip dot
        exts = [e.strip('.') for e in exts]
    else:
        exts = ['*']
    

    # array of files
    files = np.array(
        list_files(root, exts)
    )

    # array of levels
    levels = np.array(
        [f.count('/') + 1 for f in files]
    )

    # get root tree
    trees = dict()
    for level in set(levels):
        files_ = files[levels == level]
        n_ref = len(files_)
        for i in range(1, level-1):
            subdirs = set([f.rsplit('/', i)[0] for f in files_])
            if len(subdirs) != n_ref:
                break
        trees[level] = sorted(subdirs)
    trees = [l for sublist in trees.values() for l in sublist]
    
    # verbose
    if verbose:
        print(f"Meaningful Structure Under {root}")
        for tree in trees:
            print(f"  - {tree.replace(root, '.')}")
        
    return trees

################################################################
## make list of files (parallel search using dask)
################################################################
def list_files(root, exts='*', posix=False):
    '''
    Parallel version (faster) of list files - using Dask
    
    params
      root    root to scan
      exts    list of extensions to find
      posix   if true, posix path will be returned
      
    return
      (list of files)   list of posix or string paths
    '''
    # root type check
    if type(root) is not list:
        dirs = [root]
        
    # extension type check
    if type(exts) is not list:
        exts = [exts]
    
    # revise extensions
    exts = [ext.strip('.') for ext in exts]
    
    # n patternes
    n_exts = len(exts)
    
    # max no. of partitions ~ no. of CPUs x 2
    n_max = os.cpu_count()
    
    # get partitions
    while len(dirs) * n_exts < n_max:
        # scandir
        dirs_ = [d for subdirs in dirs for d in os.scandir(subdirs)]
        n_files = len([f for f in dirs_ if f.is_file()])
        # break if meet files
        if n_files > 0:
            break
        # update dirs
        dirs = dirs_

    # to dask bag
    dirs = db.from_sequence(
        [':'.join([d.path if type(d) is not str else d, f'**/*.{ext}']) for ext in exts for d in dirs]
    )
    
    # search
    files = dirs.map(lambda d: [f for f in Path(d.split(':')[0]).glob(d.split(':')[-1])])
    files = files.compute()
    
    # return posix path if posix is True
    if posix:
        files = [f for fs in files for f in fs]
    else:
        files = [str(f) for fs in files for f in fs]
    
    return files

################################################################
## make list of extensions
################################################################
def count_extensions(root):
    '''
    directory 재귀적 탐색하여 확장자 카운트 반환
    '''        
    # search
    files = list_files(root, '*', posix=True)
    extensions = pd.Series(
        [str(f).rsplit('.', 1)[-1] for f in files if not f.is_dir()],
        name = 'extensions'
    )
    return extensions.value_counts()

################################################################
## check duplicated date
################################################################
def infer_duplicates(files):
    '''
    filename 확인하여 중복 의심되는 index 반환 (사례: augmentated data가 원본에 섞임)
    
    params
      files    <pd.Series> or <list> list of filenames or filepaths
      
    return
      dataframe with fields;
        - is_dups: orginal or copied (추정)
        - is_original: original file (추정)
        - is_copied: copied file (추정)
    '''
    # init
    files = pd.Series(
        [f.rsplit('/', 1)[-1] for f in files],
        name='filename'
    )
    
    # get lengths
    lengths = np.array(
        [len(f.rsplit('.', 1)[0]) for f in files]
    )
    
    # when length is not fixed, duplicates may exist
    if len(set(lengths)) > 1:
        # original files ~ files w/ shortest filename
        min_length = lengths.min()
        shorten = pd.Series(
            [f[:min_length] for f in files], 
            name='shorten'
        )
    
        # update flag
        duplicates = shorten.duplicated(keep=False).to_numpy()
        
        df_flag = pd.DataFrame({
            'filename': files,
            'origin': shorten,
            'is_dups': duplicates,
            'is_original': lengths == min_length,
            'is_copied': (lengths != min_length) & duplicates
        })
        
        return df_flag
        
    else:
        return None

    
################################################################################################################################
## GET PROJECT's SOMETHING
################################################################################################################################

################################################################
## gen_db_dirs
################################################################
def gen_project_db_dirs(project):
    '''
    project의 DB, DIRS를 생성하여 반환
    
    params
      project   project code (예: airpurifier, dishwasher)
      
    return
      DB, DIRS
    '''
    
    #### FIXED VARIABLES ####   
    # project's directories
    project_dir = os.path.join(ROOT, project)
    DIRS = {
        d: os.path.join(project_dir, d) for d in PROJECT_SUBDIRS
    }
    DIRS['root'] = project_dir
    
    # project's database
    db_url = f"sqlite:///{project_dir}/project.db"
    DB = create_engine(db_url)
    
    return DB, DIRS


################################################################
## get_project
################################################################
def get_project(project):
    '''
    준비되어 있는 project의 DB, DIRS를 load
    
    params
      project   project code (예: airpurifier, dishwasher)
      
    return
      DB, DIRS
    '''
    
    DB, DIRS = gen_project_db_dirs(project)
    
    # validation - DIRS
    if not os.path.exists(DIRS['root']):
        print(f"[ERROR] No project '{project}' found. Exit!")
        return
    
    # validation - DB
    if not database_exists(DB.url):
        print(f"[ERROR] No project '{project}' found. Exit!")
        return
    
    return DB, DIRS


################################################################
## project_parser
################################################################
def project_parser(project):
    '''
    사용자 편의용 - project, DB, DIRS 중 하나를 입력하면 tuple(project, DB, DIRS)를 반환
    '''
    # parse
    if type(project) is sqlalchemy.engine.base.Engine:
        project = Path(str(project.url).replace('sqlite:///', '')).parent.name
    elif type(project) is dict:
        project = Path(project['root']).name
    elif type(project) is not str:
        print("ERROR!")
        return

    # get info
    DB, DIRS = get_project(project)
    
    return project, DB, DIRS


################################################################
## list_projects
################################################################
def list_projects(full=False, return_=False):
    '''
    등록되어 있는 프로젝트 목록 반환
    
    Example
    -------
    >>> list_projects()
    
    Paramters
    ---------
    full : boolean
        기본 정보 외 모든 정보 반환 (defalt False)
    return_ : boolearn
        프로젝트 목록을 dataframe으로 반환 (default False)
        
    Return
    ------
    (Void) return_=True일 경우 DataFrame 반환
    '''
    
    # read table 'project' from mother database
    tbl = read_table(MDB, 'projects')
    
    # shorten
    if not full:
        tbl = tbl[['code', 'name', 'category', 'client', 'contact', 'opened', 'note']]
        
    print(tbl.to_markdown(index=False, tablefmt='simple'))
    
    # return table if return_
    if return_:
        return tbl


################################################################
## list_lots
################################################################
def list_lots(project, process=None, status=None, verbose=False):
    '''
    지정된 process가 완료된 lot들의 list 반환
    
    params
      DB
      process   ['inventory', 'dataset', 'extract', 'post', 'report']
      forced
      
    return
      (lots_to_update)
    '''
    
    # init
    project, DB, DIRS = project_parser(project)
    
    # read tables from project database
    try:
        history = read_table(DB, 'history')
    except Exception as ex:
        print(f"[ERROR] Cannot load table history - {ex}")
        return
    
    # 아무것도 지정 안하면 df 출력
    SELECT = ['lot', 'extensions', 'n_origin', 'n_valid', 'n_revised', 'added', 'copied', 'extracted', 'posted', 'reported', 'modified']
    if process is None and status is None:
        display(history[SELECT])
        return
    
    # verbose
    if verbose:
        display(history[SELECT])
    
    # all lots
    history = history.set_index('lot')
    lots = sorted(history.index)
    
    # return list of all lots if status is None
    if status is None:
        return lots
    
    # default process is 'extract'
    if process is None:
        process = 'extract'
    
    # map process to timestamp
    try:
        field_stamp = MAP_TIMESTAMP[process]
    except Exception as ex:
        print(f"[ERROR] Process '{process}' is not in {[p for p in MAP_TIMESTAMP.keys()]} - {ex}")
        return
    
    # list complete lots
    lots_complete = []
    for lot in history.index:
        if history.at[lot, field_stamp] is not None:
            if history.at[lot, field_stamp] > history.at[lot, 'modified']:
                lots_complete.append(lot)
    
    # list uncomplete lots
    lots_uncomplete = sorted(set(lots) - set(lots_complete))
    
    # returns
    if status.lower() in ['complete', 'up-to-date']:
        return lots_complete
    elif status.lower() in ['uncomplete', 'modified', 'changed']:
        return lots_uncomplete
    else:
        print("Please Select Status: [None, 'complete', 'modified']")
        return


################################################################
## load_dataset
################################################################
def load_inventory(project, valid_only=True):
    '''
    load inventory of project
    
    Parameters
    ----------
    project : string
        project code (i.e., 'airpurifier')
    valid_only : boolean
    
    Returns
    -------
    DataFrame
        A dataframe of project's inventory
    '''
    DB, DIRS = get_project(project)
    inventory = read_table(DB, 'inventory')
    if valid_only:
        inventory = inventory[inventory['status']!=0].reset_index(drop=True)
        
    return inventory


################################################################
## laod_metadata
################################################################
def load_metadata(project, columns=None, compute=True, verbose=False):
    '''
    load extracted raw data of project as pd.DataFrame
    
    params
      project   project_code (e.g. airpurifier, dishwasher)
      compute   if False, it returns dask dataframe
      verbose   for consistency (will not be used)
    
    return
      extracted raw data <pd.DataFrame>
    '''
    
    # for manager's consistency
    try:
        DB, DIRS = get_project(project)
    except Exception as ex:
        print(ex)
        return

    # read dataset
    history = read_table(DB, 'history')
    inventory = read_table(DB, 'inventory')

    # list of prepared lots
    lots = list_lots(project, process='extract', status='complete')
    
    # read dataset (parquet) and compute
    files = [os.path.join(DIRS['extract'], f"meta_{lot}*.parquet") for lot in lots]
    
    # read parquet
    extracted = dd.read_parquet(files, columns=columns)
    
    # compute if compute
    if compute:
        extracted = extracted.compute().reset_index(drop=True)
    
    return extracted


################################################################
## load_rawdata
################################################################
def load_rawdata(project, columns=None, compute=True, verbose=False):
    '''
    load extracted raw data of project as pd.DataFrame
    
    params
      project   project_code (e.g. airpurifier, dishwasher)
      compute   if False, it returns dask dataframe
    
    return
      extracted raw data <pd.DataFrame>
    '''
    
    # for manager's consistency
    try:
        project, DB, DIRS = project_parser(project)
    except Exception as ex:
        print(ex)
        return

    # read dataset
    history = read_table(DB, 'history')
    inventory = read_table(DB, 'inventory')

    # list of prepared lots
    lots = list_lots(project, process='extract', status='complete')
    
    # read dataset (parquet) and compute
    files = [os.path.join(DIRS['extract'], f"extracted_{lot}*.parquet") for lot in lots]
    
    # read parquet
    extracted = dd.read_parquet(files, columns=columns)
    
    # if verbose
    if verbose:
        history_ = history.set_index('lot')
        translate_ = history_.loc[lots, 'translate'].unique()
        if len(translate_) > 1:
            print(f"Field Map 'TDMS_field: current_field' for {lot}:")
            print(f"  - {history_.at[lot, history]}")
        else:
            print(f"Field Map 'TDMS field: current field':")
            print(f"  - {translate_[0]}")

    # compute if compute
    if compute:
        extracted = extracted.compute().reset_index(drop=True)
    
    return extracted


################################################################
## load_features
################################################################
def load_features(project=None, srcpath=None, custom=None, downloadpath=None, verbose=True):
    '''
    load prepared features.
    
    (example)
    features = load_features('airpurifier') ~ 다른 옵션 지정 불필요
    
    (NOTE)
    이미 처리된 feature들의 저장소로 HDF5 형식 파일을 사용하고 있습니다.
    HDF5 형식은 데이터를 RAM에 load하지 않고 disk에서 바로 access합니다. 
    RAM 크기에 제한 받지 않고 큰 데이터를 저장할 수 있고, 최초 load가 발생하지 않는 장점이 있습니다.
    다만 disk에 빈번히 access하는 만큼 disk 속도에 큰 영향을 받습니다. NFS(NAS)를 사용하면 더욱 늦어집니다.
    분석 속도를 높이려면 downloadpath를 지정하여 HDF5를 local에 다운로드 후 load하시면 됩니다.
    만약 SSD가 있다면 downloadpath로 SSD를 지정하시는 것을 권장합니다.
    
    params
      project        project_code (e.g. airpurifier, dishwasher)
      srcname        srcpath - 사용자 로컬에 저장한 HDF5를 load할 때 사용
      custom         default name (features.hdf5)가 아닌 features를 load할 때 사용
      downloadpath   download path. When it is not None, features will be load after download
    
    return
      extracted raw data <pd.DataFrame>
    '''
    
    if srcpath is None:
        if project is None:
            print('[EXIT] Please set project or srcpath!')
        else:
            # for manager's consistency
            project, DB, DIRS = project_parser(project)    
            # set srcpath
            if custom is None:
                srcpath = os.path.join(DIRS['extract'], 'features.hdf5')
            else:
                srcpath = os.path.join(DIRS['extract'], custom)
    else:
        if project is not None:
            print('[WARNING] If both project and srcpath are given, srcpath will be used.')
    
    # download if download path is not None
    if downloadpath is not None:
        # get size
        size_gb = os.path.getsize(srcpath)/1024/1024/1024
        
        # check before download
        download = True
        maxloop = 3
        
        # is too large?
        if download:
            n=0; chk = 'init'
            if size_gb > 0:
                while (chk not in ['yes', 'no']) and n < maxloop:
                    n += 1
                    chk = input(f"HDF5 file is very large ({size_gb:.1f} GB), download anyway? (yes or no):").lower()
                if chk == 'no':
                    download = False
                
        # already exists?
        if download:
            n=0; chk2 = 'init'
            if os.path.exists(downloadpath):
                while (chk2 not in ['yes', 'no']) and (n < maxloop):
                    n += 1
                    chk2 = input(f"File {downloadpath} exists, overwrite? (yes or no):").lower()
                if chk2 == 'yes':
                    os.remove(downloadpath)
                else:
                    download = False
                
        # download
        if download:
            print(f"Start Download {size_gb:.1f} GB files...", end=" ")
            shutil.copy(srcpath, downloadpath)
            print("DONE!")
            srcpath = downloadpath
                    
    # load
    features = h5py.File(srcpath)
    
    if verbose:
        print(f"Try below commands")
        print(f"  - Y = features['Y'][:]")
        print(f"  - Xmel = features['mel'][:]")
        print(f"  - Xobps = features['obps'][:]")
        print(f"  - F = np.array([x.decode('utf-8') for x in features['filename'][:]])")
        print("")
        print(f"If you need more information, execute 'icu.info_hdf5(features)'.")
        print("")
    
    return features


################################################################
## get_dataset_dir
################################################################
def get_dataset_dir(project, verbose=True):
    '''
    Get dataset directory
    
    Arguments
    ---------
    project : string
        project code (airpurifier, dishwasher, ... try 'icu.list_projects()')
    verbose : boolean
    
    Returns
    -------
    path : stirng 
    '''
    DB, DIRS = get_project(project)
    
    if verbose:
        size_ = get_directory_size(DIRS['dataset'])
        for unit in ['KB', 'MB', 'GB']:
            size_ = size_ / 1024
            if size_ < 1000:
                break
        print(f"Dataset size is {size_:.1f}{unit}. Try 'icu.download_dataset(\'{project}\')'. Local dataset is much faster when training.")
            
    return DIRS['dataset']


################################################################
## download_dataset
################################################################
def download_dataset(project, download_dir='./dataset'):
    '''
    Download dataset
    
    Arguments
    ---------
    project : string
        project code (airpurifier, dishwasher, ... try 'icu.list_projects()')
    
    Returns
    -------
    path : stirng 
    '''
    DB, DIRS = get_project(project)
    
    inventory = read_table(DB, 'inventory')
    inventory = inventory.loc[~inventory['filepath'].isna(), :]
    
    n_copied, n_exists = 0, 0
    for idx in tqdm(inventory.index):
        fp = inventory.at[idx, 'filepath']
        split = inventory.at[idx, 'split']
        label = inventory.at[idx, 'label_origin']
        fn = inventory.at[idx, 'filename']
        
        # check directory exists
        subdir = os.path.join(os.path.abspath(download_dir), split, label)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
            
        # check file exsits and copy
        dst = os.path.join(subdir, fn)
        if not os.path.exists(dst):
            shutil.copy(fp, dst)
            n_copied += 1
        else:
            n_exists += 1
            
    print(f"[Done!] {n_copied} copied, {n_exists} already exists.")


################################################################
## load_features
################################################################
def info_hdf5(features, feature=None):
    '''
    HDF5의 정보를 쉽게 확인
    '''
    # prep description if exists
    get_desc = lambda feature: features[feature].attrs['desc'] if 'desc' in features[feature].attrs.keys() else 'no description.'
    
    # feature를 지정하지 않으면 전체 dataset의 이름을 출력
    if feature is None:
        rj = max([len(feature) for feature in features.keys()])
        print(f"You have {len(features.keys())} dataset in features.hdf5;")
        for feature in features.keys():
            dataset_name = f"'{feature}'".ljust(rj+2)
            print(f"  - {dataset_name}: {get_desc(feature)}")
        print("")
        print(f"If you need more information, execute 'icu.info_hdf5(features, dataset_name)'.")
    
    # feature를 지정하면 해당 dataset의 정보를 출력
    else:
        print(f"'{feature}': {get_desc(feature)}")
        print(f"  - shape {features[feature].shape}")
        print(f"  - properties")
        for prop in features[feature].attrs.keys():
            value = features[feature].attrs[prop]
            if type(value) is np.ndarray:
                if value.ndim > 1 or value.shape[0] > 3:
                    s = f"{type(value)} w/ shape {value.shape}"
            elif type(value) is list:
                if len(value) > 3:
                    s = f"{type(value)} w/ {len(value)} elements; {', '.join([e for e in value[:3]])}, ..."
            else:
                s = value
            print(f"    . {prop}: {s}")


################################################################
## load_project
################################################################
def load_project(project):
    '''
    project의 모든 정보, 데이터를 로드 - 리포트 init 용
    
    return
      project, DB, DIRS, history, inventory, revisions, rawdata, features, Y, L
    
    return info.
      Y   encoded label ~ 0, 1, ...
      L   string label ~ OK, NG, ...
      F   filenames
    '''
    # mother database
    info = (
        pd.read_sql_table('projects', MDB)
        .set_index('code')
        .loc[project, :]
        .to_dict()
    )

    # project urls
    project, DB, DIRS = project_parser(project)

    # get project tables
    history = read_table(DB, 'history')
    inventory = read_table(DB, 'inventory')
    revisions = read_table(DB, 'inventory')

    # data
    rawdata = load_rawdata(project)
    features = load_features(project, verbose=False)

    # parse features
    Y = features['Y'][:]
    decoder = eval(features['Y'].attrs['decoder']) if 'decoder' in features['Y'].attrs.keys() else None
    if decoder is not None:
        if 'ok' not in decoder[0].lower():
            print("[WARNING] Coded class 0 is not OK class! Please check!")
        L = np.array([decoder[y] for y in features['Y'][:]])
    else:
        L = Y
    F = np.array([f.decode('utf-8') for f in features['filename'][:]])
        
    # prep assets
    assets = pd.read_csv(os.path.join(DIRS['assets'], 'assets.csv'))
    
    return project, DB, DIRS, info, history, inventory, revisions, rawdata, features, Y, L, F, assets


################################################################################################################################
## Machine Learning Preps
################################################################################################################################

################################################################
## sort_labels
################################################################
def sort_labels(labels):
    '''
    클래스 순서를 정렬
    sort_labels([NG_1, OK, NG_2, OK, NG_1, ...]) -> ['OK', 'NG_1', 'NG_2', 'NG_3']
    '''
    PATTERN_OK = 'ok'
    INCLASS_REVERSE = False
    
    classes = set(labels)
    ok_labels = sorted({l for l in labels if isinstance(l, (int, bool, np.int, np.bool_)) or PATTERN_OK in l.lower()}, reverse=INCLASS_REVERSE)
    other_labels = sorted({l for l in labels if l not in ok_labels}, reverse=INCLASS_REVERSE)
        
    return ok_labels + other_labels

################################################################
## sampling
################################################################
def eda_sampling(tbl, by, n=None, nested=False, sort=True, verbose=True):
    '''
    (예) eda_sampling(df, 'label_origin', n=100, )
    
    by에 지정된 columns로 groupby한 뒤 각 group에서 동일 개수의 sample을 추출.
    EDA 시 OK 개수가 상대적으로 많아 NG의 분포가 가려지는 것을 완화하기 위해 사용.
    
    params
      tbl      <pd.DataFrame>
      by       <str> or <list> groupby할 columns ~ 예: label_origin
      n        n을 지정, n보다 부족한 sample은 최대한의 sample 출력
      nested   True이면 샘플링 결과를 dictionary로 반환. 예, outputs['NG'], outputs['OK'], ...
      sort     True이면 샘플링 결과를 입력 dataframe의 index 순서로 재정렬, default True
    
    return
      <pd.DataFrame>   sampled dataframe (nested=True이면 dictionary of dataframes)
    
    '''
    # multi index available
    if type(by) is not list:
        by = [by]
    
    # dummy index to get series count
    df = tbl.copy(deep=False)
    
    # idxs is sets of multi indices
    summary = df.groupby(by)['filename'].count()
    groups = summary.index
    
    # 가장 적은 sample을 가진 group의 sample 수
    n_min = summary.min()
    
    # message용 rjust 간격
    rj_total = len(str(summary.max()))
    rj_sample = len(str(n))
    
    # sampling n rows for each 'by'
    outputs = dict()
    message = "Sampling Results:"
    for group in groups:
        # if group is multi-index
        if type(group) is tuple: 
            group = list(group)
        # if group is single index
        if type(group) is not list: 
            group = [group]
        
        # sampling from each groups
        df_group = df
        for field, ref in zip(by, group):
            df_group = df_group.loc[df_group[field]==ref, :]
        
        # n이 지정되지 않으면 sample 가장 적은 group의 sample 수를 기준으로
        n_group = len(df_group)
        n_samples = n_min if n is None else min(n_group, n)
        
        # sampling
        df_group = df_group.sample(n=n_samples)
        
        # append message
        message += f"\n  - Group {'/'.join(group)}: {str(n_samples).rjust(rj_sample)} samples / {str(n_group).rjust(rj_total)} total"
        
        # sort if sort
        if sort:
            df_group = df_group.sort_index()
        
        # nested outputs' keys are [level1, level2]
        outputs['/'.join(group)] = df_group
    
    if verbose:
        print(message)
        
    if not nested:
        outputs = pd.concat([v for k, v in outputs.items()])
        if sort:
            outputs = outputs.sort_index()
        
    return outputs


################################################################
# split_train_test
################################################################
def split_train_test(df, by, ratio_test=0.2, n_min=2, n_max=10e4):
    '''
    dataframe을 train, test로 split하고 그 결과를 field 'split'에 추가하여 반환
    예: split_train_test(df, by='label_origin', )
    
    params
      df          split할 dataframe
      by          split할 때 비율을 유지할 fields (보통 label의 비율을 유지) ~ list를 입력하면 계층적으로 비율을 유지할 수 있음 (예: by=['label', 'channel'])
      ratio_test  test 비율 (default=0.2)
      n_min       test에 포함될 최소 개수 (by 기준)
      n_max       test에 포함될 최대 개수
      
    return
      'split' field가 추가된 df ~ 'split' field는 'test', 'train' 두 개의 level을 가짐
    '''
    if type(by) is not list:
        by = [by]

    # n_test for each groups
    sorter = df[by].assign(_idx = lambda x: df.index).set_index(by).sort_index()
    n_test = sorter.groupby(sorter.index.names).count().apply(lambda x: np.clip(np.rint(x * ratio_test), n_min, n_max), raw=True).astype(int)

    # get test indices
    test_indices = []
    for idx in set(sorter.index):
        test_indices += sorter.loc[idx, '_idx'].sample(n=n_test.at[idx, '_idx'].item()).tolist()

    # write train-test flags
    df_ = df.copy()
    df_.loc[:, 'split'] = 'train'
    df_.loc[test_indices, 'split'] = 'test'
    
    return df_


################################################################
# make labels inferred from subdirs
################################################################
def make_labels(root, hrchy='label', exts='all'):
    '''
    root 내 파일들의 filename, filepath 및 하위 디렉토리 이름을 데이터프레임으로 반환
    (예) root가 '/dataset'인 아래 구조의 hrchy는 'channel/label'임
      /dataset
          ├ CH1
          │   ├ NG
          │   └ OK
          └ CH2
              ├ NG
              └ OK
      
      /dataset/channel/NG, /dataset/channel/OK로 나뉜 dataset의 subdir_structure='channel/NG'
    '''
    
    if not isinstance(exts, list):
        if exts in EXTENSIONS.keys():
            exts = EXTENSIONS['all']
        else:
            exts = [exts]
    
    files = list_files(root, exts=exts, posix=True)
        
    labels = pd.DataFrame({
        'filename': [f.name for f in files],
        'filepath': [str(f) for f in files],
        'hrchy': [str(f).replace(root, '').strip('/') for f in files]
    })
    
    # set field names
    hrchy = hrchy.split('/')
    
    fields = labels['hrchy'].str.split('/', expand=True).iloc[:, :len(hrchy)]
    fields.columns = hrchy
    
    # merge labels with fields
    labels = pd.concat([labels, fields], axis=1).drop(columns='hrchy')
    
    return labels


################################################################
# slice dataframe 
################################################################
def estimate_parquet_size(func, input_, n_samples=100, **kwargs):
    
    TEMP_FILENAME = 'parquet_size_check.parquet'
    
    if type(input_) is not list:
        input_ = list(input_)
    n_total = len(input_)
    samples = random.sample(input_, n_samples)
    
    output = func(samples, **kwargs)
    if type(output) is not pd.DataFrame:
        output = pd.DataFrame(output)
    output.to_parquet(TEMP_FILENAME)
    
    sample_size_mb = os.path.getsize(TEMP_FILENAME)/1024/1024
    required_memory_gb = output.memory_usage(index=True, deep=True).sum()/n_samples*n_total/1024/1024
    n_rows_per_parquet = int(1024 / sample_size_mb * n_samples)
    
    os.remove(TEMP_FILENAME)
    
    print(f"#### Parquet Size Estimation ####")
    print(f" - write 1 parquet per {n_rows_per_parquet} rows (for 1 GB/parquet)")
    print(f" - if you load all {n_total} rows at once, {required_memory_gb:.0f} GB will be required")
    
    return n_rows_per_parquet, required_memory_gb


################################################################
# slice dataframe 
################################################################
def slice_df(df, chunk_size=None, n_chunks=None):
    '''
    input
    :df: dataframe
    :chunk_size: 
    :n_chunks:
    
    return
    dict(i:padded_string, chunk:dataframe)
    '''
    
    len_df = len(df)
    
    if n_chunks and not chunk_size:
        chunk_size = np.ceil(len_df / n_chunks).astype(int)
    if chunk_size and not n_chunks:
        n_chunks = np.ceil(len_df / chunk_size).astype(int)
    else:
        print("set a parameter between chunk_size and n_chunks")
        return None
    
    n_zfill = np.trunc(np.log10(n_chunks)).astype(int) + 1
    
    return {f"{str(i+1).zfill(n_zfill)}": df[i*chunk_size:(i+1)*chunk_size].reset_index(drop=True) for i in np.arange(0, n_chunks)}


################################################################
# encode labels
################################################################
def encode_labels(list_labels, reverse=True, verbose=True):
    '''
    (NG, OK) become (1, 0) if reverse else (0, 1)
    (NG1, NG2, NG3, OK) becomes (3, 2, 1, 0) if reverse else (0, 1, 2, 3)
    
    params
      labels   list of labels in string
      reverse
      verbose
      
    return
      <list>, <dict>, <dict>   encoded labels, encoder, decoder
    '''
    names = sort_labels(list_labels)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    encoded_labels = np.array([encoder[x] for x in list_labels])
    
    if verbose:
        print(f'<LABELS> {len(names)} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return encoded_labels, encoder, decoder


################################################################
# one hot encode labels
################################################################
def one_hot_encode_labels(list_labels, class_nothing='', verbose=True):
    '''
    binary cross entropy 사용을 위한 one_hot_encoding
    class_nothing class 지정하면 해당 class는 (0, 0, ..., 0) 값을 가짐 (예를 들어 OK를 OK으로 분류하는 것이 아니라 아무것도 아님으로 분류)
    '''
    names = sort_labels('|'.join(list_labels).split('|'))
    if class_nothing in names:
        names.remove(class_nothing)
    
    n_classes = len(names)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    #### one hot encoding
    encoded_labels = []
    for lab in list_labels:
        label_vector = n_classes * [0]
        classes = lab.split('|')
        if class_nothing in classes:
            classes.remove(class_nothing)
        for c in classes:
            label_vector[encoder[c]] = 1
        encoded_labels.append('|'.join([str(e) for e in label_vector]))
    
    if verbose:
        print(f'<LABELS> {n_classes} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return encoded_labels, encoder, decoder
      
        
################################################################
# make_confusion_matrix
################################################################
# def make_confusion_matrix(truth, predict):
#     cm = pd.crosstab(truth, predict)
#     for l in cm.index:
#         if l not in cm.columns:
#             cm[l] = 0
#     return cm[cm.index]
