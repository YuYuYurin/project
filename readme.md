
# Belohnungssystem Version 04

## Projektstruktur

belohnungssystem/
├── belohnungssystem.py
├── blockchain.py
├── templates/
│   └── index.html
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

## Todo
- Probelm mit der falschen Darstellung der Umlaute auf der Seite http://127.0.0.1:5000/confirmed_transactions beheben

## Memo (Nice to have)
'''Zeitgesteuerte Blockerstellung
Ein neuer Block wird in regelmäßigen Zeitintervallen erstellt, z.B. alle 24 Stunden, unabhängig davon, wie viele Transaktionen vorliegen.

Vorteile:

Einfach und vorhersehbar.
Ermöglicht eine regelmäßige Überprüfung und Erstellung von Blöcken.

Nachteile:

Möglicherweise werden leere Blöcke erstellt, wenn keine neuen Transaktionen vorliegen.'''