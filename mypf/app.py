from flask import Flask
from flask import render_template,redirect,request
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required,current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import os


app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SECRET_KEY"] = os.urandom(24)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(12))
    element = db.relationship('Element',backref='user')

class Element(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    origin = db.Column(db.String(30),nullable=False)
    destination = db.Column(db.String(30),nullable=False)
    mode = db.Column(db.String)
    modeName = db.Column(db.String)
    waypoint = db.relationship('Waypoint',backref='element',lazy='joined')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class Waypoint(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    waypoint = db.Column(db.String(30),nullable=True)
    element_id = db.Column(db.Integer,db.ForeignKey('element.id'))

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/",methods=['GET','POST'])
def input():
    
        return render_template('input.html')

@app.route("/result",methods=['GET','POST'])
def result():
    GOOGLE_API_KEY = os.environ['google_api_key']
    if request.method == 'POST':
        start = request.form.get('start')
        destinations = request.form.getlist('destination')
        end = request.form.get('end')
        mode = request.form.get('modeSelect')
        if mode == 'DRIVING':
            modeName = '車'
        elif mode == 'WALKING':
            modeName = '徒歩'
        elif mode == 'BICYCLING':
            modeName = '自転車'
        elif mode == 'TRANSIT':
            modeName = '交通機関'
        
        return render_template('result.html',start=start,destinations=destinations,end=end,mode=mode,modeName=modeName,GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route("/input/members",methods=['GET','POST'])
@login_required
def members_input():
    username = current_user.username
    return render_template('members_input.html',username=username)

@app.route("/result/members",methods=['GET','POST'])
@login_required
def members_result():
    GOOGLE_API_KEY = os.environ['google_api_key']
    username = current_user.username
    if request.method == 'POST':
        start = request.form.get('start')
        destinations = request.form.getlist('destination')
        end = request.form.get('end')
        mode = request.form.get('modeSelect')
        if mode == 'DRIVING':
            modeName = '車'
        elif mode == 'WALKING':
            modeName = '徒歩'
        elif mode == 'BICYCLING':
            modeName = '自転車'
        elif mode == 'TRANSIT':
            modeName = '交通機関'
        
        user_id = current_user.id
        
        element = Element(origin=start,destination=end,mode=mode,modeName=modeName,user_id=user_id)
        db.session.add(element)
        db.session.commit()

        last_element = Element.query.order_by(Element.id.desc()).first()
        element_id = last_element.id

        for destination in destinations:
            waypt = destination
            point = Waypoint(waypoint=waypt,element_id=element_id)
            db.session.add(point)
            db.session.commit()
        
        return render_template('members_result.html',start=start,destinations=destinations,end=end,mode=mode,modeName=modeName,username=username,GOOGLE_API_KEY=GOOGLE_API_KEY)

@app.route("/<int:id>/result/members/date",methods=['GET','POST'])
@login_required
def members_result_date(id):
    username = current_user.username
    element = Element.query.get(id)
    if request.method == 'GET':
        start = element.origin
        destinations = []
        end = element.destination
        mode = element.mode
        modeName = element.modeName
        for waypoint in element.waypoint:
            destination = waypoint.waypoint
            destinations.append(destination)
        
        return render_template('members_result_date.html',start=start,destinations=destinations,end=end,mode=mode,modeName=modeName,username=username)
    
#サインアップ
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username,password=generate_password_hash(password,method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

#ログイン画面
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        try:
            if check_password_hash(user.password,password):
                login_user(user)
                return redirect('/input/members')

        except:
            return render_template('login.html',error='ユーザーが見つかりませんでした')
        
    else:
        return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/mypage/members',methods=['GET','POST'])
@login_required
def mypage():
    username = current_user.username
    if request.method == 'GET':
        elements = Element.query.filter_by(user_id=current_user.id).all()
        
        return render_template('mypage.html',elements=elements,username=username)
    
@app.route('/<int:id>/delete',methods=['GET'])
@login_required
def delete(id):
    element = Element.query.get(id)
    waypoints = Waypoint.query.filter_by(element_id=id).all()
    for waypoint in waypoints:
        db.session.delete(waypoint)
    db.session.delete(element)
    db.session.commit()

    return redirect('/mypage/members')

if __name__ == "__main__":
        app.run()