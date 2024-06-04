import json
import logging
from blockchain import Blockchain
from user import User

'''
Implementiertung PoW
'''
logging.basicConfig(level=logging.DEBUG)

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

def main():

    blockchain = Blockchain()
    users = load_data('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_01/users.json')
    logging.debug(users)
    activities = load_data('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_01/activities.json')
    logging.debug(activities)
    while True:
        print("1. Neue Aktivität hinzufügen")
        print("2. Aktivitäten anzeigen und die Aktivität durchführen")
        print("3. Blockchain anzeigen")
        print("4. Beenden")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            new_activity = input("Neue Activität eingeben: ")
            coins = input("Wie viele Coins bekommt man für die Aktivität?: ")

            activities.append({"name": new_activity, "coins": int(coins)})
            save_data(activities,'/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_01/activities.json')

        elif choice == '2':
        
            user = input("Benutzername: ")
            user_names = [u["name"] for u in users]
            if user not in user_names:
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

            blockchain.new_transaction(user, activity_name, activity['coins'])
            proof = blockchain.proof_of_work(blockchain.last_block['proof'])
            blockchain.new_block(proof)
            user.activities.append()

            print(f"{activity['coins']} Coins wurden {user} gutgeschrieben für {activity_name}.")

        elif choice == '3':
            for block in blockchain.chain:
                print(json.dumps(block, indent=4))

        elif choice == '4':
            break

if __name__ == "__main__": #Das bedeutet, dass die Funktion main() nur ausgeführt wird, wenn belohnungssystem.py direkt ausgeführt wird,
                           # und nicht, wenn es als Modul in einem anderen Skript importiert wird.
    main()
