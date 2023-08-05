import os
from sqlalchemy import create_engine


# NFS ROOT
ROOT = '/nas001/projects/ia'

# HOST
HOST = 'http://mi.lge.com'

# ENGINE of MOTHER DATABASE
MDB = create_engine(f"sqlite:///{os.path.join(ROOT, 'projects.db')}")

# TABLE PROJECT
# key can be 'PRIMARY KEY', 'PRIMARY KEY AUTOINCREMENT'
MDB_TABLES = {
    'projects': {
        'code': {
            'dtype': 'TEXT', 'key': 'PRIMARY KEY',
        },
        'name': {
            'form': 'Input Project Name in Korean',
            'dtype': 'TEXT',
        },
        'category': {
            'form': 'Input Project Category (Image, Audio, or Video, ...)',
            'dtype': 'TEXT',        
        },
        'client': {
            'form': 'Input Client (Division, Organization, or Team, ...)',
            'dtype': 'TEXT',        
        },
        'contact': {
            'form': 'Input Contact Person (Member of Client)',
            'dtype': 'TEXT',
        },
        'opened': {
            'form': 'Input Opened Date (YYYY-MM-DD), Leave Empty if Today',
            'dtype': 'TEXT',
        },
        'closed': {
            'dtype': 'TEXT',
        },
        'site_url': {
            'dtype': 'TEXT',
        },
        'project_dir': {
            'dtype': 'TEXT',
        },
        'project_db': {
            'dtype': 'TEXT',
        },
        'note': {
            'form': 'Input Project Description',
            'dtype': 'TEXT',
        },
    }
}

# PROJECT_SUBDIRS
PROJECT_SUBDIRS = [
    'origin',     # 프로젝트 데이터들의 upload dir.
    'dataset',    # origin dir.를 학습에 적합하게 재구성
    'extract',    # extract된 parquet, hdf5를 저장
    'assets',     # wave, mel 등의 multimedia 파일들을 추출하여 저장
    'reports',    # 프로젝트 관련 html 리포트 저장 - (NEW!) REFACTORING 시 주의
    'revisions',  # 레이블 교정 지시서 upload dir.
    'logs'        # 프로젝트 진행 logs (아직 사용 안 함, 자동학습 등의 log 기록할 예정)
]

# PROJECT_TABLE_MODELS
# (참고) inventory는 다소 무의미함
#   - 과제에 따라 fields가 추가될 수 있어 기존 overwrite하는 식으로 update ~ 실제 자료형은 update_inventory에서 결정 됨
#   - 다만 project 초기화 직후 각 table이 존재하는 상태여야 이후 process 진행되기 때문에, dummy 역할 정도 수행
PROJECTDB_TABLES = {
    'inventory': {
        'lot': {'dtype': 'CHARACTER', },
        'split': {'dtype': 'CHARACTER', },
        'originpath': {'dtype': 'VARCHAR', 'key': 'PRIMARY KEY', },
        'filepath': {'dtype': 'VARCHAR', },
        'filename': {'dtype': 'VARCHAR', },
        'status': {'dtype': 'BIGINT', },
        'log': {'dtype': 'TEXT', },
        'added': {'dtype': 'TEXT', },
        'inventoried': {'dtype': 'TEXT', },
        'modified': {'dtype': 'TEXT', }, 
        'note': {'dtype': 'TEXT',
        }, 
    },
    'history':   {
        'lot': {'dtype': 'CHARACTER', 'key': 'PRIMARY KEY', },
        'status': {'dtype': 'CHARACTER'},
        'extensions': {'dtype': 'CHARACTER'},
        'n_origin': {'dtype': 'BIGINT'},
        'n_valid': {'dtype': 'BIGINT'},
        'n_invalid': {'dtype': 'BIGINT'},
        'n_revised': {'dtype': 'BIGINT'},
        'added': {'dtype': 'TEXT'},          # 새로 추가 됨 - refactoring할 때 주의
        'inventoried': {'dtype': 'TEXT'},
        'copied': {'dtype': 'TEXT'},
        'extracted': {'dtype': 'TEXT'},
        'featured': {'dtype': 'TEXT'},       # 새로 추가 됨 - refactoring할 때 주의
        'posted': {'dtype': 'TEXT'},
        'reported': {'dtype': 'TEXT'},
        'modified': {'dtype': 'TEXT'},
        'translate': {'dtype': 'TEXT'},
        'note': {'dtype': 'TEXT'},
        'stats': {'dtype': 'BLOB'}, 
    },
    'revisions': {
        'id': {'dtype': 'INTEGER', 'key': 'PRIMARY KEY AUTOINCREMENT'},
        'confirmed': {'dtype': 'TEXT'},
        'filename': {'dtype': 'VARCHAR'},
        'label': {'dtype': 'CHARACTER'},
        'label_before': {'dtype': 'CHARACTER'},
        'label_revised': {'dtype': 'CHARACTER'},
        'confirmer': {'dtype': 'VARCHAR'},
        'note': {'dtype': 'TEXT'}, 
    },
}

# DATATIME FIELDS
DATETIME_FIELDS = {
    'added',      # 파일 업로드 datetime (파일 mtime)
    'inventory',      # inventory 최초 추가 datetime
    'modified',   # 변경이 발생한 datetime
    'copied',     # dataset lunk 최종 갱신 datetime
    'extracted',  # extracted.parquet 최종 갱신 datetime
    'featured',   # features.hdf5 최종 갱신 datetime
    'posted',     # sound tool 최종 갱신 datetime
    'reported',   # report 최종 갱신 datetime
    'confirmed',  # label 변경 confirm된 날짜 - 오직 revisions table에서만 사용
}

# PROCESS-TIMESTAMP MAPPER
MAP_TIMESTAMP = {
    'inventory': 'inventoried',
    'dataset': 'copied',
    'extract': 'extracted',
    'post': 'posted',
    'report': 'reportd'
}

# EXTENSIONS
EXTENSIONS = {
    'audio': ['wav', 'tdms', 'mp3'],
    'image': ['png', 'jpg', 'gif', 'bmp'],
}
EXTENSIONS['all'] = [extension for extensions in EXTENSIONS.values() for extension in extensions]

# ASSETS - 사운드툴, labeler에 사용 됨
ASSETS = {
    'pcm': {
        'type': 'wavform',
        'extension': 'wav',
    },
    'rms': {
        'type': 'rms', 
        'extension': 'png',
        'cutoff_percentile': (1, 99),
    },
    'stft': {
        'type': 'spectrogram',
        'extension': 'png',
        'scale': 'log',
        'colormap': 'magma',
        'cutoff_percentile': (1, 99),
    },
    'mel': {
        'type': 'spectrogram',
        'extension': 'png',
        'scale': 'log',
        'colormap': 'magma',
        'cutoff_percentile': (1, 99),
    },
    'zstft': {
        'type': 'spectrogram',
        'extension': 'png',
        'scale': 'linear',
        'colormap': 'bwr',
        'cutoff_percentile': (1, 99),
    },
    'zmel': {
        'type': 'spectrogram',
        'extension': 'png',
        'scale': 'linear',
        'colormap': 'bwr',
        'cutoff_percentile': (1, 99),
    },
}
