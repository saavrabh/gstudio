### GENERIC STRUCTURE:

```
State (State Code)                              [ LEVEL 1 ]
    - School (School Code + Server ID)          [ LEVEL 2 ]
        - gstudio (Clix Platform)               [ LEVEL 3 ]
            - db                                [ LEVEL 4 ]
            - media                             [ LEVEL 4 ]
            - rcs-repo                          [ LEVEL 4 ]
            - pgdump-YYYYMMDD-HHMM.sql          [ LEVEL 4 ]
            - local_settings.py                 [ LEVEL 4 ]
            - server_settings.py                [ LEVEL 4 ]
            - git-commit.log                    [ LEVEL 4 ]
        - unplatform (Optional)                 [ LEVEL 3 ]
```

**[ LEVEL 1 ] : State (State Code)**
- Small case state code, which we had used in our school instances.
- Possible values: 
    - Mizoram      : **mz**
    - Rajasthan    : **rj**
    - Chhattisgarh : **ct**
    - Telangana    : **tg**

**[ LEVEL 2 ] : School (School Code + Server ID)**
- It's combination of "school code" and "server id"
- i.e: `<school code>-<server id>`
- Example: 2031001-mz1

> *NOTE:
In Actual school data collection, Considering "Unplatform" and/or "clixserver"(gstudio) will be active in fields. Hence making provision for unplatform folder along with clixserver. To keep script generic and distinct from unplatform, we are naming `clixserver` as `gstudio`.*

**[ LEVEL 3 ] : gstudio**
- A CLIx Platform, clixserver.
- gstudio Folder will have following items:
    - `db`: mongoDB data.
    - `media`: Files uploaded on clixserver.
    - `rcs-repo`: rcs, versioned json files.
    - `pgdump-YYYYMMDD-HHMM.sql`: Postgres DB dump with specified naming convention.
    - `local_settings.py`: Copy of file in deployed instance.
    - `server_settings.py`: Copy of file in deployed instance.
    - `git-commit.log`: Snapshot of git records at time of backup. It will have output of following git commands:
        - `git status`
        - `git diff`
        - `git log -5`
        - `git branch`


---

### EXAMPLE STRUCTURE:
```
Example-data-collection-dir-str/
├── ct
│   └── 1011011-ct11
│       ├── gstudio
│       │   ├── db
│       │   ├── git-commit.log
│       │   ├── local_settings.py
│       │   ├── media
│       │   ├── pgdump-20170921-1305.sql
│       │   ├── rcs-repo
│       │   └── server_settings.py
│       └── unplatform
└── mz
    └── 2031001-mz1
        └── gstudio
            ├── db
            ├── git-commit.log
            ├── local_settings.py
            ├── media
            ├── pgdump-20170921-1305.sql
            ├── rcs-repo
            └── server_settings.py
```