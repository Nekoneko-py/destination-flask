from flask import Flask
from flask import render_template,redirect,request
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required
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
    waypoint = db.relationship('Waypoint',backref='element')
    user_id = db.Column(db.Integer,db.ForeignKey(User.id))

class Waypoint(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    waypoint = db.Column(db.String(30),nullable=False)
    element_id = db.Column(db.Integer,db.ForeignKey(Element.id))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/",methods=['GET','POST'])
def input():
    
        return render_template('input.html')

@app.route("/result",methods=['GET','POST'])
def result():
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
        
        return render_template('result.html',start=start,destinations=destinations,end=end,mode=mode,modeName=modeName)

@app.route("/input/members",methods=['GET','POST'])
@login_required
def members_input():
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

        element = Element(start=start,end=end,mode=mode,modeName=modeName)
        db.session.add(element)
        db.session.commit

        waypoint = Waypoint(destinations=destinations)
        db.session.add(waypoint)
        db.session.commit
        return redirect('/result')
    else:
        return render_template('members_input.html')

@app.route("/<int:id>/result/members",methods=['GET','POST'])
@login_required
def members_result(id):
    if request.method == 'POST':
        element = Element.query.get(id)
        start = element.origin
        destinations = element.waypoint
        end = element.destination
        mode = element.mode
        modeName = element.modeName
        
        return render_template('members_result.html',start=start,destinations=destinations,end=end,mode=mode,modeName=modeName)

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

@app.route('/mypage/members',methods=['GET','POST'])
@login_required
def mypage():
    if request.method == 'GET':
        elements = Element.query.all()
        return render_template('mypage.html',elements=elements)

    if __name__ == "__main__":
        app.run()