from flask import Flask, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os

from models import db, connect_db, User
from forms import LoginForm, SignupForm
from env import secret


app = Flask(__name__, root_path=os.path.dirname(os.path.realpath(__file__)))


# resolve postgres / postgresql error with heroku
uri = (os.environ.get('DATABASE_URL', 'postgresql:///dnd-repo'))
if uri.startswith("postgres://"):
  uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = secret
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


CURR_USER_KEY = 'current_user_id'


def login(user):
  session[CURR_USER_KEY] = user.id

def logout():
  del session[CURR_USER_KEY]


@app.before_request
def get_user():
  if CURR_USER_KEY in session:
    g.user = User.query.get(session[CURR_USER_KEY])
  else:
    g.user = None


############ 404 ############

@app.errorhandler(404)
def get_404(e):
  return render_template('404.jinja')



############ Index ############

@app.route('/', methods=['GET'])
def get_index():

  if g.user:
    return redirect('/home')

  form = LoginForm()
  return render_template('index.jinja', form=form)


@app.route('/login', methods=['POST'])
def get_user():
  
  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate_user(form.username.data, form.password.data)
    if user:
      session[CURR_USER_KEY] = user.id
      flash(f"Hello, {user.username}!", "success")
      return redirect("/")
    else:
      flash("Authentication failed. Please check username and password.")
  else:
    flash("Error. Please try again.")
  
  return redirect("/")


@app.route('/login-guest', methods=['GET'])
def get_guest():
  user = User.query.filter(User.username == "guest").one()
  session[CURR_USER_KEY] = user.id
  flash(f"Hello, {user.username}!", "success")
  return redirect("/")


@app.route('/logout', methods=['GET'])
def logout():

  if g.user:
    del session[CURR_USER_KEY]
    g.user = None

  return redirect('/')

@app.route('/home')
def get_home():

  return render_template('home.jinja')


@app.route('/signup', methods=['GET', 'POST'])
def handle_signup():

  form = SignupForm()

  if g.user:
    flash("You're already logged in!")
    return redirect("/home")
  
  elif form.validate_on_submit():
    valid = True
    # check username
    if len(User.query.filter(User.username == form.username.data).all()) > 0:
      flash("Entered username already exists")
      valid=False
    # check email
    if len(User.query.filter(User.email == form.email.data).all()) > 0:
      flash("Account already registered to that email")
      valid=False


    if valid is True:
      try:
        user = User.create_user(email=form.email.data, 
                                username=form.username.data,unhashed_password=form.password.data)
        db.session.commit()
        session[CURR_USER_KEY] = user.id
        flash(f"Welcome to Dragon's Hoard, {user.username}!")
        return redirect('/home')
      except:
        flash("Something went wrong")
        return render_template("signup_form.jinja", form=form)
    else:
      return render_template("signup_form.jinja", form=form)

  else:
    return render_template("signup_form.jinja", form=form)

############ Armor ############


from routes.armor_routes import armor
app.register_blueprint(armor, url_prefix="/armor")


############ Weapons ############

from routes.weapon_routes import weapons
app.register_blueprint(weapons, url_prefix="/weapons")


############ Spells ############

from routes.spell_routes import spells
app.register_blueprint(spells, url_prefix='/spells')


############ Classes ############

from routes.class_routes import classes
app.register_blueprint(classes, url_prefix="/classes")