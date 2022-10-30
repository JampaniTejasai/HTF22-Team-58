
import mimetypes
from telnetlib import STATUS
from urllib import response
from flask import Flask,jsonify,render_template,request,redirect,url_for
import json
from bson.json_util import dumps
import pymongo
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from geopy.distance import geodesic
# Create your views here.
from geopy.geocoders import Nominatim
import bcrypt
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'project_21'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/project_21'
app.config['SECRET_KEY']="obndobnoboid"
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('register.html')

@app.route('/donar_ho')
def donar_ho():
    return render_template('Donar_home.html')
@app.route('/bank_home')
def bank_home():
    return render_template('BloodBank_home.html')
@app.route('/hosp_home')
def hosp_home():
    return render_template('Hospital_home.html')

@app.route('/home')

def index():
    if 'username' in session:
        users = mongo.db.users
        user_id = users.find_one({'name' : session['username']},{"_id" :1})
        # print(users.find_one({'name' : session['username']},{"_id" :1}))
        users_data = mongo.db.usersdata
        # users_data.insert_one({'user_id': user_id['_id'],'item':'Carrots','quantity':'100','month':'Oct','year':'2022'})
        # print(user_id['_id'])
        user_data = users_data.find({'user_id' : user_id['_id']},{'_id':0})
        total_calories = [0 for i in range(0,12)]
        # list(user_data)[0]['item']
        months = {"Jan":[], "Feb":[], "Mar":[], "Apr":[], "May":[], "Jun":[], "Jul":[], "Aug":[], "Sep":[], "Oct":[], "Nov":[], "Dec":[]}
        months_data = {"Jan":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Feb":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Mar":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Apr":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "May":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Jun":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Jul":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Aug":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Sep":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Oct":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Nov":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}, "Dec":{'Protiens':0,'Fats':0,'Carbohydrates':0,'Vitamins':0,'cholesterol':0,'calories':0}}
        # print(months) req(an['item'])[0]
        for an in list(user_data):
            # print(list(req('milk'))[0])
            dict1 = req(an['item'])[0]
            dict2 = {'quantity':an['quantity']}
            dict1.update(dict2)
            (months[an['month']].append(dict1))
            # months[an['month']].append({'quantity' : an['quantity']})
            # if an['month'] == months[i]:
                # print(req(an['item'])[0]['calories'])
                # total_calories[i]+=int(req(an['item'])[0]['calories'])
                # print(total_calories[i],'*******')
        # return 'You are logged in as ' + session['username']
        # print(user_data)
        an=0
        for i in months:
            # print(months[i])
            for k in months[i]:

                
                total_calories[an]+=float(int(k['quantity'])/100)*int(k['calories'])
                # print(k[0])
                # print(months[i][0])
                months_data[i]['Protiens']+=float(int(k['quantity'])/100)*float(k['protein'][0:2])
                months_data[i]['Fats']+=float(int(k['quantity'])/100)*float(k['total_fat'][0:2])
                months_data[i]['Carbohydrates']+=float(int(k['quantity'])/100)*float(k['carbohydrate'][0:2])
                months_data[i]['Vitamins']+=float(int(k['quantity'])/100)*(float(k['vitamin_a'][0:2])+float(k['vitamin_b12'][0:2])+float(k['vitamin_b6'][0:2])+float(k['vitamin_c'][0:2])+float(k['vitamin_d'][0:2])+float(k['vitamin_e'][0:2])+float(k['vitamin_k'][0:2]))
                months_data[i]['cholesterol']+=float(int(k['quantity'])/100)*(float(k['cholesterol'][0:2]))
                months_data[i]['calories']+=float(int(k['quantity'])/100)*(float(k['calories'][0:2]))
            
            an+=1
        # print(months_data["Oct"] )
        monthdata = [[]]
        for i in months:
            lis = []
            for an in months_data['Jan']:
                lis.append(months_data[i][an])
            monthdata.append(lis)
        print(monthdata[10])
        return render_template('odash.html', values = total_calories,months = months,months_data = months_data ,jan = monthdata[1],feb = monthdata[2],mar = monthdata[3],apr = monthdata[4],may = monthdata[5],jun = monthdata[6],jul = monthdata[7],aug = monthdata[8],sep = monthdata[9],oct = monthdata[10],nov = monthdata[11],dec = monthdata[12])

    return render_template('signin.html')

@app.route('/donar_login', methods=['POST'])
def donar_login():
    donars = mongo.db.donars
    login_user = donars.find_one({'email' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('donar_dashboard'))

    return 'Invalid username/password combination'
@app.route('/hospital_login', methods=['POST'])
def hospital_login():
    hosps=mongo.db.hospital
    login_user=hosps.find_one({'email' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('hosp_dashboard'))

def donar_login():
    donars = mongo.db.donars
    login_user = donars.find_one({'email' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('donar_dashboard'))

    return 'Invalid username/password combination'
    
@app.route('/bank_login', methods=['POST','GET'])
def bank_login():
    banks = mongo.db.banks
    if 'username' in session:
        user_id = banks.find_one({'email' : session['username']},{'_id':1})
        bloodgroups = mongo.db.bloodgroups.find_one({'bank_id':user_id})
        # print(bloodgroups['group_A+'])
        return render_template('Blood_Bank_dashboard.html',bloodgroups = bloodgroups)

    login_user = banks.find_one({'email' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            user_id = banks.find_one({'email' : request.form['username']},{'_id':1})
            bloodgroups = mongo.db.bloodgroups.find_one({'bank_id':user_id})
            session['username'] = request.form['username']
            # print(bloodgroups['group_A+'])
            return render_template('Blood_Bank_dashboard.html',bloodgroups = bloodgroups)

    return 'Invalid username/password combination'

@app.route('/donar_dashboard')
def donar_dashboard():
    if 'username' in session:
        donars = mongo.db.donars
        banks = mongo.db.banks
        user_id = donars.find_one({'name' : session['username']},{"_id" :1})
        lis = []
        lat = donars.find_one({'name' : session['username']},{"lat" :1})
        lon = donars.find_one({'name' : session['username']},{"lon" :1})
        lsbanks = banks.find()
        # print(banks.query.f)
        for i in lsbanks:
            # print(i.lat)
            loc = Nominatim(user_agent="GetLoc")
 
            # entering the location name
            print(i['address'])
            getLoc = loc.geocode(i['address'])
            cords_2 = (getLoc.latitude,getLoc.longitude)
            dict={}
            dict['bank_name'] = i['name']
            dict['dist'] = geodesic((lat,lon),cords_2)
            lis.append(dict)
        sorted(lis, key=lambda j: j['dist'])
        print(lis)
        return render_template('odash.html',list = lis)
@app.route('/bank_dashboard')
def bank_dashboard():
    if 'username' in session:
        return render_template('Blood_Bank_dashboard.html')
@app.route('/hosp_dashboard')
def hosp_dashboard():
    if 'username' in session:
        banks = mongo.db.banks.find()
        return render_template('hospital_dashboard.html',banks = banks)

        

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/donar_register', methods=['POST', 'GET'])
def donar_register():
    if request.method == 'POST':
        users = mongo.db.donars
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'],'email':request.form['email'],'phno':request.form['phno'],'address':request.form['address'],'bloodgrp':request.form['bloodgrp'],'password' : hashpass,'lat':request.form['address-lat'],'lon':request.form['address-lon']})
            session['username'] = request.form['username']
            return redirect(url_for('donar_dashboard'))
        
        return 'That username already exists!'

    return render_template('donor_registration.html')
    
@app.route('/bank_register', methods=['POST', 'GET'])
def bank_register():
    if request.method == 'POST':
        users = mongo.db.banks
        blood_grps = mongo.db.bloodgroups
        
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'],'email':request.form['email'],'phno':request.form['phno'],'address':request.form['address'],'password' : hashpass,})
            session['username'] = request.form['username']
            user_id = users.find_one({'email' : request.form['email']},{'_id':1})
            blood_grps.insert_one({'bank_id':user_id, 'group_A+':0,'group_A-':0,'group_B+':0,'group_B-':0,'group_O-':0,'group_O+':0,'group_AB+':0,'group_AB-':0})
            return redirect(url_for('bank_dashboard'))
        
        return 'That username already exists!'

    return render_template('bloodbank_register.html')

    
@app.route('/hosp_register', methods=['POST', 'GET'])
def hosp_register():
    if request.method == 'POST':
        users = mongo.db.hospital
        existing_user = users.find_one({'email' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'],'email':request.form['email'],'phno':request.form['phno'],'address':request.form['address'],'password' : hashpass,})
            session['username'] = request.form['username']
            return redirect(url_for('hosp_dashboard'))
        
        return 'That username already exists!'

    return render_template('hospital_register.html')

@app.route('/packet_update/<name>',methods=['POST','GET'])
def packet_update(name):
    users = mongo.db.banks
    if(request.method=='POST'):
        user_name = session['username']
        user_id = users.find_one({'email' : user_name},{'_id':1})
        bloodgroups = mongo.db.bloodgroups.find_one({'bank_id':user_id})
        mongo.db.bloodgroups.update_one({name:bloodgroups[name]},{"$set":{name:bloodgroups[name]+1}})
        return redirect(url_for('bank_login'))
    return render_template('Blood_Bank_dashboard.html',bloodgroups = bloodgroups)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/items",methods = ["POST","GET"])
def res():
    if request.method == "POST":
        item = request.form["data"]
        return redirect(url_for("req", name = item))
    else :
        return render_template("form.html")

@app.route("/<name>")
def req(name):
    try:
        db = mongo.db
        patterns = name.split(' ')
        # return name
        # # return str(len(patterns))
        if(len(patterns) > 1):
            pat = str(patterns[0])
            # rdata = []
            rdata = db.values.find({"name": {'$regex':pat , '$options':'i'}}, {"_id":0})
            rdata = list(rdata)
            for i in range(1,len(patterns)):
                odata = db.values.find({"name": {'$regex':patterns[i] , '$options':'i'}}, {"_id":0})
                odata = list(odata)
                rdata = [value for value in rdata if value in odata]
            return rdata
        pattern1 ='^' + name
        pattern2 = "raw"
        pattern3 = "ground"
        odata = db.values.find({"name": {'$regex':pattern1 , '$options':'i'}}, {"_id":0})
        odata = list(odata)
        # return odata
        if(len(odata) == 0):
            odata = db.values.find({"name": {'$regex':name , '$options':'i'}}, {"_id":0})
            odata = list(odata)
            print(odata)
            return odata
            if(len(odata) == 1):
                return odata
        elif(len(odata) == 1 or  len(odata) == 2):
            return odata
        ndata = db.values.find({"name": {'$regex':pattern2 , '$options':'i'}}, {"_id":0})
        ndata = list(ndata)
        # return ndata
        rdata = [value for value in odata if value in ndata]
        # return rdata
        if(len(rdata) == 1):
            return rdata
        fdata = db.values.find({"name": {'$regex':pattern3 , '$options':'i'}}, {"_id":0})
        fdata = list(fdata)
        rfdata = [value for value in fdata if value in rdata]
        if(len(rfdata) == 0):
            return list(rdata)
        return rfdata
    except Exception as ex:
        print(ex)
        return response(response = json.dumps({"message":"cannot read users"}),status = 500, mimetype = "application/json")

@app.route('/items1/items2',methods=['GET','POST'])
def items2():
    return render_template('cart.html')
@app.route('/items1',methods=['GET','POST'])
def items1():
    return render_template('button.html')

@app.route('/item/<name>')
def item_d(name):
    item_data = req(name)[0]
    k = item_data
    vit=(float(k['vitamin_a'][0:2])+float(k['vitamin_b12'][0:2])+float(k['vitamin_b6'][0:2])+float(k['vitamin_c'][0:2])+float(k['vitamin_d'][0:2])+float(k['vitamin_e'][0:2])+float(k['vitamin_k'][0:2]))
    pro=item_data['protein']
    carbs=item_data['carbohydrate']
    fat=item_data['total_fat']
    cal=item_data['calories']
    n=name.upper()
    return render_template('item.html',vit=vit,pro=pro,carbs=carbs,fat=fat,cal=cal,name=n)
if __name__ == "__main__" :
    app.run(port = 80,debug = True)












