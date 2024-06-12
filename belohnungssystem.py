from flask import Flask, render_template, request, redirect, url_for, jsonify
from blockchain import Blockchain
from transaction import Transaction
from user import User
import json
from flask import jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
blockchain = Blockchain()

with open('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_04/user_data.json', 'r', encoding='utf-8') as file:
    user_data = json.load(file)

with open('/home/yuri/Dokumente/Weiterbildung_2023/BlockChain/Projekt_04/activities.json', 'r', encoding='utf-8') as file:
    activities = json.load(file)

users = [User(user['name'], user['role'], user.get('coins', 0)) for user in user_data]

@app.route('/')
def index():
    return render_template('index.html', users=users, activities=activities) 
    # render_template() wird in Flask wird verwendet, um HTML-Vorlagen zu rendern und 
    # dynamisch Inhalte in diese Vorlagen einzufügen.
    # Hier wird die Datei "index-html" gerendert
    # "usesrs" und "activities" werden an die Vorlage übergeben

@app.route('/add_activity', methods=['POST'])
def add_activity():
    new_activity = request.form['activity']
    coins = int(request.form['coins'])
    activities.append({"name": new_activity, "coins": coins})
    with open('activities.json', 'w', encoding='utf-8') as file:
        json.dump(activities, file, ensure_ascii=False, indent=4)
        logging.debug(f"new activity is added: {activities}")
    return redirect(url_for('index'))

@app.route('/perform_activity', methods=['POST'])
def perform_activity():
    username = request.form['username']
    activity_name = request.form['activity']

    user = next((u for u in users if u.name == username), None)
    if not user:
        error = "der Benutzer wurde nicht gefunden"
        return render_template('index.html', users=users, activities=activities, error=error)
    activity = next((act for act in activities if act['name'] == activity_name), None)
    if not activity:
        error = "Aktivität nicht gedfunden"
        return render_template('index.html', users=users, activities=activities, error=error)
    
    coins = activity['coins']
    
    parents = [u.name for u in users if u.role == "parent"]
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
    logging.debug(f"pending_transactions: {blockchain.pending_transactions}")

    user.add_activity(activity_name, coins)
    logging.debug(f"activity is added in perform_activity(). User: {user}")
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
@app.route('/confirmed_transactions')
def confirmed_transactions():
    return redirect(url_for('confirmed_transactions_page'))

@app.route('/api/confirmed_transactions')
def api_confirmed_transactions():
    transactions = blockchain.list_confirmed_transactions()
    logging.debug(f"confirmed_transactions: {transactions}")
    return jsonify(transactions)

@app.route('/confirmed_transactions_page')
def confirmed_transactions_page():
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
        return redirect(url_for('confirmed_transactions'))
    return "Transaction not found or not authorized", 400


if __name__ == "__main__":
    app.run(debug=True)