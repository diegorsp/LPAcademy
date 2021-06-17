from main import db, login_manager
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(64),unique=True, index = True)
    username = db.Column(db.String(64), unique = True, index=True) 
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=True)
    token = db.Column(db.Integer,default=0)



    def confirm(self,token):
        if int(token) != int(self.token):
            return False
        self.confirmed = True
        db.session.add(self)
        return True
        

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User %r>' % self.username



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))








class Quiz(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.Text, nullable=False)
    questions = db.relationship('Question', backref='quiz',lazy=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Quiz:'{}'>".format(self.title)

class Question(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    body = db.Column(db.Text, nullable= False)
    quiz_id = db.Column(db.Integer,db.ForeignKey('quiz.id'), nullable=False)
    alternatives= db.relationship('Alternative',backref='question',lazy=True)

    def __init__(self,body):
        self.body = body

    def __repr__(self):
        return "<Question: '{}'>".format(self.body)


class Alternative(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text, nullable=False)
    isCorrect = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),nullable=False)

    def __init__(self,body,isCorrect):
        self.body = body
        self.isCorrect = isCorrect

    def __repr__(self):
        return "<Alternative: '{}' / Correct: '{}'>".format(self.body,self.isCorrect)


 
class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.Integer,db.ForeignKey('question.id'),nullable=False)
    isCorrect = db.Column(db.Boolean)




class Result(db.Model):
    pk = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    score = db.Column(db.Integer,default=0)
    
    def __init__(self, user,score):
        self.user = user
        self.score = score