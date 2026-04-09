import sys

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
    print(schedule)

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
    

if __name__ == "__main__":
    main()