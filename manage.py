from main import app,db,migrate
from main import User,Quiz,Question,Alternative

@app.shell_context_processor
def make_shell_context():
    return dict(app=app,db=db,User=User,Quiz=Quiz,Question=Question,Alternative=Alternative,
     migrate=migrate)

