
# Belohnungssystem Version 04

## Projektstruktur

belohnungssystem/
├── belohnungssystem.py
├── blockchain.py
├── templates/
│   └── index.html
│   └── confirmed_transactions.html
├── static/ css
│   └── styles.css
├── user.py
├── transaction.py
├── activities.json
└── user_data.json


## Ideen
- App "Belohnungssystem" 
- Innerhalb der Familie einzusetzen
- eine private Blockchain wird verwendet, um die Nachverfolgbarkeit der Coins zu gewährleisten

## Änderungen
- Wenn es nur einen Elternteil gibt, wird dieser als approver gesetzt.
- Wenn es mehr als einen Elternteil gibt, wird der approver aus dem Formular entnommen. Dabei wird überprüft, dass der approver nicht derselbe wie der Benutzer ist.

- confirmed_transactions.html wurde hinzugefügt 
- Probelm mit der falschen Darstellung der Umlaute auf der Seite http://127.0.0.1:5000/confirmed_transactions wurde behoben 

- proof-Wert in Blockchain wurde entfernt, da PoA als Konsensalgorithmus gewählt wurde
- Neuer Block wird erstellt, wenn die bestätigten Transaktionen > 5 wird

