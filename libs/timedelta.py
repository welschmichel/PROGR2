from datetime import date, datetime

def calc_timedelta(date_list):
	### remove title from the column
	date_list_new = date_list[1:]
	### get today's date
	today = date.today()
	### empty list
	date_difference = []
	### calculate time-delta from note "fällig am" & "today's date" in days and append to list
	for i in date_list_new:
		date_obj = datetime.strptime(i, '%d.%m.%Y')
		date_until = date_obj.date()
		delta = (date_until - today).days
		date_difference.append(delta)
	### insert title "fällig in" at the beginning from list
	date_difference.insert(0, 'Fällig in ... Tage')
	### return the list with the timedeltas in days
	return date_difference