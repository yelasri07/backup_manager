import sys
import re
from datetime import datetime
import os
import subprocess

def main():
    args = sys.argv
    if len(args) <= 1:
        print("Usage: python3 ./backup_manager.py [OPTION]")
        exit(1)

    option = args[1]

    try:
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

                index: int
                try:
                    index = int(args[2])
                except:
                    write_log("Error: invalid index number")
                    exit(1)

                handle_delete(index)
            case "start":
                handle_start()
            case "stop":
                handle_stop()
            case "backups":
                handle_backups()
            case _:
                write_log("Error: unknown command")
                exit(1)
    except Exception as e:
        write_log(str(e))

def handle_create(schedule: str):
    log_message = f"Error: malformed schedule: {schedule}"
    if is_valid_schedule(schedule):
        log_message = f"New schedule added: {schedule}"
        backup_schedules_file = open("backup_schedules.txt", "a")
        backup_schedules_file.write(schedule + "\n")
        backup_schedules_file.close()

    write_log(log_message)

def handle_list():
    if not os.path.exists("backup_schedules.txt"):
        write_log("Error: can't find backup_schedules.txt")
        return

    schedules_file = open("backup_schedules.txt")
    result = ""
    index = 0
    for line in schedules_file:
        result += f"{index}: {line}"
        index += 1
    print(result.strip("\n"))
    write_log("Show schedules list")

def handle_delete(index: int):
    if not os.path.exists("backup_schedules.txt"):
        write_log("Error: can't find backup_schedules.txt")
        return
    
    lines = []
    
    file = open("backup_schedules.txt")
    lines = file.readlines()
    file.close()

    if index >= len(lines):
        write_log(f"Error: can't find schedule at index {index}")
        return

    file = open("backup_schedules.txt", "w")
    for number, line in enumerate(lines):
        if number == index: 
            continue

        file.write(line)

    write_log(f"Schedule at index {index} deleted")


def handle_start():
    res = subprocess.run(["pgrep", "-f", "backup_service.py"], capture_output=True, text=True)
    if res.stdout != "":
        write_log("Error: backup_service already running")
        return

    subprocess.Popen(["python3", "./backup_service.py"])
    write_log("backup_service started")

def handle_stop():
    res = subprocess.run(["pgrep", "-f", "backup_service.py"], capture_output=True, text=True)
    if res.stdout == "":
        write_log("Error: can't stop backup_service")
        return
    
    subprocess.run(["kill", res.stdout.strip("\n")])
    write_log("backup_service stopped")

def handle_backups():
    if not os.path.exists("./backups"):
        write_log("Error: can't find backups directory")
        return
    
    res = subprocess.run(["ls", "./backups"], capture_output=True, text=True)
    if res.stderr != "":
        write_log(res.stderr.strip("\n"))
        return
    
    print(res.stdout.strip("\n"))
    write_log("Show backups list")

def is_valid_schedule(schedule: str):
    is_valid_schedule = re.search("^[\\w./-]+;\\d{2}:\\d{2};[\\w.]+$", schedule)
    if is_valid_schedule == None:
        return False
    
    timestamp = schedule.split(";")[1].split(":")
    
    hour = int(timestamp[0])
    minute = int(timestamp[1])

    if hour >= 24 or minute >= 60:
        return False

    return True

def write_log(message: str):
    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M")

    log_file = open("./logs/backup_manager.log", "a")
    log_file.write(f"[{current_time}] " + message + "\n")
    log_file.close()
    
if __name__ == "__main__":
    main()