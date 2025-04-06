import sqlite3

DB_FILE = r"C:\Users\lenovo\Downloads\job_screening-ai\backend\candidates.db"  # ✅ fixed

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shortlisted (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id TEXT,
            email TEXT,
            job_role TEXT,
            score REAL,
            interview_date TEXT,
            interview_time TEXT,
            meet_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_candidate(candidate_id, email, job_role, score, date, time, link):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO shortlisted (candidate_id, email, job_role, score, interview_date, interview_time, meet_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (candidate_id, email, job_role, score, date, time, link))
    conn.commit()
    conn.close()
