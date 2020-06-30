from flask import Flask,render_template,url_for,jsonify,request,redirect,make_response, flash
import json
from bs4 import BeautifulSoup
import random
from datetime import date
import datetime 
from flask_babel import Babel,_,gettext
import os
import requests
from time import sleep 
from urllib.request import urlopen
from wtforms import DateField, BooleanField, IntegerField,Label, ValidationError, validators, FloatField, FormField, Form, FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import uuid
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE']='az'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'adminlogin'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @app.before_request 
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(hours=1)  #burada seconds, minutes, hours, days, years ola biler



UPLOAD_FOLDER = 'static/images/cars/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with open("cars.json", "r") as f:
    masin=json.load(f)
babel=Babel(app)

def  getCountry():
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        country=data['country']
        return country
    except Exception as ex:
        sleep(1)
        return "EN"

@babel.localeselector
def get_local():
    lang=request.cookies.get('language')
    if lang=="en":
        return 'en'
    elif lang=='ru':
        return 'ru'
    elif lang=='tr':
        return 'tr'
    elif lang=='az':
        return "az"
    else:
        lang=getCountry()
        if lang =="AZ":
            return 'az'
        elif lang=='RU':
            return 'ru'
        elif lang=='TR':
            return 'tr'
        elif lang=='US':
            return "en"
        else:
            return request.accept_languages.best_match(['az','ru','tr',"en"])

            

def getObject():
     with open("cars.json","r") as file:
            data=file.read()
            file.close()
            obyekt=json.loads(data)
            return obyekt
def saveMoney(moneys):
    with open("static/currency/currency.json","w") as file:
        json.dump(moneys,file)
      
def work():
    soup = BeautifulSoup(requests.get("http://www.mezenne.az/").content, "html.parser")
    trler = soup.findAll('tr', style="white-space: nowrap;")
    moneyList = []
    for i in trler:
        children = i.findChildren("td", recursive=False)
        pulVahidininAdi = str(children[2]).replace("<td>", "").replace("</td>", "")
        deyer = str(children[3])
        deyerFrom = deyer.find('placeholder="')
        deyer = deyer[deyerFrom + 13:]
        last = deyer.find('"')
        deyer = deyer[:last]
        moneyList.append([pulVahidininAdi, deyer])
    saveMoney(moneyList)
def getJsonFile(path):
    try:
         with open(path,"r", encoding='utf8') as file:
            data=file.read()
            file.close()
            obyekt=json.loads(data)
            return obyekt   
    except Exception as ex:
        print(ex)
        result=getJsonFile(path)
        return result

@app.errorhandler(404)
def error404(error):
    return render_template("404.html")
@app.errorhandler(500)
def error500(error):
    return render_template("404.html")
@app.errorhandler(403)
def error403(error):
    return render_template("404.html")
@app.errorhandler(405)
def error405(error):
    return render_template("404.html")

@app.route("/cars")
def cars():
    website=getJsonFile("static/site/website.json")
    pullar=getJsonFile("static/currency/currency.json")
    with open("cars.json","r") as file:
        data=file.read()
    obyekt=json.loads(data)
    return render_template("cars.html",cars=obyekt,moneys=pullar,website=website)
@app.route("/about")
def about():
    website=getJsonFile("static/site/website.json")
    pullar=getJsonFile("static/currency/currency.json")
    return render_template("about.html",moneys=pullar,website=website)
@app.route("/changemoney/<string:currency>")
def changemoney(currency):
    work()
    return redirect(url_for("index"))
@app.route("/car/<int:id>")
def car(id):
    website=getJsonFile("static/site/website.json")
    pullar=getJsonFile("static/currency/currency.json")
    with open("cars.json","r") as file:
        data=file.read()
        file.close()
    obyekt=json.loads(data)
    return render_template("car.html",id=id,cars=obyekt,moneys=pullar,website=website)
    
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
        return str(gettext('Avtomobilin götürülmə ve buraxılma tarixi yanlış daxil edilib.')), False
    elif str(pick)==str(drop):
        return str(gettext('Avtomobilin götürülmə ve buraxılma tarixi eyni ola bilməz.')), False
    elif len(total)<19:
        return str(gettext('Avtomobilin götürülmə ve ya buraxılma tarixi daxil edilməyib.')), False
    elif totalDays(drop,pick)<0:
        return str(gettext('Avtomobilin buraxılma tarixi götürülmə tarixindən tezdir.')), False
    return "",True
def calPrice(pick,drop,baby,id,carss):
    totalPrice=0
    numberDays=totalDays(drop,pick)
    for car in carss:
        if car['id']==id:
            if numberDays<4:
                totalPrice+=numberDays*car['days']['1_3']
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
def writethismessage(firstname,lastname,email,phone,message):
    with open("messages/messages.json","r" , encoding='utf8') as file:
        data=file.read()
        file.close()
        print(data)
        time=str(datetime.datetime.now())
        data=eval(data)
        amessage={
            'date':time,
            "firstname":firstname,
            "lastname":lastname,
            "email":email,
            "phone":phone,
            "message":message
        }
        data.append(amessage)
        with open("messages/messages.json","w" , encoding='utf8') as file:
            json.dump(data,file)
@app.route("/takemessage",methods=["POST"])
def takemessage():
    if request.method=="POST":
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        writethismessage(firstname,lastname,email,phone,message)
        notfication=str(gettext('Sizin mesajınız uğurlu şəkildə göndərildi !'))
        return "<script>alert('{}');window.location.href='/contact'</script>".format(notfication)
    return render_template("404.html")
# getting messages info with token
# getting messages info with token
@app.route('/messages')
def gettoken():
    auth=request.authorization
    if auth and auth.password=='password' and auth.username=='username':
        return jsonify(getJsonFile("messages/messages.json"))
    return make_response('Coudnt verify',401,{'WWW-Authenticate':'Basic realm="Login Required"'})
# getting messages info with token
# getting messages info with token

# getting responses info with token
# getting responses info with token
@app.route('/responses')
def getresponses():
    auth=request.authorization
    if auth and auth.password=='password' and auth.username=='username':
        return jsonify(getJsonFile("responses/carresponses.json"))
    return make_response('Coudnt verify',401,{'WWW-Authenticate':'Basic realm="Login Required"'})
# getting responses info with token
# getting responses info with token
@app.route("/calc/<int:id>",methods=["POST"])
def calc(id):
    website=getJsonFile("static/site/website.json")
    pullar=getJsonFile("static/currency/currency.json")
    if request.method=="POST":
        pick=request.form.get('pick')
        drop=request.form.get('drop')
        baby=request.form.get('baby')
        obyekt=getObject()
        res = cheking(pick,drop)
        if res[1] is False:
            error=res[0]
            return render_template("car.html",id=id,cars=obyekt,moneys=pullar,error=error,website=website)
        else:
            totalPrice,totalDays,totalBaby=calPrice(pick,drop,baby,id,obyekt) 
            return render_template("car.html",id=id,cars=obyekt,moneys=pullar,totalPrice=totalPrice,totalDays=totalDays,totalBaby=totalBaby,website=website,pick=pick,drop=drop)
        return render_template("car.html",id=id,cars=obyekt,website=website)
        
    return render_template("404.html")
@app.route("/contact")
def contact():
    pullar=getJsonFile("static/currency/currency.json")
    website=getJsonFile("static/site/website.json")
    return render_template("contact.html",website=website,moneys=pullar)
def writethisresponse(fullname,mail,phone,carid,totalPrice,pickdate,dropdate,babyseat):
    with open("responses/carresponses.json","r",encoding='utf8') as file:
        data=file.read()
        file.close()
        data=eval(data)
        time=str(datetime.datetime.now())
        amessage={
            'date':time,
            "fullname":fullname,
            "mail":mail,
            "phone":phone,
            "carid":carid,
            "totalPrice":totalPrice,
            "pickdate":pickdate,
            "dropdate":dropdate,
            "babyseat":babyseat
        }
        data.append(amessage)

        with open("responses/carresponses.json","w",encoding='utf8') as file:
            json.dump(data,file)
            print(data)
@app.route("/wewillcallyou/<int:carid>/<int:totalPrice>/<string:pickdate>/<string:dropdate>/<string:babyseat>",methods=["POST"])
def wewillcallyou(carid,totalPrice,pickdate,dropdate,babyseat):
    if request.method=="POST":
        name=request.form.get('name')
        mail=request.form.get('mail')
        phone=request.form.get('phone')
        writethisresponse(name,mail,phone,carid,totalPrice,pickdate,dropdate,babyseat)
        notfication=str(gettext('Salam hörmətli {} . Sizin istəyiniz qeydə alındı ən yaxın zamanda sizinlə əlaqə saxlayacağıq.Bizi seçdiyiniz üçün minnətdarıq.').format(name))
        return "<script>alert('{}');window.location.href='/cars'</script>".format(notfication)
    return render_template("404.html")
@app.route("/")
def index():
    pullar=getJsonFile("static/currency/currency.json")
    website=getJsonFile("static/site/website.json")
    obyekt=getObject()
    try:
        aCar=random.randint(1,len(obyekt))
    except Exception as ex:
        print(ex)
        aCar=None
    print("random a car",aCar)
    return render_template("index.html",cars=obyekt,moneys=pullar,aCar=aCar,website=website)

@app.route("/currency")
def getcur():
    result=getJsonFile("static/currency/currency.json")
    return jsonify(result)


#-------------------------------------------------ADMIN PANEL-----------------------------------------------

class CarForm(FlaskForm):
    carname = StringField("Masinin Adi", validators=[DataRequired(), Length(min=2, max=20)])
    cartypelevel = SelectField("Masin Tipi Derece", choices=[('sport', 'sport'), ('business', 'business'),
        ('full-size', 'full-size'), ('minivan', 'minivan'), ('economy', 'economy')])
    doors = IntegerField("Qapi Sayi", validators=[NumberRange(min=2, max=15, message='Invalid length')])
    seat = IntegerField("Oturacaq Sayi", validators=[NumberRange(min=2, max=15, message='Invalid length')])
    engine = FloatField("Muherrik", validators=[DataRequired()])
    transmission = SelectField("Ötürücü" ,choices=[('Avtomatik', 'Avtomatik' ), ('Mexanik', 'Mexanik')])
    day_1_3 = IntegerField("1-3 gunluk", validators=[DataRequired()])
    day_4_7 = IntegerField("4-7 gunluk", validators=[DataRequired()])
    day_8_15 = IntegerField("8-15 gunluk", validators=[DataRequired()])
    day_16_30 = IntegerField("16-30 gunluk", validators=[DataRequired()])
    day_30_ = IntegerField("30+ gunluk", validators=[DataRequired()])
    year = IntegerField("İl", validators=[DataRequired()])
    picture = FileField("Sekil", validators=[FileRequired('Bir sekil secin'), FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece sekil')])
    pictures = FileField('Sekiller', validators=[FileRequired('Bir sekil secin'), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Send')





class LoginForm(FlaskForm):
    username = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"





@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    form=LoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            return redirect(url_for('adminpanel'))
        else:
            flash(message='istifadeci adi veya sifre yanlisdir', category='danger') 
    return render_template("adminlogin.html", form=form)


@app.route("/adminpanel")
@login_required
def adminpanel():
    return render_template("adminpanel.html")


@app.route("/adminpanel/cars")
@login_required
def show_cars():
    website = getJsonFile("static/site/website.json")
    pullar = getJsonFile("static/currency/currency.json")
    with open("cars.json", "r") as file:
        data = file.read()
    obyekt = json.loads(data)
    return render_template("admincars.html", website=website, pullar=pullar, cars=obyekt)


@app.route("/adminpanel/car/<int:id>")
@login_required
def show_car(id):
    website = getJsonFile("static/site/website.json")
    pullar = getJsonFile("static/currency/currency.json")
    with open("cars.json", "r") as file:
        data = file.read()
        file.close()
    obyekt = json.loads(data)
    return render_template("admincar.html", id=id, cars=obyekt, moneys=pullar, website=website)


def getObject():
    with open("cars.json", "r") as file:
        data = file.read()
        file.close()
        obyekt = json.loads(data)
        return obyekt
@app.route("/adminpanel/addcar", methods=["GET", "POST"])
@login_required
def add_car():
    form=CarForm()
    if form.validate_on_submit():
        print('burdayam')
        cars=getObject() 
        maksimum=0
        for i in cars:
            try:
                maksimum = max(i['id'], maksimum)
            except Exception as ex:
                print(ex)
        print(maksimum,"maksimum id")
        filename = str(uuid.uuid4()) + secure_filename(form.picture.data.filename)
        form.picture.data.save(app.config['UPLOAD_FOLDER'] + filename)
        images = request.files.getlist("pictures")
        image_files = []
        imagesForJson=[]
        if images:
            for img in images:
                # Create Images
                file_name = str(uuid.uuid4()) + secure_filename(img.filename)
                image_file = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                imagesForJson.append("images/cars/"+file_name)
                img.save(image_file)
                image_files.append(image_file)
        masinbilgi = {
            "id":maksimum+1,
            "car_name" : form.carname.data,
            "car_type_level" : form.cartypelevel.data,
            "doors" : form.doors.data,
            "seat" : form.seat.data,
            "engine" : form.engine.data,
            "transmission" : form.transmission.data,
            "days": {
                    "1_3": form.day_1_3.data,
                    "4_7": form.day_4_7.data,
                    "8_15": form.day_8_15.data,
                    "16_30": form.day_16_30.data,
                    "30_": form.day_30_.data
            },
            "year" : form.year.data,
            "photo_links": "images/cars/"+ filename,
            "links": imagesForJson,

        }
        cars.append(masinbilgi)
        with open("cars.json", "w", encoding="utf-8") as file:
            json.dump(cars, file, indent=7)
        return redirect(url_for("show_cars"))
    return render_template("adminaddcar.html", form=form)



#EDIT
def getObjectEdit():
    with open("cars.json", "r") as file:
        data = file.read()
        file.close()
        obyekt = json.loads(data)
        return obyekt


@app.route("/adminpanel/car/<int:id>/edit", methods=["GET", "POST"])
@login_required
def car_edit(id):
    form = CarForm()
    cars = getObjectEdit()
    for car in cars:
        if form.validate_on_submit():
            print("post olmur")
       	    car["car_name"] = form.carname.data
            car["car_type_level"] = form.cartypelevel.data
            car["doors"] = form.doors.data
            car["seat"] = form.seat.data
            car["engine"] = form.engine.data
            car["transmission"] = form.transmission.data
            car["days"]["1_3"] = form.day_1_3.data
            car["days"]["4_7"] = form.day_4_7.data
            car["days"]["8_15"] = form.day_8_15.data
            car["days"]["16_30"] = form.day_16_30.data
            car["days"]["30_"] = form.day_30_.data
            car["year"] = form.year.data
            cars.append(car)
            with open("cars.json", "w", encoding="utf-8") as file:
                json.dump(cars, file, indent=7)
            return redirect(url_for("show_cars"))
            print("blah blah")
        elif request.method == "GET":
            form.carname.data = car["car_name"]
            form.cartypelevel.data = car["car_type_level"]
            form.doors.data = car["doors"]
            form.seat.data = car["seat"]
            form.engine.data = car["engine"]
            form.transmission.data = car["transmission"]
            form.day_1_3.data = car["days"]["1_3"]
            form.day_4_7.data = car["days"]["4_7"]
            form.day_8_15.data = car["days"]["8_15"]
            form.day_16_30.data = car["days"]["16_30"]
            form.day_30_.data = car["days"]["30_"]
            form.year.data = car["year"]
        return render_template("admineditcar.html", id=id, form=form, cars=cars)



#DELETE

@app.route("/adminpanel/car/<int:id>/delete", methods=["POST"])
def deletecar(id):
    with open("cars.json", "r") as file:
        data = file.read()
    galery = json.loads(data)
    for photo in galery:
        if photo["id"] == id:
            galery.remove(photo)
            for sekil in photo["links"]:
                os.remove('static/' + sekil)
            os.remove('static/' + photo["photo_links"])
            with open("cars.json", "w", encoding="utf-8") as file:
                json.dump(galery, file, indent=7, ensure_ascii=False)
            return redirect(url_for("adminpanel"))



@app.route("/adminpanel/message")
@login_required
def show_message():
    return render_template("adminmessages.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#-------------------------------------------------ADMIN PANEL-----------------------------------------------


if __name__=="__main__":
    app.run(port=5000,debug=True,host='127.0.0.2')
