import sys, os, sqlite3
sys.path.insert(0, os.getcwd())
from config.settings import DB_FILE
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)
for t in tables:
    cur.execute(f'SELECT COUNT(*) FROM {t}')
    count = cur.fetchone()[0]
    print(f'  {t}: {count} rows')
conn.close()
