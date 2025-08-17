#!/usr/bin/env python3
import os
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def backup_database():
    db_path = "frc_components.db"
    if os.path.exists(db_path):
        shutil.copy2(db_path, "frc_components.db")
        try:
            subprocess.run(["git", "add", "frc_components.db"], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-backup database"], check=True)
            subprocess.run(["git", "push"], check=True)
            logging.info("Database backed up to GitHub")
        except subprocess.CalledProcessError:
            logging.warning("Git backup failed (might be no changes)")

if __name__ == "__main__":
    backup_database()
