from flask import Flask,render_template,url_for
import json
app = Flask(__name__)
@app.route("/cars")
def cars():
    with open("cars.json","r") as file:
        data=file.read()
    obyekt=json.loads(data)
    
    return render_template("cars.html",cars=obyekt)
@app.route("/about")
def about():
    return render_template("about.html")    
@app.route("/car/<int:id>")
def car(id):
    with open("cars.json","r") as file:
        data=file.read()
    obyekt=json.loads(data)
    return render_template("car.html",id=id,cars=obyekt)        
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/")
def index():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)