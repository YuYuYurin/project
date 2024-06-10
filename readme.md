
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
- Implementierung der Webanwendung mit Flask
- Anpassung der Logik, wann neuer Block erstellt wird.

'''Zeitgesteuerte Blockerstellung
Ein neuer Block wird in regelmäßigen Zeitintervallen erstellt, z.B. alle 24 Stunden, unabhängig davon, wie viele Transaktionen vorliegen.

Vorteile:

Einfach und vorhersehbar.
Ermöglicht eine regelmäßige Überprüfung und Erstellung von Blöcken.

Nachteile:

Möglicherweise werden leere Blöcke erstellt, wenn keine neuen Transaktionen vorliegen.'''