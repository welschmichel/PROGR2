from flask import Flask, render_template, request, url_for, jsonify,json

app = Flask(__name__)

# Master Route definiert und erste Ausgabe auf Website
@app.route('/ok')
def welcome():
    return 'Webserver erfolgreich gestartet (debug=True, port=5000).'

# Sub-Route definiert und HTML-File ausgeben
#@app.route('/input', methods=['POST'])
#def input():
#	if request.method=="POST":
#		vorname = request.form['vorname']
#	return render_template("input.html", vorname=vorname)

# Test-Route for JSON
@app.route('/json')
def json():
	try:
		meine_liste = []
		for i in range(0,3):
			mein_dict = {
			'vorname':'Michel',
			'nachname': 'Welsch'}
			meine_liste.append(mein_dict)

		jsonStr = json.dumps(meine_liste)

	except:
		print('fehler')

	return render_template("json.html", meine_liste=meine_liste)
	return jsonify(meine_liste)








	#notiz1 = 'Hallo ich bin der Text aus der Notiz'
	#datum1 = '19. Januar 2020'
	#notiz2 = 'ich bin die zweite Notiz'
	#datum2 = '01.01.2022'
	#return render_template('json.html')


@app.route('/', methods=["POST", "GET"])
def index():
	return render_template("header.html")

@app.route('/input', methods=["POST", "GET"])
def input():
	if request.method=='POST':
		notiz=request.form['notiz']
		date=request.form['date']
		notiz = notiz.capitalize()
		single_date = date.split("-")
		

		return render_template("input.html", notiz=notiz, date=date, single_date=single_date)
	else:
		return render_template("input.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)


