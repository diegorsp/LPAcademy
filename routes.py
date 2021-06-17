from main import app,mail
from models import *
from forms import *
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from random import randint, random, sample

def send_email(to,subject,template,**kwargs):
    msg = Message(subject, sender= app.config['MAIL_DEFAULT_SENDER'],
    recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    mail.send(msg)

@app.context_processor
def utility_processor():
    def random4(question):
        order = [0,1,2,3]
        order = sample(order,4)
        alternatives = []
        for number in order:
            alternatives.append(question.alternatives[number])
        return alternatives
    return dict(random4=random4)


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static',filename='img/icon.png'))


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next= url_for('index')
            return redirect(next)
        flash("Senha ou Login Inválidos")
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você foi deslogado.")
    return redirect(url_for('index'))


@app.before_request
def before_request():
    if  current_user.is_authenticated and not current_user.confirmed and request.endpoint != 'confirm' and request.endpoint !='static' and request.endpoint !='favicon' and request.endpoint != 'logout':
        print(request.endpoint)
        return render_template('unconfirmed.html')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        token = randint(0,100)
        user = User(email=form.email.data, username=form.username.data,password=form.password.data,token=token) 
        db.session.add(user)
        db.session.commit()

        send_email(user.email, "Confirme seu Email", 'confirm', user=user,token=token)

        flash("Um email de confirmação foi enviado para o seu email.")
        return redirect(url_for('index'))
    return render_template('register.html',form=form)
    

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Sua conta está confirmada!')
    else:
        flash('Seu link de confirmação é inválido ou já expirou.')
    return redirect(url_for('index'))  

@app.route('/perfil')
@login_required
def perfil():
    return render_template('profile.html')


@app.route('/jogar', methods=['GET','POST'])
@login_required
def jogar():
    quiz_available = True
    all_questions = Question.query.all()
    questions_list = []
    for question in all_questions:
        questions_list.append(question)
    questions_list= sample(questions_list,5)

    respostas = Answer.query.filter_by(user=current_user.id)
    if respostas.count() != 0:
        quiz_available = False
    
    return render_template('jogar.html',quiz_available=quiz_available, questions_list=questions_list)



@app.route('/quiz-result', methods=['GET','POST'])
def resultado():
    score=0
    question_points = 50
    questions_query =list(request.form)
    questions =[]
    correct_answers = []
    responses = []
  



    for question in questions_query:
        questions.append(question)
        
    #To pegando as respostas corretas para comparar com as respostas dadas
    for question in questions_query: 
        question_id = Question.query.filter_by(body=question).first().id
        correct_answers.append(Alternative.query.filter_by(question_id = question_id, isCorrect = True).first().body)
      
    #checo se a pergunta foi respondida e coloca na lista de respostas
    for question in questions: 
        if (question in list(request.form)):
            
            responses.append((request.form.getlist(question)[0]))
        else:
            responses.append('Não respondida')

  
    for correct_answer in correct_answers:
       
        for response in responses:
            if correct_answer == response:
                score = score + question_points
            
   
    # até aqui tudo certo
    ziped = zip(questions_query, responses, correct_answers)
  
    result = Result(user=current_user.username,score=score)
    db.session.add(result)
    db.session.commit()
    
    return render_template('quizresult.html',ziped=ziped,questions_query=questions_query, responses=responses,score=score)    
        

@app.route('/placar')
def placar():
    allusers=[]
    allusersquery = User.query.order_by(User.username).all()
    
    for user in allusersquery:
        allusers.append(user.username)
    allusers = sorted(allusers,key=str.lower)
    print(allusers)
    scores =[]
    real_bests = []

    for user in allusers:        
        mybest = Result.query.filter_by(user=user).all()
        if len(mybest)>0:
            for result in mybest:
                scores.append(result.score)
            real_bests.append(max(scores))
            scores=[]
        else:
            real_bests.append(0)
    ziped = zip(allusers, real_bests)
    



    return render_template('placar.html',ziped=ziped)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

#Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


