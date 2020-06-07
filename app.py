from flask import Flask,render_template,url_for,request
import json
from datetime import date
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
        file.close()
    obyekt=json.loads(data)
    return render_template("car.html",id=id,cars=obyekt) 
def dataNowDays(picked):
    pick=str(picked).split("-")
    pickk=[]
    for i in pick:
        pickk.append(int(i))
    pick=date(pickk[0],pickk[1],pickk[2])
    today=date.today()
    howmanydays=pick-today
    print("howmanydays:",howmanydays)
    
def totalDays(droped,picked):
    drop=str(droped).split("-")
    pick=str(picked).split("-")
    dropp=[]
    for i in drop:
        dropp.append(int(i))
    pickk=[]
    for i in pick:
        pickk.append(int(i))
    drop=date(dropp[0],dropp[1],dropp[2])
    pick=date(pickk[0],pickk[1],pickk[2])
    days=drop-pick
    days=str(days).split(",")
    days=days[0]
    days=days.strip("days")
    numberDays=int(days)
    return numberDays
def cheking(pick,drop):
    total=str(pick)+str(drop)
    print(total)
    dataNowDays(pick)
    if len(total)<19:
        return "Goturulme tarixi ve ya buraxilma tarixi daxil edilmeyib",False
    elif totalDays(drop,pick)<0:
        return "Buraxilma tarixi Goturulme tarixinden tezdir",False
    return "",True

def calPrice(pick,drop,baby,id,carss):
    totalPrice=0
    numberDays=totalDays(drop,pick)
    print(baby,"babyu")
    if "0"!=str(baby):
        totalPrice+=30
    for car in carss:
        if car['id']==id:
            if numberDays<4:
                totalPrice+=numberDays*car['days']['2_3']
            elif numberDays<8:
                totalPrice+=numberDays*car['days']['4_7']
            elif numberDays<16:
                totalPrice+=numberDays*car['days']['8_15']
            elif numberDays<31:
                totalPrice+=numberDays*car['days']['16_30']
            elif numberDays>31:
                totalPrice+=numberDays*car['days']['30_'] 
    print(totalPrice)
    
@app.route("/calc/<int:id>",methods=["POST"])
def calc(id):
    if request.method=="POST":
        pick=request.form.get('pick')
        drop=request.form.get('drop')
        baby=request.form.get('baby')
        
        with open("cars.json","r") as file:
            data=file.read()
            file.close()
        obyekt=json.loads(data)
        res = cheking(pick,drop)
        if res[1] is False:
            error=res[0]
            return render_template("car.html",id=id,cars=obyekt,error=error)
        else:
            calPrice(pick,drop,baby,id,obyekt) 
        return render_template("car.html",id=id,cars=obyekt) 
        
    return "islemedi"
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/")
def index():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)