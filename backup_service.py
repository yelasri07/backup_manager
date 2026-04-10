import os
import time
import tarfile 
from datetime import datetime

SCHEDULE_FILE = 'backup_schedules.txt'
LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'backup_service.log')
BACKUP_DIR = 'backups'

def setup_envirenment():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
    except Exception as e:
        print(f"Critical error setting up environment: {e}")
    
def log(message):
    try:
        now = datetime.now().strftime("[%d/%m/%Y %H:%M]")
        with open(LOG_FILE, 'a') as f:
            f.write(f"{now} {message}\n")
    except Exception:
        pass

def create_tar_backup(source_path, backup_name):
    tar_path = os.path.join(BACKUP_DIR, f"{backup_name}.tar")
    try:
        with tarfile.open(tar_path, 'w') as tar:
            tar.add(source_path, arcname=os.path.basename(source_path))
        log(f"Backup done for {tar_path} in backups/{backup_name}.tar")
    except Exception as e:
        log(f"Error: failed to backup {source_path}: ({e})")

def process_backup_schedules():
    if not os.path.exists(SCHEDULE_FILE):
        return
    
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            schedules = f.readlines()
            remaining_schedules = []
        current_time = datetime.now()
        current_minutes = current_time.hour * 60 + current_time.minute

        for line in schedules:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(';')
            if len(parts) != 3:
                continue # Skip malformed lines

            source_path, sched_time_str, backup_name = parts
            
            try:
                h, m = map(int, sched_time_str.split(':'))
                sched_minutes = h * 60 + m
            except ValueError:
                remaining_schedules.append(line + '\n')
                continue

            # Process if the time matches
            if sched_minutes == current_minutes:
                create_tar_backup(source_path, backup_name)
            
            # Keep schedule only if its time is in the future
            if sched_minutes > current_minutes:
                remaining_schedules.append(line + '\n')

        # Rewrite the schedule file with only future tasks
        with open(SCHEDULE_FILE, 'w') as f:
            f.writelines(remaining_schedules)

    except Exception as e:
        log(f"Error: failed to process schedules ({e})")

def main():
    setup_envirenment()
    while True:
        process_backup_schedules()
        # Sleep for 45 seconds to save CPU cycles
        time.sleep(45)

if __name__ == "__main__":
    main()