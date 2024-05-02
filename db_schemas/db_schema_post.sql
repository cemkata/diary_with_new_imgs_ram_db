BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categories_tbl" (
	"id"	INTEGER NOT NULL UNIQUE,
	"style"	TEXT,
	"text"	TEXT,
	"catid"	INTEGER,
	"order"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id"),
	FOREIGN KEY("catid") REFERENCES "categories_tbl"("id")
);
CREATE TABLE IF NOT EXISTS "day_content_tbl" (
	"date_day"	INTEGER NOT NULL,
	"date_month"	INTEGER NOT NULL,
	"date_year"	INTEGER NOT NULL,
	"cat_id"	INTEGER NOT NULL,
	"table_row_number"	INTEGER NOT NULL,
	"style"	TEXT,
	"text"	TEXT,
	FOREIGN KEY("cat_id") REFERENCES "categories_tbl"("id")
);
CREATE TABLE IF NOT EXISTS "post_tbl" (
	"id"	INTEGER NOT NULL UNIQUE,
	"year"	INTEGER,
	"month"	INTEGER,
	"day"	INTEGER,
	"content"	TEXT,
	"title"	TEXT,
	"hidden"	INTEGER
);
CREATE TABLE IF NOT EXISTS "files_tbl" (
	"os_file_path"	TEXT NOT NULL,
	"userFriendlyName"	TEXT NOT NULL,
	"postID"	INTEGER NOT NULL,
	"id"	INTEGER NOT NULL UNIQUE,
	"timeStamp"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
