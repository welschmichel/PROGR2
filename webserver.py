from flask import Flask, render_template, request, url_for

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


