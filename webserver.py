from flask import Flask, render_template, request, url_for, jsonify, json, flash
from datetime import date, datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import calendar
import time
import webbrowser


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["CACHE_TYPE"] = "null"



# Master Route definiert und erste Ausgabe auf Website
@app.route('/pulse')
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
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification
		### --- START--- open Google Spreadsheet & Counter-Value
		worksheet = gc.open("notizen").sheet1
		val = worksheet.acell('E1').value

		### --- START--- request the input-values
		notiz=request.form['notiz']
		date=request.form['date']
		wer=request.form['wer']
		

		### Flash text
		flash('Die Notiz wurde erfolgreich gespeichert!')

		### --- START--- change cell-value 'B1' from str to int and ++ || Needed for placing the note in the right cell
		val = int(val)
		val = val + 1
		### create timestamp to save with the note || it's also an unique id for every note
		ts = calendar.timegm(time.gmtime())

		### --- START--- store the input-values in the spreadsheet
		#worksheet.update_acell('B1', val)
		worksheet.update_acell('A'+str(val), ts)
		worksheet.update_acell('B'+str(val), notiz)
		worksheet.update_acell('C'+str(val), date)
		worksheet.update_acell('D'+str(val), wer)
		### --- END--- store the input-values in the spreadsheet
		
		### Output date in correct format
		date=worksheet.acell('C'+str(val)).value

		return render_template("input.html", notiz=notiz, date=date, wer=wer)
	else:
		
		return render_template("input.html")

@app.route('/output', methods=["POST", "GET"])
def output():
	### --- START--- Google Spreadsheet Authentification
	scope = ['https://www.googleapis.com/auth/drive']
	### Google Spreadsheet URL
	gs_url = 'https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit?usp=sharing'
	#Name des credential-Files
	credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
	gc = gspread.authorize(credentials)
	### --- END--- Google Spreadsheet Authentification
	### --- START--- open Google Spreadsheet & Counter-Value
	worksheet = gc.open("notizen").sheet1

	id_list = worksheet.col_values(1)
	notes_list = worksheet.col_values(2)
	date_list = worksheet.col_values(3)
	wer_list = worksheet.col_values(4)
	
	# export_file = worksheet.export(format='xlsx')
	# f = open('notes.xlsx', 'wb')
	# f.write(export_file)
	# f.close()

	return render_template("output.html", notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list, gs_url=gs_url)



@app.route('/delete', methods=["POST", "GET"])
def delete():
	if request.method=='POST':
		nummer=request.form['nummer']
		#nummer = int(nummer)
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']
		#Name des credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification
		### --- START--- open Google Spreadsheet & Counter-Value
		worksheet = gc.open("notizen").sheet1

		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		
		val = worksheet.acell('E1').value
		
		# for deleting a row
		cell = worksheet.find(nummer)
		worksheet.delete_row(cell.row)
		flash('Die Notiz wurde erfoglreich gelöscht!')

		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		
		return render_template("delete.html", notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)

	else:
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']
		#Name des credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification
		### --- START--- open Google Spreadsheet & Counter-Value
		worksheet = gc.open("notizen").sheet1

		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		
		
		#print(date_list)

		return render_template("delete.html", notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)
		#worksheet.delete_row(8)

@app.route('/output2', methods=["POST", "GET"])
def output2():
	### --- START--- Google Spreadsheet Authentification
	scope = ['https://www.googleapis.com/auth/drive']
	### Google Spreadsheet URL
	gs_url = 'https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit?usp=sharing'
	#Name des credential-Files
	credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
	gc = gspread.authorize(credentials)
	### --- END--- Google Spreadsheet Authentification
	### --- START--- open Google Spreadsheet & Counter-Value
	worksheet = gc.open("notizen").sheet1

	id_list = worksheet.col_values(1)
	notes_list = worksheet.col_values(2)
	date_list = worksheet.col_values(3)
	wer_list = worksheet.col_values(4)
	
	
	date_list_new = date_list[1:]
	#print(date_list_new)

	today = date.today()
	print(today)
	date_difference = []

	for i in date_list_new:
		date_string = i
		date_obj = datetime.strptime(date_string, '%d.%m.%Y')
		date_until = date_obj.date()
		delta = (date_until - today).days
		date_difference.append(delta)
		
		
	date_difference.insert(0, 'Fällig in:')
	

	return render_template("timeline.html", date_difference=date_difference, notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list, gs_url=gs_url)


@app.route('/kalender', methods=["POST", "GET"])
def termin_speichern():
	# file = open('kalendereintrag.ics', 'w')
	# file.write('BEGIN:VCALENDAR\n')
	# file.write('VERSION:2.0 \n')
	# file.write('PROID:Michel Welsch\n')
	# file.write('METHOD:REQUEST\n')
	# file.write('BEGIN:VEVENT\n')
	# file.write('UID:TEST\n')
	# file.write('LOCATION:unknow\n')
	# file.write('SUMMARY:Titel des Termins\n')
	# file.write('DESCRIPTION:Kalendereintrag erstellt aus der WebApp\n')
	# file.write('CLASS:PRIVATE\n')
	# file.write('DTSTART:20191231\n')
	# file.write('DTEND:20191231\n')
	# file.write('END:VEVENT\n')
	# file.write('END:VCALENDAR\n')
	# file.close()


	return render_template('header.html')


# BEGIN:VCALENDAR
# VERSION:2.0 
# PROID:Michel Welsch
# METHOD:REQUEST
# BEGIN:VEVENT
# UID:TEST
# LOCATION:unknow
# SUMMARY:Titel des Termins
# DESCRIPTION:Kalendereintrag erstellt aus der WebApp
# CLASS:PRIVATE
# DTSTART:20191231
# DTEND:20191231
# END:VEVENT
# END:VCALENDAR

if __name__ == "__main__":
    app.run(debug=True, port=5000)
