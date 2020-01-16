from flask import Flask, render_template, request, url_for, flash
from libs import gapi, timedelta
import gspread
import calendar
import time
import webbrowser


app = Flask(__name__)
app.secret_key = b'_5#y2Ldnoisf(#"F4Q8z\n\xec]/'

print('---------------------------------------------------------------------------')
print('| Viel Spass beim Erfassen von Notizen... bitte lese zuerst die readme.md |')
print('---------------------------------------------------------------------------')

# ---------------------------------------------------------------------------------
# Input: no input on this site
# Output: just the header.html
# ---------------------------------------------------------------------------------
@app.route('/')
def index():
	return render_template("header.html")

# ---------------------------------------------------------------------------------
# Input: type in your note, date and the responsible person and click on "speichern"
# Output: you should see a success-message and your note
# ---------------------------------------------------------------------------------
@app.route('/input', methods=["POST", "GET"])
def input():
	if request.method=='POST':
		### Google-API Authentification and return Google credentials
		gc = gapi.google_authentification()
		### Open Google Spreedsheet with passed credentials
		worksheet = gapi.open_spreadsheet(gc)
		### Get position from next empty row
		val = gapi.get_position_from_row(worksheet)
		### request the input-values from input.html
		notiz=request.form['notiz']
		date=request.form['date']
		wer=request.form['wer']		
		### create timestamp to save with the note || represents a unique id for each note
		ts = calendar.timegm(time.gmtime())
		ts = int(ts)				
		### Flash text - displayed if note added succesful 
		flash('Die Notiz wurde erfolgreich gespeichert!')
		### Update the Google Spreedsheet with input-data
		gapi.update_worksheet(worksheet, val, ts, notiz, date, wer)
		### Get date from spreadsheet to display
		date=worksheet.acell('C'+str(val)).value
		### Return input.html and send data to input.html
		return render_template("input.html", len=len, notiz=notiz, date=date, wer=wer)
	else:
		return render_template("input.html", len=len)

# ---------------------------------------------------------------------------------
# Input: no input on this site
# Output: you should see a table which contains your notes. Notice: no notes, no table
# ---------------------------------------------------------------------------------
@app.route('/output')
def output():
	### Google-API Authentification and return Google credentials
	gc = gapi.google_authentification()
	### Open Google Spreedsheet with passed credentials
	worksheet = gapi.open_spreadsheet(gc)
	### Get data from the spreadsheet and store in list
	id_list, notes_list, date_list, wer_list = gapi.get_spreadsheet_data(worksheet)
	### Google Spreadsheet URL
	gs_url = 'https://docs.google.com/spreadsheets/d/1RpGohe8TQ1XF_vHehBqiY8qHROXgtlVR6ozk9we6Blk/edit?usp=sharing'
	### return output.html and sending data to output.html
	return render_template("output.html", zip=zip, notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list, gs_url=gs_url)
	
# ---------------------------------------------------------------------------------
# Input: type in the id you want and click on "löschen"
# Output: depending on the id, you get a "success" oder "error" message
# ---------------------------------------------------------------------------------
@app.route('/delete', methods=["POST", "GET"])
def delete():
	if request.method=='POST':
		### request id from delete.html
		nummer=request.form['nummer']
		### Google-API Authentification and return Google credentials 
		gc = gapi.google_authentification()
		### Open Google Spreedsheet with passed credentials
		worksheet = gapi.open_spreadsheet(gc)
		### Pass worksheet and id-number to the delete function & delete the whole row & get success/error-message
		message = gapi.delete_spreadsheet_data(worksheet, nummer)
		### Get data from the spreadsheet and store in list
		id_list, notes_list, date_list, wer_list = gapi.get_spreadsheet_data(worksheet)
		### return delete.html and sending data to delete.html
		return render_template("delete.html", message=message, len=len, zip=zip, notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)

	else:
		### Google-API Authentification and return Google credentials 
		gc = gapi.google_authentification()
		### Open Google Spreedsheet with passed credentials
		worksheet = gapi.open_spreadsheet(gc)
		### Get data from the spreadsheet and store in list
		id_list, notes_list, date_list, wer_list = gapi.get_spreadsheet_data(worksheet)		
		### return delete.html and sending data to delete.html
		return render_template("delete.html", len=len, zip=zip, notes_list=notes_list, date_list=date_list, id_list=id_list, wer_list=wer_list)

# ---------------------------------------------------------------------------------
# Input: no input on this site
# Output: you should see a table which contains your notes and the timedelta.
#         Notice: no notes, no table
# ---------------------------------------------------------------------------------		
@app.route('/output2')
def output2():
	### Google-API Authentification and return Google credentials 
	gc = gapi.google_authentification()
	### Open Google Spreedsheet with passed credentials
	worksheet = gapi.open_spreadsheet(gc)
	### Get data from the spreadsheet and store in list
	id_list, notes_list, date_list, wer_list = gapi.get_spreadsheet_data(worksheet)
	### calculate the timedelta from today till expiration date and return timedelta-list 
	date_difference = timedelta.calc_timedelta(date_list)
	### return timeline.html and sending data to timeline.html
	return render_template("timeline.html", zip=zip, date_difference=date_difference, notes_list=notes_list, date_list=date_list, wer_list=wer_list, id_list=id_list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

