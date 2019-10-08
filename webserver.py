from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Master Route definiert und erste Ausgabe auf Website
@app.route('/')
def welcome():
    return 'Webserver erfolgreich gestartet (debug=True, port=5000).'

# Sub-Route definiert und HTML-File ausgeben
#@app.route('/input', methods=['POST'])
#def input():
#	if request.method=="POST":
#		vorname = request.form['vorname']
#	return render_template("input.html", vorname=vorname)

@app.route('/input', methods=["POST", "GET"])
def input():
	if request.method=='POST':
		vorname=request.form['vorname']
		return render_template("input.html", vorname=vorname)
	else:
		return render_template("input.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

