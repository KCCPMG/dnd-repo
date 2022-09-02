from dataclasses import dataclass
from flask import Flask, redirect, jsonify, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
import json

from models import db, connect_db, User, Armor, ArmorComment, ArmorCategory
from forms import CommentForm, LoginForm, ArmorForm

BASE_URL = 'https://api.open5e.com/'

app = Flask(__name__, root_path=os.path.dirname(os.path.realpath(__file__)))

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///dnd-repo'))
app.config['SECRET_KEY'] = 'temp_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_ECHO']

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

############ Index ############

@app.route('/', methods=['GET'])
def get_index():
  form = LoginForm()
  return render_template('index.html', form=form)


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
    flash("Oh no it didn't work")
  
  return redirect("/")


@app.route('/home')
def get_home():

  return render_template('home.html')

############ Armor ############

@app.route('/armor', methods=['GET'])
def get_armors():
  response = requests.get(BASE_URL + 'armor')
  armors = response.json()['results']
  armors += Armor.query.all()
  form = ArmorForm(my_creation=True)
  return render_template('armor_list.html', armors=armors, form=form)


@app.route('/armor/new', methods=['POST'])
def add_armor():
  
  form = ArmorForm()

  # for field in form:
  #   print(field.label, ":", field.data, "validation:", field.validate(form))
  #   if field.errors:
  #     print("Errors:")
  #     for error in field.errors:
  #       print(error)

  if form.validate_on_submit():
    valid = True

    # form.slug.data

    if requests.get(BASE_URL + f'armor/{form.slug.data}'):
      flash("URL is not unique")
      valid = False
    elif Armor.query.get(form.slug.data):
      flash("URL is not unique")
      valid = False


    # form.name.data

    category_id = None
    found_armor_cat_list = ArmorCategory.query.filter(ArmorCategory.name==form.category.data).all()
    if not found_armor_cat_list:
      flash("Invalid Armor Category")
      valid=False
    else:
      category_id = found_armor_cat_list[0].id



    # form.ac_base.data

    # form.modifier_strength
    # form.modifier_dexterity
    # form.modifier_constitution
    # form.modifier_wisdom
    # form.modifier_intelligence
    # form.modifier_charisma

    mod_fields = [form.modifier_strength, form.modifier_dexterity, form.modifier_constitution, form.modifier_wisdom, form.modifier_intelligence,form.modifier_charisma]

    modifier_attributes = [modifier.label.text for modifier in mod_fields if modifier.data is True]

    # form.max_modifier
    # form.strength_required
    # form.cost_in_gp
    # form.weight
    # form.stealth_disadvantage

    if valid:

      try:
        new_armor = Armor.create_armor(slug=form.slug.data,
                                      name=form.name.data,
                                      document__slug__id=None,
                                      document__license_url=None,
                                      document__title__id=None,
                                      category_id=category_id,
                                      ac_base=form.ac_base.data,
                                      modifier_attributes=modifier_attributes,
                                      max_modifier=form.max_modifier.data,
                                      strength_required=form.strength_required.data,
                                      cost_in_gp=form.cost_in_gp.data,
                                      weight=form.weight.data,
                                      stealth_disadvantage=form.stealth_disadvantage.data,
                                      author_user_id=g.user.id )
        db.session.commit()
        flash("Armor Created")
        return redirect(f'/armor/{form.slug.data}')
      except Exception as e:
        print(e)
        flash("Something Went Wrong")
        return redirect('/armor')

    else:
      flash("Failed to create Armor")
      return redirect('/armor')

  else:
    flash("Failed to create Armor")
    return redirect('/armor')


@app.route('/armor/<slug>', methods=['GET'])
def get_armor(slug):
  """Get an individual piece of armor from API *or* local db"""
  armor = None
  comments = None
  author = None

  response = requests.get(BASE_URL + f'armor/{slug}')
  # no item returns 404, which is falsy
  if response:
    armor = response.json()
  else:
    # armor = json.loads(Armor.to_compat_json(Armor.query.get(slug)))
    found_armor = Armor.query.get(slug)
    author = found_armor.author
    armor = json.loads(found_armor.to_compat_json())

  if armor:
    comments = Armor.get_comments(slug)
    comment_form = CommentForm()

  return render_template('armor_item.html', armor=armor, author=author, comments=comments, comment_form=comment_form)


@app.route('/armor/<slug>/add-comment', methods=['POST'])
def add_comment(slug):

  form = CommentForm()

  if form.validate_on_submit():
    armor_comment = ArmorComment.add_comment(slug, g.user.id, form.text.data)
    db.session.add(armor_comment)
    db.session.commit()
    flash("Comment Saved!")
    return redirect(f"/armor/{slug}")
  else:
    flash("Invalid")
    return redirect(f"/armor/{slug}")


############ Weapons ############


@app.route('/weapons', methods=['GET'])
def get_weapons():
  response = requests.get(BASE_URL + 'weapons')
  res_json = response.json()
  # print([result["cost"] for result in res_json["results"]])
  return jsonify(res_json)

@app.route('/weapons/<slug>', methods=['GET'])
def get_weapon(slug):
  response = requests.get(BASE_URL + f'weapons/{slug}')
  res_json = response.json()
  return res_json


############ Spells ############

@app.route('/spells', methods=['GET'])
def get_spells():
  response = requests.get(BASE_URL + 'spells')
  res_json = response.json()
  return res_json

@app.route('/spells/<slug>', methods=['GET'])
def get_spell(slug):
  response = requests.get(BASE_URL + f'spells/{slug}')
  res_json = response.json()
  return res_json


############ Classes ############

@app.route('/classes', methods=['GET'])
def get_classes():
  response = requests.get(BASE_URL + f'classes')
  res_json = response.json()
  return res_json

@app.route('/classes/<slug>', methods=['GET'])
def get_class(slug):
  response = requests.get(BASE_URL + f'classes/{slug}')
  res_json = response.json()
  return res_json