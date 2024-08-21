import sqlite3
import logging

class Datenbank:
    def __init__(self, db_path):
        """Initialisiert die Verbindung zur Datenbank."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"Verbindung zur Datenbank {self.db_path} erfolgreich hergestellt.")
        except sqlite3.Error as e:
            print(f"Fehler bei der Verbindung zur Datenbank: {e}")
    
    def create_tables(self):
        """Erstellt die notwendigen Tabellen."""
        try:
            # Tabelle "user"
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('PARENT', 'CHILD')) DEFAULT 'CHILD',
                current_points INTEGER DEFAULT 0
                )
            ''')

            # Tabelle "activity"
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity_name TEXT NOT NULL,
                    points INTEGER NOT NULL
                )
            ''')

            # Tabelle "pending_transactions"
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pending_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    activity_id INTEGER,
                    points INTEGER,
                    approver TEXT,
                    transaction_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
                    FOREIGN KEY(activity_id) REFERENCES activity(id) ON UPDATE CASCADE
                )
            ''')



            # Tabelle "history"
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    activity_id INTEGER,
                    points INTEGER,
                    approver TEXT,
                    transaction_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON UPDATE CASCADE,
                    FOREIGN KEY(activity_id) REFERENCES activity(id) ON UPDATE CASCADE
                )
            ''')
            self.conn.commit()
            print("Tabellen erfolgreich erstellt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Erstellen der Tabellen: {e}")

    def insert_user(self, username, role):
        """Fügt einen neuen Benutzer hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO user (username, role) VALUES (?, ?)
            ''', (username, role))
            self.conn.commit()
            print(f"Benutzer {username} erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen des Benutzers: {e}")

    def insert_activity(self, activity_name, points):
        """Fügt eine neue Aktivität hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO activity (activity_name, points) VALUES (?, ?)
            ''', (activity_name, points))
            self.conn.commit()
            print(f"Aktivität {activity_name} erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen der Aktivität: {e}")


    def insert_pending_transaction(self, user_id, activity_id, points, approver,transaction_id):
        """Fügt eine ausstehende Transaktion hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO pending_transactions (user_id, activity_id, points, approver, transaction_id) VALUES (?, ?, ?, ?, ?)
            ''', (user_id, activity_id, points, approver, transaction_id))
            self.conn.commit()
            print(f"Ausstehende Transaktion erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen der Transaktion: {e}")


    def insert_history(self, user_id, activity_id, points, approver):
        """Speichert die Historie einer durchgeführten Aktivität."""
        try:
            self.cursor.execute('''
                INSERT INTO history (user_id, activity_id, points, approver) VALUES (?, ?, ?, ?)
            ''', (user_id, activity_id, points, approver))
            self.conn.commit()
            print(f"bestätigte Transaktion erfolgreich gespeichert.")
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern der Historie: {e}")



    def delete_user(self, username):
        """Löscht einen Benutzer aus der Datenbank."""
        try:
            self.cursor.execute('''
                DELETE FROM user WHERE username = ?
            ''', (username,))
            self.conn.commit()
            print(f"Benutzer {username} erfolgreich gelöscht.")
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen des Benutzers: {e}")

    def delete_activity(self, activity_name):
        """Löscht eine Aktivität aus der Datenbank."""
        try:
            self.cursor.execute('''
                DELETE FROM activity WHERE activity_name = ?
            ''', (activity_name,))
            self.conn.commit()
            print(f"Aktivität {activity_name} erfolgreich gelöscht.")
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Aktivität: {e}")

    def delete_pending_transaction(self, transaction_id):
        """Löscht eine ausstehende Transaktion aus der Datenbank."""
        try:
            self.cursor.execute('''
                DELETE FROM pending_transactions WHERE transaction_id = ?
            ''', (transaction_id))
            self.conn.commit()
            print(f"Ausstehende Transaktion erfolgreich gelöscht.")
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Ausstehenden Transaktion: {e}")

    def delete_history(self, user_id, activity_id):
        """Löscht die Historie einer durchgeführten Aktivität."""
        try:
            self.cursor.execute('''
                DELETE FROM history WHERE user_id = ? AND activity_id = ?
            ''', (user_id, activity_id))
            self.conn.commit()
            print(f"Historie erfolgreich gelöscht.")
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Historie: {e}")

    def get_user_id_by_name_pending_transactions(self, user_name):
        self.cursor.execute("SELECT id FROM user WHERE username = ?", (user_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_activity_id_by_name_pending_transactions(self, activity_name):
        self.cursor.execute("SELECT id FROM activity WHERE activity_name = ?", (activity_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_user_id_by_transaction_id(self, transaction_id):
        self.cursor.execute("SELECT user_id FROM pending_transactions WHERE transaction_id = ?", (transaction_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_activity_id_by_transaction_id(self, transaction_id):
        self.cursor.execute("SELECT activity_id FROM pending_transactions WHERE transaction_id = ?", (transaction_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_coins_by_transaction_id(self, transaction_id):
        self.cursor.execute("SELECT points FROM pending_transactions WHERE transaction_id = ?", (transaction_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def update_usercoins(self, user_id, coins):
        self.cursor.execute("UPDATE user SET current_points = ? WHERE id = ?", (coins, user_id))
        self.conn.commit()

    def fetch_users(self):
        self.cursor.execute("SELECT * FROM user ")
        result = self.cursor.fetchall()
        logging.debug(f"fetch users: {result}")
        return result if result else None
    
    def fetch_activities(self):
        self.cursor.execute("SELECT * FROM activity ")
        result = self.cursor.fetchall()
        return result if result else None

    def close(self):
        """Schließt die Datenbankverbindung."""
        if self.conn:
            self.conn.close()
            print("Datenbankverbindung geschlossen.")
