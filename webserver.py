from flask import Flask, render_template, request, url_for, jsonify, json
import gspread
import calendar;
import time;
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# app_main_path = Path(os.path.abspath("/".join(os.path.realpath(__file__).split("/")[:-1])))
# data_path = Path(os.path.abspath(app_main_path / "data"))
# data_storage_file = data_path / "test.json"

# Master Route definiert und erste Ausgabe auf Website
@app.route('/ok')
def welcome():
    return 'Webserver erfolgreich gestartet (debug=True, port=5000).'



@app.route('/', methods=["POST", "GET"])
def index():
	return render_template("header.html")

@app.route('/input', methods=["POST", "GET"])
def input():
	if request.method=='POST':
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']
		#Name des credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification
		### --- START--- open Google Spreadsheet & Counter-Value
		worksheet = gc.open("notizen").sheet1
		val = worksheet.acell('B1').value

		### --- START--- request the input-values
		notiz=request.form['notiz']
		date=request.form['date']
		notiz = notiz.capitalize()

		### --- START--- change cell-value 'B1' from str to int and ++ || Needed for placing the note in the right cell
		val = int(val)
		val = val + 1
		### create timestamp to save with the note || it's also an unique id for every note
		ts = calendar.timegm(time.gmtime())

		### --- START--- store the input-values in the spreadsheet
		worksheet.update_acell('B1', val)
		worksheet.update_acell('D'+str(val), notiz)
		worksheet.update_acell('C'+str(val), ts)
		worksheet.update_acell('E'+str(val), date)
		### --- END--- store the input-values in the spreadsheet
		
		return render_template("input.html", notiz=notiz, date=date)
	else:
		
		return render_template("input.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)


