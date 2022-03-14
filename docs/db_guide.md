# Data base guide

### Creating database
Enter the following commands (bash for example, 
you may use CMD or PowerShell analogs, guide for windows<a href="https://www.microfocus.com/documentation/idol/IDOL_12_0/MediaServer/Guides/html/English/Content/Getting_Started/Configure/_TRN_Set_up_PostgreSQL.htm"> here</a>):
* Run PostgreSQL server: 
`$ sudo service postgresql start`.
* Check if it runs: `$ service postgresql status`. If it's ok, 
you will see
something like this: `14/main (port 5432): online`.
* Run psql: `$ sudo -u postgres psql`.
* Enter command `CREATE DATABASE questmaker;`.
* Enter command `\l`. You must see `questmaker` in databases list.

### Create config file
* In `QuestMaker/website` create new folder `instance`.
* In this folder create file `config.py`
* File must contain following keys:
  ```
  DB_NAME = 'questmaker'
  DB_USER = 'postgres'
  DB_PASSWORD = 'postgres'
  DB_HOST = 'localhost'
  DB_PORT = '5432'
  ```
  DB_NAME is `questmaker` if you did previous step. 
  DB_USER, DN_HOST and DB_POST is default. You should only
  set any password for user `postgres`. Just run psql again
  and enter command `\password postgres`. Then type password you want.

### Launch init script
* Enter `QuestMaker/website`. Then set `FLASK_APP` (see `README.md` for website).
* Enter command `flask init-db`.

Congratulations! You've created local PostgreSQL 
database and initialize it with tables
described in `schema.sql` script.