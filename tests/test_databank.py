import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datenbank import Datenbank
import logging
#  Das Test-Skript muss dieselben Abhängigkeiten erfüllen wie die Hauptanwendung.

logging.basicConfig(level=logging.DEBUG)

class Test_Datenbank(unittest.TestCase):
    def setUp(self):
        self.db = Datenbank("data.db", "/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_04/create_tables_for_belohnungssystem.sql")
        self.db.connect()
        self.db.create_tables()

    def tearDown(self):
        self.db.close()

    def test_insert_user(self):
        self.db.insert_user("Max", "CHILD")
    
    def test_insert_activity(self):
        self.db.insert_activity("Hiragana üben", 10)
    
    def test_insert_pending_transaction(self):
        self.db.insert_pending_transaction(1,1,5,"Charlie",12345)

    def test_delete_user(self):
        self.db.delete_user("Bob")
    

if __name__ == '__main__':
    unittest.main()