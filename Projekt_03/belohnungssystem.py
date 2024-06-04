#import sys
#print(sys.path)
#sys.path.append('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain')


import json
import logging

from blockchain import Blockchain
from user import User

logging.basicConfig(level=logging.DEBUG)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

def main():

    blockchain = Blockchain()
    user_data = load_data('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_02/user_data.json')
    logging.debug(user_data)
    activities = load_data('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_02/activities.json')
    logging.debug(activities)

    # Liste von User-Objekten erstellen
    users = [User(user['name'], user['role'],user.get('coins', 0)) for user in user_data]
    logging.debug(f"Users: {users}")

    while True:
        print("1. Neue Aktivität hinzufügen")
        print("2. Aktivitäten anzeigen und die Aktivität durchführen")
        print("3. Blockchain anzeigen")
        print("4. Offene Transaktionen anzeigen")
        print("5. Bestätigen einer Aktivität")
        print("6. Beenden")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            new_activity = input("Neue Activität eingeben: ")
            coins = input("Wie viele Coins bekommt man für die Aktivität?: ")

            activities.append({"name": new_activity, "coins": int(coins)})
            save_data(activities,'/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_02/activities.json')

        elif choice == '2':
        
            user_name = input("Benutzername: ")
            user = next((u for u in users if u.name == user_name), None)
            if not user:
                print("Benutzer nicht gefunden.")
                continue

            print("Verfügbare Aktivitäten:")
            for activity in activities:
                print(f"{activity['name']}: {activity['coins']} Coins")

            activity_name = input("Aktivität wählen: ")
            activity = next((act for act in activities if act['name'] == activity_name), None)
            if not activity:
                print("Aktivität nicht gefunden.")
                continue
            # Variable coins initialisieren
            coins = activity['coins']
   
            # Sammle alle Eltern, aber schließe den aktuellen Benutzer aus, wenn er ein Elternteil ist
            parents = [u.name for u in users if u.role == "parent" and u.name != user.name]

            logging.debug(f"Eltern: {parents}") 
            logging.debug(f"{parents},{len(parents)}")
            
            
            if len(parents) == 0:
                print("Keine Eltern vorhanden, um die Aktivität zu evaluieren.")
                continue
            elif len(parents) == 1:
                evaluater = parents[0]
                print(f"Der Prüfer der Aktivität ist {evaluater}.")
            else:
                evaluater = input(f"Wer soll deine Aktivität evaluieren? Wähle einen Namen aus: {', '.join(parents)} ")
          

            blockchain.new_transaction(user, activity_name, activity['coins'],evaluater)
            proof = blockchain.proof_of_authority(user,activity_name, coins, evaluater)
            blockchain.create_block(proof)

            user.add_activity(activity_name,activity['coins'])
            print(f"{activity['coins']} Coin\(s\) wurden {user.name} gutgeschrieben für {activity_name}.")

        elif choice == '3':
            for block in blockchain.chain:
                print(json.dumps(block, indent=4))
        
        elif choice == '4':
            unconfirmed_transactions = blockchain.list_unconfirmed_transactions()
            if not unconfirmed_transactions:
                print("Keine offenen Transaktionen.")
            else:
                print("Offene Transaktionen:")
                for transaction in unconfirmed_transactions:
                    print(f"Timestamp: {transaction['timestamp']}, User: {transaction['user']}, Activity: {transaction['activity']}, Coins: {transaction['coins']}, Approver: {transaction['approver']}")
        
        elif choice == '5':
            approver_name = input("Name des Prüfers: ")
            transaction_id = float(input("Transaktions-ID (Timestamp): "))

            if blockchain.confirm_transaction(transaction_id, approver_name):
                print("Transaktion wurde bestätigt.")
            else:
                print("Transaktion nicht gefunden oder nicht berechtigt.")

        elif choice == '6':
            break

if __name__ == "__main__": #Das bedeutet, dass die Funktion main() nur ausgeführt wird, wenn belohnungssystem.py direkt ausgeführt wird,
                           # und nicht, wenn es als Modul in einem anderen Skript importiert wird.
    main()
