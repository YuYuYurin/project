CREATE TABLE IF NOT EXISTS `user` (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	role TEXT NOT NULL CHECK(role IN ('PARENT', 'CHILD')) DEFAULT 'CHILD',
	current_points INTEGER DEFAULT 0
	);

CREATE TABLE IF NOT EXISTS `activity` (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	activity_name TEXT NOT NULL,
	points INTEGER DEFAULT 1
	);

CREATE TABLE IF NOT EXISTS pending_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity_id INTEGER,
    points INTEGER,
    approver TEXT,
    transaction_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY(activity_id) REFERENCES activity(id) ON UPDATE CASCADE
    );
    

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity_id INTEGER,
    approver TEXT,
    points INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,            
    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
    FOREIGN KEY(activity_id) REFERENCES activity(id) ON UPDATE CASCADE
	);  
	

	
	
	
	
