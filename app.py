from flask import Flask,render_template,url_for
app = Flask(__name__)
@app.route("/cars")
def cars():
    return render_template("cars.html")
@app.route("/about")
def about():
    return render_template("about.html")    
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/")
def index():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)