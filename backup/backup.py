#!/usr/bin/python3

# Schedule this script to run on set interval using systemd/cron
from datetime import datetime
import os

current_time = datetime.now()
custom_time_format = '%a, %Y %b %d at %H:%M:%S.%f'

file_name = current_time.isoformat() # current_time.strftime(custom_time_format)
file_name = file_name.replace(' ', '\ ')

backup_command = f"pg_dump -U rivia -d rivia_soft -h 127.0.0.1 -f ~/db_backups/{file_name}.sql"
os.system(backup_command)

overwrite_latest_backup = f"pg_dump -U rivia -d rivia_soft -h 127.0.0.1 -f ~/db_backups/latest.sql"
os.system(overwrite_latest_backup)
