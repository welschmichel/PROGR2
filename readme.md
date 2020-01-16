## Ausgangslage
Ein DBM-Student hat während dem Unterricht ständig seinen Laptop offen und schreibt Notizen. Dabei kann es vorkommen, dass ihm wichtige Dinge in den Sinn kommen, welche er später zu erledigen hat. Um diese flüchtigen Ideen und Erinnerungen nicht wieder zu vergessen, braucht es ein System. 

## Funktion/Projektidee
Die Webapplikation soll dem Anwender ermöglichen, seine Erinnerung in textlicher Form zu erfassen und sie zu terminieren. Diese Erinnerungen / Reminder bestehen aus der Notiz, einem Datum (Fälligkeit) und der dafür verantwortlichen Person. Die Applikation setzt sich aus drei Teilen zusammen. 

 - Notiz erfassen
 - Notiz einsehen
 - Notiz löschen

## Installation / Voraussetzungen

- `python` / `flask` / `jinja2` / `gspread` / `oauth2client`
- Damit die Applikation verwendet werden kann, muss im Ordner /static eine Datei - `client_secret.json` - abgelegt werden. Diese Datei muss den Serviceaccount (Private Key, Client-ID etc.) enthalten, welche für den Zugriff auf das spreadsheet berechtigt ist.

## Anleitung

 - Die Notizen werden durch die Applikation in ein [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit#gid=152787366) abgelegt und sind somit von überall zugänglich.
 - Das Spreadsheet ist für alle zugänglich (read-only).
 - Die Notiz kann aus max. 40 Zeichen bestehen.
 - Die maximale Anzahl Notizen beträgt 200.
 - Die maximale Anzahl Notizen kann auf Zeile 33 und 50 in libs/gapi.py `worksheet.update_acell('E1', '=ANZAHL2(A1:A200)')` geändert werden. 
 - Die Applikation funktioniert nur, wenn Google Drive verfügbar ist (Offline, Firewall etc.).
 - Die Applikation bezieht bootstrap über das CDN. Falls das CDN nicht erreichbar ist -> Darstellung mangelhaft.

## Workflow

![Workflow](https://github.com/welschmichel/PROGR2/blob/master/workflow/wf.png)
