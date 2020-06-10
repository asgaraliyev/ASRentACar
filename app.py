from flask import Flask,render_template,url_for,request
import json
from datetime import date
app = Flask(__name__)
def getObject():
     with open("cars.json","r") as file:
            data=file.read()
            file.close()
            obyekt=json.loads(data)
            return obyekt
@app.errorhandler(404)
def error404(error):
    return render_template("404.html")
@app.errorhandler(500)
def error500(error):
    return render_template("404.html")
@app.errorhandler(403)
def error500(error):
    return render_template("404.html")
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
    try:
        for i in pick:    
            i=i.replace(" ","")
            pickk.append(int(i))
        pick=date(pickk[0],pickk[1],pickk[2])
        today=date.today()
        today=str(today).split("-")
        todayy=[]
        for i in today:
            i=i.replace(" ","")
            
            todayy.append(int(i))
        print(todayy,"seseseseasease")
        fromToday=pick-date(todayy[0],todayy[1],todayy[2])
        print(fromToday,"seseseseasease")

        try:
            fromToday=int(str(fromToday).split(",")[0].strip("days"))
        except Exception as ex:
            print(ex,"""
               try:
            fromToday=int(str(fromToday).split(",")[0].strip("days"))
        except Exception as ex:
            """)
            fromToday=1
        if fromToday<0:
            return True
        
    except Exception as ex:
        print(ex)
        return True
    return False
    
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
    if dataNowDays(pick):
        return "Informasiya yanlis daxil edilib",False
    elif str(pick)==str(drop):
        return "Goturulme tarixi ve buraxilma tarixi eyni ola bilmez",False
    elif len(total)<19:
        return "Goturulme tarixi ve ya buraxilma tarixi daxil edilmeyib",False
    elif totalDays(drop,pick)<0:
        return "Buraxilma tarixi Goturulme tarixinden tezdir",False
    return "",True

def calPrice(pick,drop,baby,id,carss):
    totalPrice=0
    numberDays=totalDays(drop,pick)
    
    for car in carss:
        if car['id']==id:
            if numberDays<4:
                totalPrice+=numberDays*car['days']['2_3']
            elif numberDays<8:
                totalPrice+=numberDays*car['days']['4_7']
            elif numberDays<16:
                totalPrice+=numberDays*car['days']['8_15']
            elif numberDays<30:
                totalPrice+=numberDays*car['days']['16_30']
            elif numberDays>=30:
                totalPrice+=numberDays*car['days']['30_']
    if "0"!=str(baby):
        totalPrice+=30
        return totalPrice,numberDays,True
    return totalPrice,numberDays,False
    
@app.route("/calc/<int:id>",methods=["POST"])
def calc(id):
    if request.method=="POST":
        pick=request.form.get('pick')
        drop=request.form.get('drop')
        baby=request.form.get('baby')
        obyekt=getObject()
        res = cheking(pick,drop)
        if res[1] is False:
            error=res[0]
            return render_template("car.html",id=id,cars=obyekt,error=error)
        else:
            totalPrice,totalDays,totalBaby=calPrice(pick,drop,baby,id,obyekt) 
            return render_template("car.html",id=id,cars=obyekt,totalPrice=totalPrice,totalDays=totalDays,totalBaby=totalBaby) 
        return render_template("car.html",id=id,cars=obyekt) 
        
    return render_template("404.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/wewillcallyou",methods=["POST"])
def wewillcallyou():
        if request.method=="POST":
            name=request.form.get('name')
            mail=request.form.get('mail')
            phone=request.form.get('phone')
            obyekt=getObject()
            return  render_template("cars.html",cars=obyekt,callyou=True)
        return render_template("404.html")
@app.route("/")
def index():
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)