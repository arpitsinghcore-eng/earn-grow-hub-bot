import shutil
import time

def backup_db():
    timestamp = int(time.time())
    shutil.copy("database.db", f"database_backup_{timestamp}.db")
