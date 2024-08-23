import sqlite3
import logging

class Datenbank:
    logging.basicConfig(level=logging.INFO)

    def __init__(self, db_path, sql_script_path):
        """Initialisiert die Verbindung zur Datenbank."""
        self.db_path = db_path
        self.sql_script_path = sql_script_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Stellt eine Verbindung zur SQLite-Datenbank her."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            logging.info(f"Verbindung zur Datenbank {self.db_path} erfolgreich hergestellt.")
        except sqlite3.Error as e:
            logging.error(f"Fehler bei der Verbindung zur Datenbank: {e}")
    
    def create_tables(self):
        """Erstellt die 4 Tabellen in der Datenbank."""
        try:
            with open(self.sql_script_path, 'r') as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.conn.commit()
                logging.info("Tabellen erfolgreich erstellt.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Erstellen der Tabellen: {e}")
        except FileNotFoundError as e:
            logging.error(f"Fehler: SQL-Skriptdatei nicht gefunden: {e}")
        except Exception as e:
            logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    def insert_user(self, username, role):
        """Fügt einen neuen Benutzer hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO user (username, role) VALUES (?, ?)
            ''', (username, role))
            self.conn.commit()
            logging.info(f"Benutzer {username} erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Hinzufügen des Benutzers: {e}")

    def insert_activity(self, activity_name, points):
        """Fügt eine neue Aktivität hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO activity (activity_name, points) VALUES (?, ?)
            ''', (activity_name, points))
            self.conn.commit()
            logging.info(f"Aktivität {activity_name} erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Hinzufügen der Aktivität: {e}")


    def insert_pending_transaction(self, user_id, activity_id, points, approver,transaction_id):
        """Fügt eine ausstehende Transaktion hinzu."""
        try:
            self.cursor.execute('''
                INSERT INTO pending_transactions (user_id, activity_id, points, approver, transaction_id) VALUES (?, ?, ?, ?, ?)
            ''', (user_id, activity_id, points, approver, transaction_id))
            self.conn.commit()
            logging.info(f"Ausstehende Transaktion erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Hinzufügen der Transaktion: {e}")


    def insert_history(self, user_id, activity_id, points, approver):
        """Speichert die Historie einer durchgeführten Aktivität."""
        try:
            self.cursor.execute('''
                INSERT INTO history (user_id, activity_id, points, approver) VALUES (?, ?, ?, ?)
            ''', (user_id, activity_id, points, approver))
            self.conn.commit()
            logging.info(f"bestätigte Transaktion erfolgreich gespeichert.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Speichern der Historie: {e}")


    def delete_user(self, username):
        """Löscht einen Benutzer aus der Datenbank."""
        try:
            self.cursor.execute('''
                DELETE FROM user WHERE username = ?
            ''', (username,))
            self.conn.commit()
            logging.info(f"Benutzer {username} erfolgreich gelöscht.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Löschen des Benutzers: {e}")

    def delete_activity(self, activity_name):
        """Löscht eine Aktivität aus der Datenbank."""
        try:
            self.cursor.execute('''
                DELETE FROM activity WHERE activity_name = ?
            ''', (activity_name,))
            self.conn.commit()
            logging.info(f"Aktivität {activity_name} erfolgreich gelöscht.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Löschen der Aktivität: {e}")

    def delete_pending_transaction(self, transaction_id):
        """Löscht die bestätigteTransaktion aus der Tabelle pending_transactions."""
        try:
            self.cursor.execute('''
                DELETE FROM pending_transactions WHERE transaction_id = ?
            ''', (transaction_id,))
            self.conn.commit()
            logging.info(f"Ausstehende Transaktion erfolgreich gelöscht.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Löschen der Ausstehenden Transaktion: {e}")

    def delete_history(self, user_id, activity_id):
        """Löscht die Historie einer durchgeführten Aktivität."""
        try:
            self.cursor.execute('''
                DELETE FROM history WHERE user_id = ? AND activity_id = ?
            ''', (user_id, activity_id))
            self.conn.commit()
            logging.info(f"Historie erfolgreich gelöscht.")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Löschen der Historie: {e}")

    def get_user_id_by_name_pending_transactions(self, user_name):
        try:
            self.cursor.execute('''SELECT id FROM user WHERE username = ?
            ''', (user_name,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"User-ID für {user_name} erfolgreich abgerufen. User-ID: {result[0]}")
                return result[0]
            else:
                logging.info(f"User-ID für {user_name} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der User-ID: {e}")

    def get_activity_id_by_name_pending_transactions(self, activity_name):
        try:
            self.cursor.execute('''SELECT id FROM activity WHERE activity_name = ?
            ''', (activity_name,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"Activity-ID für {activity_name} erfolgreich abgerufen. Activity-ID: {result[0]}")
                return result[0]
            else: 
                logging.info(f"Activity-ID für {activity_name} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der Activity-ID: {e}")
    
    def get_user_id_by_transaction_id(self, transaction_id):
        try:
            self.cursor.execute('''SELECT user_id FROM pending_transactions WHERE transaction_id = ?
            ''', (transaction_id,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"User-ID für {transaction_id} erfolgreich abgerufen. User-ID: {result[0]}")
                return result[0]
            else:
                logging.info(f"User-ID für {transaction_id} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der User-ID: {e}")
    
    def get_activity_id_by_transaction_id(self, transaction_id):
        try:
            self.cursor.execute('''SELECT activity_id FROM pending_transactions WHERE transaction_id = ?
            ''', (transaction_id,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"Activity-ID für {transaction_id} erfolgreich abgerufen. Activity-ID: {result[0]}")
                return result[0]
            else: 
                logging.info(f"Activity-ID für {transaction_id} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der Activity-ID: {e}")
    
    def get_coins_by_transaction_id(self, transaction_id):
        try:
            self.cursor.execute('''SELECT points FROM pending_transactions WHERE transaction_id = ?
            ''', (transaction_id,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"Coins für {transaction_id} erfolgreich abgerufen. Coins: {result[0]}")
                return result[0]
            else:
                logging.info(f"Coins für {transaction_id} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der Coins: {e}")
        
    def get_user_name_by_transaction_id(self, transaction_id):
        try:
            self.cursor.execute('''
                SELECT u.username
                FROM pending_transactions pt
                JOIN user u ON u.id = pt.user_id
                WHERE pt.transaction_id = ?
            ''', (transaction_id,))
            result = self.cursor.fetchone()
            if result:
                logging.info(f"User-Name für {transaction_id} erfolgreich abgerufen. User-Name: {result[0]}")
                return result[0] 
            else:
                logging.info(f"User-Name für {transaction_id} nicht gefunden.")
                return None
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen des User-Names: {e}")

    
    def update_usercoins(self, user_id, coins):
        try:
            self.cursor.execute('''UPDATE user SET current_points = ? WHERE id = ?
            ''', (coins, user_id))
            self.conn.commit()
            logging.info(f"Coins für {user_id} erfolgreich aktualisiert. Coins: {coins}")
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Aktualisieren der Coins: {e}")

    def fetch_users(self):
        try:
            self.cursor.execute('''SELECT * FROM user ''')
            result = self.cursor.fetchall()
            logging.info(f"fetch users: {result}")
            if result:
                logging.info(f"fetch_users() erfolgreich abgerufen: {result}")
                return result  
            else:
                logging.info(f"Benutzer nicht gefunden.")
                return []
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der Benutzer: {e}")
    
    def fetch_activities(self):
        try:
            self.cursor.execute('''SELECT * FROM activity ''')
            result = self.cursor.fetchall()
            if result:
                logging.info(f"fetch_activities() erfolgreich abgerufen: {result}")
                return result  
            else: 
                logging.info(f"Aktivität nicht gefunden.")
                return []
        except sqlite3.Error as e:
            logging.error(f"Fehler beim Abrufen der Aktivität: {e}")
    

    def close(self):
        """Schließt die Datenbankverbindung."""
        if self.conn:
            self.conn.close()
            logging.info("Datenbankverbindung geschlossen.")
