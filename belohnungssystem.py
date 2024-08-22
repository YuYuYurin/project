from flask import Flask, render_template, request, redirect, url_for, jsonify
from blockchain import Blockchain
from transaction import Transaction
from user import User
from flask import jsonify
import logging
from datenbank import Datenbank

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
blockchain = Blockchain()
db = Datenbank('/home/yuri/Dokumente/Weiterbildung_2023/SQLite.db')

# Laden der Benutzer und Aktivitäten aus der Datenbank
users = [User(user[1], user[2], user[3]) for user in db.fetch_users()]
logging.debug(f"users: {users}")

activities = [{"activity name": act[1], "coins": act[2]} for act in db.fetch_activities()]
logging.debug(f"activities: {activities}")

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form['name']
        role = request.form['role']
        db.insert_user(new_user_name, role)  # In Datenbank einfügen
        logging.debug(f"new_user: {new_user_name}, role: {role} is added in the db")
        return redirect(url_for('add_user'))

    # GET-Anfrage: Benutzer anzeigen
    users = db.fetch_users()  # Alle Benutzer abfragen

    if not users:  # Wenn die Benutzerliste leer ist
        logging.debug("No users found in the database")
        return render_template('add_user.html', users=[], message="Noch keine Benutzer vorhanden. Fügen Sie einen neuen Benutzer hinzu.")
    return render_template('add_user.html', users=users)



@app.route('/')
def index():
    # Laden erneut der Benutzer aus der Datenbank, da ein neuer User hinzugefügt werden kann
    users = [User(user[1], user[2], user[3]) for user in db.fetch_users()]
    return render_template('index.html', users=users, activities=activities) 
    # render_template() wird in Flask wird verwendet, um HTML-Vorlagen zu rendern und 
    # dynamisch Inhalte in diese Vorlagen einzufügen.
    # Hier wird die Datei "index-html" gerendert
    # "usesrs" und "activities" werden an die Vorlage übergeben

@app.route('/add_activity', methods=['POST'])
def add_activity():
    new_activity = request.form['activity']
    coins = int(request.form['coins'])
    db.insert_activity(new_activity, coins)  # In Datenbank einfügen
    return redirect(url_for('index'))

@app.route('/perform_activity', methods=['POST'])
def perform_activity():
    username = request.form['username']
    activity_name = request.form['activity']

    user = next((u for u in users if u.name == username), None)
    if not user:
        error = "der Benutzer wurde nicht gefunden"
        return render_template('index.html', users=users, activities=activities, error=error)
    
    activity = next((act for act in activities if act['activity name'] == activity_name), None)
    if not activity:
        error = "Aktivität nicht gedfunden"
        return render_template('index.html', users=users, activities=activities, error=error)
    
    coins = activity['coins']
    
    parents = [u.name for u in users if u.role == "PARENT"]
    logging.debug(f"Parents: {parents}, Username: {username}")

    if not parents:
        error = "Keine Eltern zur Evaluierung vorhanden"
        return render_template('index.html', users=users, activities=activities, error=error)
    
    if len(parents) == 1:
        approver = parents[0]
        logging.debug(f"Single parent, approver: {approver}")
    elif len(parents) > 1:
        approver = request.form['approver']
        logging.debug(f"Multiple parents, selected approver: {approver}")
        if approver == username:
            logging.debug("Error: der Prüfer muss eine andere Person als Benutzer sein")
            return render_template('index.html', users=users, activities=activities, error="Error: der Prüfer soll eine andere Person als Benutzer sein")
    else:
        logging.debug("Unexpected error: No parents available")
        return render_template('index.html', users=users, activities=activities, error="Unerwarteter Error") 
    
    new_transaction = Transaction(user.name, activity_name, coins, approver)
    blockchain.pending_transactions.append(new_transaction)
    logging.debug(f"blockchain.pending_transactions: {blockchain.pending_transactions}")
    user_id = db.get_user_id_by_name_pending_transactions(user.name)
    activity_id = db.get_activity_id_by_name_pending_transactions(activity_name)
    db.insert_pending_transaction(user_id, activity_id, coins, approver,new_transaction.timestamp)
    logging.debug(f"new_pending_transaction added in db")


    
    return redirect(url_for('index'))


@app.route('/unconfirmed_transactions')
def unconfirmed_transactions():
    transactions = blockchain.list_unconfirmed_transactions()
    logging.debug(f"unconfirmed_transactions: {transactions}")
    return jsonify(transactions)


"""
- /confirmed_transactions: Diese Route leitet zur neuen Seite /confirmed_transactions_page weiter.
- /api/confirmed_transactions: Diese Route liefert die bestätigten Transaktionen im JSON-Format.
- /confirmed_transactions_page: Diese Route rendert das HTML-Template, das die bestätigten Transaktionen von der API abruft und anzeigt.

"""

@app.route('/api/confirmed_transactions')
def api_confirmed_transactions():
    transactions = blockchain.list_confirmed_transactions()
    logging.debug(f"confirmed_transactions: {transactions}")
    return jsonify(transactions)

@app.route('/confirmed_transactions')
def confirmed_transactions():
    return render_template('confirmed_transactions.html')

@app.route('/confirm_transaction', methods=['POST'])
def confirm_transaction():
    approver_name = request.form['approver']
    transaction_id = request.form['transaction_id']
    logging.debug(f"Received transaction_id: {transaction_id}") 

    if not transaction_id:
        return "Invalid transaction ID", 400
    
    try:
        transaction_id = float(transaction_id)
    except ValueError:
        logging.error(f"ValueError: Cannot convert {transaction_id} to float")
        return "Invalid transaction ID format", 400

    if blockchain.confirm_transaction(transaction_id, approver_name):
        user_id = db.get_user_id_by_transaction_id(transaction_id)
        activity_id = db.get_activity_id_by_transaction_id(transaction_id)
        coins = db.get_coins_by_transaction_id(transaction_id)
        db.insert_history(user_id, activity_id, coins, approver_name)
        logging.debug(f"new confirmed transaction is added in the db history")
        db.delete_pending_transaction(transaction_id)
        logging.debug(f"this transaction with {transaction_id} is deleted from the db pending_transactions")

        # User bekommt die Belohnungspunkte
        user_name = db.get_user_name_by_transaction_id(transaction_id)
        user = next((u for u in users if u.name == user_name), None)
        if user:
            user.add_coins(coins)
            logging.debug(f"coins is added to the user: {user.name} has currently {user.coins} coins")
            db.update_usercoins(user_id, user.coins)
            logging.debug(f"coins of {user} in db user is updated")

        else:
                logging.error(f"User with name {user_name} not found")

        return redirect(url_for('confirmed_transactions'))
    
    return "Transaction not found or not authorized", 400


if __name__ == "__main__":
    app.run(debug=True)