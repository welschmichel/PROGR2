import json
from datetime import date
import datetime

def termin_speichern(notiz, single_date):
    
    json_daten = load_json()
    alle_termine = json_daten.get("notiz", {})
        
    termin = {
        "Notiz": notiz,
        "Datum": single_date,
    }
        
    alle_termine[category][str(datetime.datetime.now())] = single_date
        
    json_daten["notiz"] = alle_termine

    save_to_json(json_daten)
    return json_daten                        #Json-Datei mit neuer Eingabe wird zurückgegeben

def get_events_from_now(termin_daten):
    now = datetime.datetime.combine(date.today(),datetime.datetime.now().time())

    filtered_events = {}
    for key, value in termin_daten.items():
        datetime_string = value['date'] + " " + value['time']
        event_datetime = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')

        if event_datetime >= now:
            filtered_events[key] = value

    return filtered_events


def load_json():
    json_daten = {}
    try:
        with open('data/data.json') as open_file:    #Json-Datei öffnen/lesen
            json_daten = json.load(open_file)
    
    except FileNotFoundError:                       #wenn json.datei noch leer ist     
        print("File not found")

    return json_daten

def save_to_json(daten):
    with open('data/data.json', "w", encoding="utf-8") as open_file:
        json.dump(daten, open_file)


