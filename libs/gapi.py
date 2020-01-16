### all functions for establishing googledrive-connection and interact with the spreadsheet

from oauth2client.service_account import ServiceAccountCredentials
import gspread

def google_authentification():
	### --- START--- Google Spreadsheet Authentification
	scope = ['https://www.googleapis.com/auth/drive']
	# name/place credential-Files
	credentials = ServiceAccountCredentials.from_json_keyfile_name('static/client_secret.json', scope)
	gc = gspread.authorize(credentials)
	return gc
	### --- END--- Google Spreadsheet Authentification

def open_spreadsheet(gc):
	### open Google Spreadsheet
	worksheet = gc.open("notizen").sheet1
	return worksheet

def get_position_from_row(worksheet):
	### get the value from cell "E1", which contains next empty row
	val = worksheet.acell('E1').value
	val = int(val)
	return val

def update_worksheet(worksheet, val, ts, notiz, date, wer):
	### store the input-values in the spreadsheet
	worksheet.update_acell('A'+str(val), ts)
	worksheet.update_acell('B'+str(val), notiz)
	worksheet.update_acell('C'+str(val), date)
	worksheet.update_acell('D'+str(val), wer)
	### define max. possible notes || change value 'A200' for changing max possible notes
	worksheet.update_acell('E1', '=ANZAHL2(A1:A200)+1')

def get_spreadsheet_data(worksheet):
	### get all values from spreadsheet and store in lists
	id_list = worksheet.col_values(1)
	notes_list = worksheet.col_values(2)
	date_list = worksheet.col_values(3)
	wer_list = worksheet.col_values(4)
	return id_list, notes_list, date_list, wer_list

def delete_spreadsheet_data(worksheet, nummer):
	try:
		### find the cell-cordinates which matches the id
		cell = worksheet.find(nummer)
		### delete the row which includes the matching id
		worksheet.delete_row(cell.row)
		### updating cell "E1", because a row was deleted
		worksheet.update_acell('E1', '=ANZAHL2(A1:A200)+1')
		### define success-message - DONT CHANGE!
		success = 'Die Notiz wurde erfolgreich gelöscht!'
		return success
	except:
		### define error-message - DONT CHANGE!
		exception = 'ID nicht gefunden...'
		return exception

