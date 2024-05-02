BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS "sessions" (
        "expire"	INTEGER,
        "csrf"	TEXT UNIQUE,
        "name"	TEXT,
        "login_true"	INTEGER,
        "session_id"	TEXT NOT NULL
    );
COMMIT;