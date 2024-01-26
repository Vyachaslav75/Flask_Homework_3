from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from registerform import RegisterForm
from flask_wtf.csrf import CSRFProtect
from models import db, User


app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')
    

def add_user(first_name, last_name, email, password):
    user = User(firstname=first_name, lastname=last_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

@app.route('/')
def base_page():
    return render_template('base.html')
    
@app.route('/register/', methods=['GET', 'POST'])
@csrf.exempt
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        add_user(first_name, last_name, email, password)
        print(first_name, last_name, email, password)
    
    return render_template('register.html', form=form)  
    
    
if __name__ == '__main__':
    app.run(debug=True)