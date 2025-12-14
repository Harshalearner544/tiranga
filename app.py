from flask import Flask, render_template, request, redirect, url_for 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash 
from models import db, User, Bet 
from game_logic import generate_result, ODDS

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'demo-secret' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#initialize database

db.init_app(app)

#login manager

login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'

@login_manager.user_loader 
def load_user(user_id): 
       return User.query.get(int(user_id))

@app.before_first_request 
def create_tables(): 
       db.create_all()

@app.route('/', methods=['GET', 'POST']) 
def login(): 
       if request.method == 'POST': 
           user = User.query.filter_by(username=request.              form['username']).first() 
           if user and check_password_hash(user.     password, request.form['password']):   login_user(user) 
                     return redirect(url_for('dashboard')) 
       return render_template('login.html')

@app.route('/register', methods=['GET', 'POST']) 
def register(): 
       if request.method == 'POST': 
           user = User( username=request.   form['username'],          password=generate_password_hash(request. form['password']) ) 
           db.session.add(user) 
           db.session.commit() 
           return redirect(url_for('login')) 
       return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST']) @login_required 
def dashboard(): 
       all_bets = Bet.query.all() 
       bet_choices = [b.choice for b in all_bets]

       if request.method == 'POST':
              choice = request.form['choice']
              amount = float(request.form['amount'])

              if amount <= current_user.balance:
                   number, color =      generate_result(bet_choices)
                   win = amount * ODDS.get(choice, 0) if  choice == color else 0
                   current_user.balance += win - amount

                    bet = Bet(user_id=current_user.id,choice=choice, amount=amount,  result_color=color,win_amount=win )
                    db.session.add(bet)
                    db.session.commit()

                    return render_template( 'result.html', number=number,color=color,win=win )

           return render_template('dashboard.html', balance=current_user.balance)

@app.route('/logout')
@login_required 
def logout(): 
      logout_user() 
      return redirect(url_for('login'))

if __name__ == '__main__': 
        app.run(debug=True)