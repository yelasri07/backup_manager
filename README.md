# Backup Manager

## Overview

Backup Manager is a Python-based automated backup system designed to replace error-prone manual backups. It schedules and performs automated local directory backups from the command line. The system consists of a CLI manager and a background service that work together to create compressed `.tar` archives of specified directories at scheduled times, complete with structured logging and error handling.

## Features

- **Automated Scheduling:** Schedule directory backups for specific times (HH:MM).
- **Background Processing:** Runs seamlessly as a background daemon, ensuring your terminal remains free.
- **Storage Optimization:** Automatically compresses directories into `.tar` archives.
- **Comprehensive Logging:** Tracks all user commands, background actions, and errors with precise timestamps.
- **Easy Management:** Command-line interface to create, list, and delete backup schedules.

## Project Structure

```
backup-manager/
├── backup_manager.py              # CLI script for managing schedules and the background service
├── backup_service.py              # Background daemon that executes scheduled backups
├── logs/                          # Directory for log files (auto-created at runtime)
│   ├── backup_manager.log         
│   └── backup_service.log         
├── backups/                       # Directory for backup .tar files (auto-created at runtime)
├── backup_schedules.txt           # Active schedule configuration file (auto-created at runtime)
└── README.md                      # Project documentation
```

## Prerequisites

- Python 3.x
- A Unix-like operating system (Linux/macOS) is recommended for optimal `subprocess` and process management behavior.

## Usage Guide

The system is controlled entirely through `backup_manager.py`.

### 1. Managing Schedules

**Create a new schedule**

Format: `python3 backup_manager.py create "<source_path>;<HH:MM>;<backup_name>"`

```bash
python3 backup_manager.py create "test1;16:07;personal_data"
```

> **Note:** The backup name should not include the `.tar` extension; the service adds it automatically.

**List all schedules**

Displays all active schedules with their corresponding index IDs.

```bash
python3 backup_manager.py list
```

**Delete a schedule**

Removes a schedule by its index ID (starting at 0).

```bash
python3 backup_manager.py delete 0
```

### 2. Managing the Background Service

**Start the service**

Launches `backup_service.py` as a detached background process.

```bash
python3 backup_manager.py start
```

**Stop the service**

Safely kills the running backup background process.

```bash
python3 backup_manager.py stop
```

### 3. Managing Backups

**List completed backups**

Displays all `.tar` archive files successfully created and stored in the `./backups` directory.

```bash
python3 backup_manager.py backups
```

## Logging and Troubleshooting

The system maintains distinct logs for the user interface and the background service. Both logs format their entries with timestamps: `[dd/mm/yyyy hh:mm]`.

- `./logs/backup_manager.log`: Check this log to verify that your schedules were added correctly, or if you encounter errors running CLI commands (e.g., malformed schedule strings, missing files).
- `./logs/backup_service.log`: Check this log to verify that backups were successfully archived or to debug why a scheduled backup failed to execute.

## System Behavior Notes

- The background service (`backup_service.py`) loops continuously but sleeps for ~45 seconds per cycle to conserve CPU resources.
- Once a scheduled backup executes successfully, it is automatically removed from `backup_schedules.txt` to prevent duplicate runs.
