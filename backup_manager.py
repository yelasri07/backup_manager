import sys
import re
from datetime import datetime
import os

def main():
    args = sys.argv
    if len(args) <= 1:
        print("Usage: python3 ./backup_manager.py [OPTION]")
        exit(1)

    option = args[1]

    match option:
        case "create":
            if len(args) <= 2:
                print("Usage python3 ./backup_manager.py create [schedule]")
                exit(1)

            handle_create(args[2])
        case "list":
            handle_list()
        case "delete":
            if len(args) <= 2:
                print("Usage python3 ./backup_manager.py delete [index]")
                exit(1)

            try:
                handle_delete(int(args[2]))
            except:
                print("Invalid index number")
                exit(1)
        case "start":
            handle_start()
        case "stop":
            handle_stop()
        case "backups":
            handle_backups()
        case _:
            print("Invalid option")
            exit(1)

def handle_create(schedule: str):

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M")
    log_message = f"[{current_time}] Error: malformed schedule: {schedule}"
    if is_valid_schedule(schedule):
        log_message = f"[{current_time}] New schedule added: {schedule}"
        backup_schedules_file = open("backup_schedules.txt", "a")
        backup_schedules_file.write(schedule + "\n")
        backup_schedules_file.close()

    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    log_file = open("./logs/backup_manager.log", "a")
    log_file.write(log_message + "\n")
    log_file.close()
    
    

def handle_list():
    print("hello world")

def handle_delete(index: int):
    print(index)

def handle_start():
    print("hello world")

def handle_stop():
    print("hello world")

def handle_backups():
    print("hello world")

def is_valid_schedule(schedule: str):
    is_valid_schedule = re.search("^[\/\w.]+;\d{2}:\d{2};[\w.]+$", schedule)
    if is_valid_schedule == None:
        return False
    
    timestamp = schedule.split(";")[1].split(":")
    
    hour = int(timestamp[0])
    minute = int(timestamp[1])

    if hour >= 24 or minute >= 60:
        return False

    return True
    
if __name__ == "__main__":
    main()