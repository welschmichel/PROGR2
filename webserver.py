from flask import Flask, render_template, request, url_for, jsonify, json, flash
from datetime import date, datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import calendar
import time
import webbrowser


app = Flask(__name__)
app.secret_key = b'_5#y2Ldnoisf(#"F4Q8z\n\xec]/'
app.config["CACHE_TYPE"] = "null"

print(' ---> Viel Spass beim Erfassen von Notizen... bitte lese zuerst die readme.md')

# Master Route definiert und erste Ausgabe auf Website
@app.route('/pulse')
def welcome():
    return 'Flask erfolgreich gestartet (debug=True, port=5000).'

# Startsite
@app.route('/', methods=["POST", "GET"])
def index():
	return render_template("header.html")



# Input-Site for adding Notes
@app.route('/input', methods=["POST", "GET"])
def input():
	if request.method=='POST':
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']

		# name/place credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification

		### --- START--- open Google Spreadsheet & Counter-Value
		worksheet = gc.open("notizen").sheet1
		val = worksheet.acell('E1').value

		### --- START--- request the input-values from input.html
		notiz=request.form['notiz']
		date=request.form['date']
		wer=request.form['wer']
		
		### --- START--- change cell-value 'E1' from str to int and ++ || Needed for placing the note in the right cell
		val = int(val)
		val = val + 1

		### create timestamp to save with the note || it's also an unique id for every note
		ts = calendar.timegm(time.gmtime())
		ts = int(ts)
				
		### Flash text - displayed if note added succesful 
		flash('Die Notiz wurde erfolgreich gespeichert!')


		### --- START--- store the input-values in the spreadsheet
		worksheet.update_acell('A'+str(val), ts)
		worksheet.update_acell('B'+str(val), notiz)
		worksheet.update_acell('C'+str(val), date)
		worksheet.update_acell('D'+str(val), wer)
		### --- END--- store the input-values in the spreadsheet
		
		### Get date from spreadsheet to display
		date=worksheet.acell('C'+str(val)).value
		### define max. possible notes || change value 'A200' for changing max possible notes
		worksheet.update_acell('E1', '=ANZAHL2(A1:A200)')
		

		### Return input.html and send data to input.html
		return render_template("input.html", len=len, notiz=notiz, date=date, wer=wer)
	else:
		return render_template("input.html", len=len)

# Output-Site for displaying notes
@app.route('/output', methods=["POST", "GET"])
def output():
	### --- START--- Google Spreadsheet Authentification
	scope = ['https://www.googleapis.com/auth/drive']
	### Google Spreadsheet URL
	gs_url = 'https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit?usp=sharing'

	# name/place credential-Files
	credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
	gc = gspread.authorize(credentials)
	### --- END--- Google Spreadsheet Authentification

	### --- START--- open Google Spreadsheet & get data from column & add to list
	worksheet = gc.open("notizen").sheet1
	id_list = worksheet.col_values(1)
	notes_list = worksheet.col_values(2)
	date_list = worksheet.col_values(3)
	wer_list = worksheet.col_values(4)
	### --- END--- open Google Spreadsheet & get data from column & add to list


	### return output.html and sending data to output.html
	return render_template("output.html", zip=zip, notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list, gs_url=gs_url)
	
# Output-Site for displaying & deleting notes 
@app.route('/delete', methods=["POST", "GET"])
def delete():
	if request.method=='POST':
		### request id from delete.html which get's deleted
		nummer=request.form['nummer']
		
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']

		# name/place  credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification

		### --- START--- open Google Spreadsheet & get data from column & add to list
		worksheet = gc.open("notizen").sheet1
		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		### --- START--- open Google Spreadsheet & get data from column & add to list

		### --- START--- deleting a note (row)
		# find the cell-cordinates which matches the id
		cell = worksheet.find(nummer)
		# delete the row which includes the matching id
		worksheet.delete_row(cell.row)
		# flash text if deleting was succesfull
		flash('Die Notiz wurde erfoglreich gelöscht!')
		### --- END--- deleting a note (row)

		### --- START--- get data from column & add to list || done twice for updating the site
		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		### --- END--- get data from column & add to list || done twice for updating the site
		
		### return delete.html and sending data to delete.html
		return render_template("delete.html", zip=zip, notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)

	else:
		### --- START--- Google Spreadsheet Authentification
		scope = ['https://www.googleapis.com/auth/drive']

		# name/place credential-Files
		credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
		gc = gspread.authorize(credentials)
		### --- END--- Google Spreadsheet Authentification

		### --- START--- open Google Spreadsheet & get data from column & add to list
		worksheet = gc.open("notizen").sheet1
		id_list = worksheet.col_values(1)
		notes_list = worksheet.col_values(2)
		date_list = worksheet.col_values(3)
		wer_list = worksheet.col_values(4)
		### --- END--- open Google Spreadsheet & get data from column & add to list
		
		### return delete.html and sending data to delete.html
		return render_template("delete.html", zip=zip, notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)
		
@app.route('/output2', methods=["POST", "GET"])
def output2():
	### --- START--- Google Spreadsheet Authentification
	scope = ['https://www.googleapis.com/auth/drive']

	### Google Spreadsheet URL
	gs_url = 'https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit?usp=sharing'

	# name/place credential-Files
	credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
	gc = gspread.authorize(credentials)
	### --- END--- Google Spreadsheet Authentification

	### --- START--- open Google Spreadsheet & get data from column & add to list
	worksheet = gc.open("notizen").sheet1
	id_list = worksheet.col_values(1)
	notes_list = worksheet.col_values(2)
	date_list = worksheet.col_values(3)
	wer_list = worksheet.col_values(4)
	### --- END--- open Google Spreadsheet & get data from column & add to list
	
	### remove title from the column
	date_list_new = date_list[1:]
	
	### get today's date
	today = date.today()
	
	### empty list
	date_difference = []

	### calculate time-delta from note "fällig am" & "today's date" in days and append to list
	for i in date_list_new:
		date_string = i
		date_obj = datetime.strptime(date_string, '%d.%m.%Y')
		date_until = date_obj.date()
		delta = (date_until - today).days
		date_difference.append(delta)
		
	### insert title "fällig in" at the beginning from list
	date_difference.insert(0, 'Fällig in ... Tage')
	
	### return timeline.html and sending data to timeline.html
	return render_template("timeline.html", zip=zip, date_difference=date_difference, notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list, gs_url=gs_url)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

