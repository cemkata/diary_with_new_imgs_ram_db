BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users_tbl" (
	"id"	INTEGER NOT NULL UNIQUE,
	"fname"	TEXT,
	"lname"	TEXT,
	"user_name"	TEXT  NOT NULL UNIQUE,
	"email"	TEXT,
	"salt"	TEXT  NOT NULL,
	"passchecksum"	TEXT  NOT NULL,
	PRIMARY KEY("id")
);
COMMIT;