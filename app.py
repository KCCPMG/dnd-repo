from flask import Flask, redirect, jsonify, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
import json
import markdown

from models import db, connect_db, User, Armor, ArmorComment, WeaponComment, SpellComment, ClassComment, ArmorCategory, Weapon, Spell, PlayerClass, WeaponProperty, WeaponCategory, DamageType, MagicSchool
from forms import CommentForm, LoginForm, ArmorForm, SignupForm, WeaponForm, SpellForm, PlayerClassForm

BASE_URL = 'https://api.open5e.com/'

app = Flask(__name__, root_path=os.path.dirname(os.path.realpath(__file__)))

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///dnd-repo'))
app.config['SECRET_KEY'] = 'temp_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO']
# app.jinja_env.lstrip_blocks = False
# app.jinja_env.trim_blocks = False



toolbar = DebugToolbarExtension(app)

connect_db(app)


CURR_USER_KEY = 'current_user_id'

def get_comment_time(comment):
  return comment.posted_at

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

############ Index ############

@app.route('/', methods=['GET'])
def get_index():

  if g.user:
    return redirect('/home')

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
      flash("Authentication failed. Please check username and password.")
  else:
    flash("Error. Please try again.")
  
  return redirect("/")

@app.route('/logout', methods=['GET'])
def logout():

  if g.user:
    del session[CURR_USER_KEY]
    g.user = None

  return redirect('/')

@app.route('/home')
def get_home():

  return render_template('home.html')


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
        return render_template("signup_form.html", form=form)
    else:
      return render_template("signup_form.html", form=form)

  else:
    return render_template("signup_form.html", form=form)

############ Armor ############

@app.route('/armor', methods=['GET'])
def get_armors():
  response = requests.get(BASE_URL + 'armor')
  armors = response.json()['results']
  
  db_armors = Armor.query.all()
  compat_armors = []
  for armor in db_armors:
    armor_dict = json.loads(armor.to_compat_json())
    # armor.ac_string = armor_dict['ac_string']
    # armor.category = armor_dict['category']
    # armor.strength_requirement = armor_dict['strength_requirement']
    armor_dict['author'] = armor.author
    compat_armors.append(armor_dict)

  armors += compat_armors

  # armors += Armor.query.all()
  form = ArmorForm(my_creation=True)
  return render_template('armor_list.html', armors=armors, form=form)


@app.route('/armor/new', methods=['POST'])
def add_armor():
  
  form = ArmorForm()

  if form.validate_on_submit():
    valid = True

    if requests.get(BASE_URL + f'armor/{form.slug.data}'):
      flash("URL is not unique")
      valid = False
    elif Armor.query.get(form.slug.data):
      flash("URL is not unique")
      valid = False

    # check armor category before proceeding
    category_id = None
    found_armor_cat_list = ArmorCategory.query.filter(ArmorCategory.name==form.category.data).all()
    if not found_armor_cat_list:
      flash("Invalid Armor Category")
      valid=False
    else:
      category_id = found_armor_cat_list[0].id

    mod_fields = [form.modifier_strength, form.modifier_dexterity, form.modifier_constitution, form.modifier_wisdom, form.modifier_intelligence,form.modifier_charisma]

    modifier_attributes = [modifier.label.text for modifier in mod_fields if modifier.data is True]

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
    if not found_armor:
      return render_template("404.jinja")
    author = found_armor.author
    armor = json.loads(found_armor.to_compat_json())

  if armor:
    comments = Armor.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)
    comment_form = CommentForm()

  return render_template(
    'armor_item.jinja', 
    armor=armor, 
    author=author, 
    comments=comments, 
    comment_form=comment_form, 
    form_action=f"/armor/{slug}/add-comment")


@app.route('/armor/<slug>/add-comment', methods=['POST'])
def add_armor_comment(slug):
  """Add comment to a single armor item"""
  form = CommentForm()

  if form.validate_on_submit():
    armor_comment = ArmorComment.add_comment(slug, g.user.id, form.text.data)
    db.session.add(armor_comment)
    db.session.commit()
    flash("Comment Saved!")
    return redirect(f"/armor/{slug}")
  else:
    flash("Failed to add comment")
    armor = None
    author = None
    comments = Armor.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)

    response = requests.get(BASE_URL + f'armor/{slug}')
    # no item returns 404, which is falsy
    if response:
      armor = response.json()
    else:
      found_armor = Armor.query.get(slug)
      if not found_armor:
        return render_template("404.jinja")
      author = found_armor.author
      armor = json.loads(found_armor.to_compat_json())

    return render_template(
      'armor_item.jinja', 
      armor=armor, 
      author=author, 
      comments=comments, 
      comment_form=form, 
      form_action=f"/armor/{slug}/add-comment")


############ Weapons ############


@app.route('/weapons', methods=['GET'])
def get_weapons():
  response = requests.get(BASE_URL + 'weapons')
  weapon_results = response.json()['results']
  weapons = [json.loads(Weapon.api_doc_to_compat_json(wr)) for wr in weapon_results]

  db_weapons = Weapon.query.all()
  compat_weapons = []

  for weapon in db_weapons:
    weapon_dict = json.loads(weapon.to_compat_json())
    weapon_dict['author'] = weapon.author
    compat_weapons.append(weapon_dict)

  compat_weapons += weapons

  form = WeaponForm(my_creation=True)
  return render_template('weapon_list.jinja', weapons=compat_weapons, form=form)


@app.route('/weapons/new', methods=['POST'])
def add_weapon():

  form = WeaponForm()

  if form.validate_on_submit():
    valid = True

    if requests.get(BASE_URL + f'weapons/{form.slug.data}'):
      flash("URL is not unique")
      valid = False
    elif Weapon.query.get(form.slug.data):
      flash("URL is not unique")
      valid = False


    ammo_property = None
    thrown_property = None
    versatile_property = None

    # check ammunition properties before proceeding
    if form.wp_ammunition.data:
      if not (form.ammo_range_lower_bound.data and form.ammo_range_upper_bound.data):
        flash("If setting the ammunition property, both range inputs must have valid input")
        valid = False
        
      if valid:
        if form.ammo_range_lower_bound.data < 0:
          flash("Range cannot be less than 0")
          valid = False

      if valid:
        if form.ammo_range_upper_bound.data < form.ammo_range_lower_bound.data:
          flash("'With Disadvantage' range must be equal to or greater than the max range")
          valid = False

      if valid:
        provisional_property = f'ammuntion (range {form.ammo_range_lower_bound.data}/{form.ammo_range_upper_bound.data})'

        check = WeaponProperty.query.filter(WeaponProperty.name == provisional_property).all()
        if len(check) == 0:
          ammo_property = WeaponProperty(name=provisional_property)
          db.session.add(ammo_property)
        else:
          ammo_property = check[0]

        
    # check thrown properties before proceeding
    if form.wp_thrown.data:
      if not (form.thrown_range_lower_bound.data and form.thrown_range_upper_bound.data):
        flash("If setting the thrown property, both range inputs must have valid input")
        valid = False
      if form.thrown_range_lower_bound.data < 0:
        flash("Range cannot be less than 0")
        valid = False
      if form.thrown_range_upper_bound.data < form.thrown_range_lower_bound.data:
        flash("'With Disadvantage' range must be equal to or greater than the max range")
        valid = False
      if valid:
        provisional_property = f'ammuntion (range {form.thrown_range_lower_bound.data}/{form.thrown_range_upper_bound.data})'

        check = WeaponProperty.query.filter(WeaponProperty.name == provisional_property).all()
        if len(check) == 0:
          thrown_property = WeaponProperty(name=provisional_property)
        else:
          thrown_property = check[0]


    # check versatile properties before proceeding
    if form.wp_versatile.data:
      if not (form.versatile_dmg_dice_no.data and form.versatile_dmg_dice_sides.data):
        valid = False
        flash("If setting the versatile property, a complete damage dice roll must be included")
      if valid:
        provisional_property = f'versatile ({form.versatile_dmg_dice_no.data}d{form.versatile_dmg_dice_sides.data})'

        check = WeaponProperty.query.filter(WeaponProperty.name == provisional_property).all()
        if len(check) == 0:
          versatile_property = WeaponProperty(name=provisional_property)
        else:
          versatile_property = check[0]
    
    # resolve all property ids
    other_properties_text = [field.label.text for field in [form.wp_finesse, form.wp_heavy,form.wp_light, form.wp_loading, form.wp_reach, form.wp_special, form.wp_two_handed] if field.data]

    other_properties = [WeaponProperty.query.filter(WeaponProperty.name == p_text).one() for p_text in other_properties_text]

    all_properties = other_properties + [prop for prop in [ammo_property, versatile_property, thrown_property] if prop]

    property_ids = [prop.id for prop in all_properties]

    # get weapon category
    weapon_category_id = WeaponCategory.query.filter(WeaponCategory.name==form.weapon_category.data).one().id

    weapon_damage_rolls = []


    if form.first_weapon_damage_dice_no.data or form.first_weapon_damage_flat_damage.data:
      damage_type_id = DamageType.query.filter(DamageType.name==form.first_weapon_damage_type.data).one().id
      weapon_damage_rolls.append({
        'dice_no': form.first_weapon_damage_dice_no.data,
        'die_sides': int(form.first_weapon_damage_die_sides.data),
        'damage_type': damage_type_id,
        'flat_damage': form.first_weapon_damage_flat_damage.data,
        'weapon_slug': form.slug.data
      })

    if form.second_weapon_damage_dice_no.data or form.second_weapon_damage_flat_damage.data:
      damage_type_id = DamageType.query.filter(DamageType.name==form.second_weapon_damage_type.data).one().id
      weapon_damage_rolls.append({
        'dice_no': form.second_weapon_damage_dice_no.data,
        'die_sides': int(form.second_weapon_damage_die_sides.data),
        'damage_type': damage_type_id,
        'flat_damage': form.second_weapon_damage_flat_damage.data,
        'weapon_slug': form.slug.data
      })

    if form.third_weapon_damage_dice_no.data or form.third_weapon_damage_flat_damage.data:
      damage_type_id = DamageType.query.filter(DamageType.name==form.third_weapon_damage_type.data).one().id
      weapon_damage_rolls.append({
        'dice_no': form.third_weapon_damage_dice_no.data,
        'die_sides': int(form.third_weapon_damage_die_sides.data),
        'damage_type': damage_type_id,
        'flat_damage': form.third_weapon_damage_flat_damage.data,
        'weapon_slug': form.slug.data
      })

    if valid is True:
      try:
        Weapon.create_weapon(
          slug=form.slug.data,
          name=form.name.data,
          weapon_category=weapon_category_id,
          document__slug__id=None, 
          document__title__id=None, 
          document__license_url=None,
          cost_in_gp=form.cost_in_gp.data,
          weight=form.weight.data,
          bonus=form.bonus.data,
          author_user_id=g.user.id,
          weapon_damage_rolls=weapon_damage_rolls,
          weapon_property_assignments=property_ids
        )

        db.session.commit()
        flash("Weapon Created!")
        return redirect("/weapons")


      except Exception as e:
        print(e)
        flash("failed validation")
        for error in form.errors:
          flash(error)
        return redirect('/weapons')
    else:
      flash("failed validation")
      for error in form.errors:
        flash(error)
      return redirect('/weapons')
  else:
    flash("failed validation")
    for error in form.errors:
      flash(error)
    return redirect('/weapons')



@app.route('/weapons/<slug>', methods=['GET'])
def get_weapon(slug):
  """Get an individual weapon from API *or* local db"""
  weapon = None
  comments = None
  author = None

  response = requests.get(BASE_URL + f'weapons/{slug}')
  # no item returns 404, which is falsy
  if response:
    weapon_json = response.json()
    weapon = json.loads(Weapon.api_doc_to_compat_json(weapon_json))
  else:
    found_weapon = Weapon.query.get(slug)
    if not found_weapon:
      return render_template("404.jinja")
    author = found_weapon.author
    weapon = json.loads(found_weapon.to_compat_json())
  
  if weapon:
    comments = Weapon.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)
    comment_form = CommentForm()
  
  return render_template(
    'weapon_item.jinja',
    weapon=weapon,
    author=author,
    comments=comments, 
    comment_form=comment_form, 
    form_action=f"/weapons/{slug}/add-comment"
  )

@app.route('/weapons/<slug>/add-comment', methods=['POST'])
def add_weapon_comment(slug):
  """Add comment to a single weapon item"""
  form = CommentForm()

  if form.validate_on_submit():
    weapon_comment = WeaponComment.add_comment(slug, g.user.id, form.text.data)
    db.session.add(weapon_comment)
    db.session.commit()
    flash("Comment Saved!")
    return redirect(f"/weapons/{slug}")
  else:
    flash("Failed to add comment")
    weapon = None
    author = None
    comments = Weapon.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)

    response = requests.get(BASE_URL + f'weapons/{slug}')
    # no item returns 404, which is falsy
    if response:
      weapon_json = response.json()
      weapon = json.loads(Weapon.api_doc_to_compat_json(weapon_json))
    else:
      found_weapon = Weapon.query.get(slug)
      if not found_weapon:
        return render_template("404.jinja")
      author = found_weapon.author
      weapon = json.loads(found_weapon.to_compat_json())
    
    return render_template(
      'weapon_item.jinja',
      weapon=weapon,
      author=author,
      comments=comments, 
      comment_form=form, 
      form_action=f"/weapons/{slug}/add-comment"
    )

############ Spells ############

@app.route('/spells', methods=['GET'])
def get_spells():
  response = requests.get(BASE_URL + 'spells/?limit=1000')
  spells = response.json()['results']

  db_spells = Spell.query.all()
  compat_spells = []
  for spell in db_spells:
    spell_dict = json.loads(spell.to_compat_json())
    spell_dict['author'] = spell.author
    compat_spells.append(spell_dict)

  spells += compat_spells

  form = SpellForm(my_creation=True)
  return render_template('spell_list.jinja', spells=spells, form=form)


@app.route('/spells/new', methods=['POST'])
def add_spell():
  
  form = SpellForm()

  import pdb
  pdb.set_trace()

  if form.validate_on_submit():

    if requests.get(BASE_URL + f'spells/{form.slug.data}'):
      flash("URL is not unique")
      return redirect("/spells")
    elif Spell.query.get(form.slug.data):
      flash("URL is not unique")
      return redirect("/spells")

    spell_components = []
    if form.spell_component_v.data:
      spell_components.append("V")
    if form.spell_component_s.data:
      spell_components.append("S")
    if form.spell_component_m.data:
      spell_components.append("M")


    magic_school_id = MagicSchool.query.filter(MagicSchool.name == form.magic_school.data).one().id

    try:
      Spell.create_spell(slug=form.slug.data,
                        name=form.name.data,
                        description=form.description.data,
                        higher_level=form.higher_level.data,
                        page=form.page.data,
                        spell_range=form.spell_range.data,
                        material=form.material.data,
                        ritual=form.ritual.data,
                        duration=form.duration.data,
                        concentration=form.concentration.data,
                        casting_time=form.casting_time.data,
                        level=form.level.data,
                        magic_school=magic_school_id,
                        document__slug__id=None,
                        document__title__id=None,
                        document__license_url=None,
                        circles=form.circles.data,
                        author_user_id=g.user.id,
                        spell_components=spell_components,
                        class_slug_spell_assignments=[],
                        archetype_spell_assignments=[])
      db.session.commit()
      flash("Spell Created!")
      return redirect("/spells")
    except Exception as e:
      print(e)
      flash("Something went wrong")
      return redirect("/spells")
  else:
    print(form.errors)
    flash("Something went wrong")
    return redirect("/spells")


@app.route('/spells/<slug>', methods=['GET'])
def get_spell(slug):
  """Get an individual spell from API *or* local db"""
  spell = None
  comments = None
  author = None

  response = requests.get(BASE_URL + f'spells/{slug}')
  # no item returns 404, which is falsy
  if response:
    spell = response.json()
  else:
    found_spell = Spell.query.get(slug)
    if not found_spell:
      return render_template("404.jinja")
    author = found_spell.author
    spell = json.loads(found_spell.to_compat_json())

  if spell:
    comments = Spell.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)
    comment_form = CommentForm()

  return render_template(
    'spell_item.jinja',
    spell=spell,
    author=author,
    comments=comments, 
    comment_form=comment_form, 
    form_action=f"/spells/{slug}/add-comment"
  )

@app.route('/spells/<slug>/add-comment', methods=['POST'])
def add_spell_comment(slug):
  """Add comment to a single spell item"""
  form = CommentForm()

  if form.validate_on_submit():
    spell_comment = SpellComment.add_comment(slug, g.user.id, form.text.data)
    db.session.add(spell_comment)
    db.session.commit()
    flash("Comment Saved!")
    return redirect(f"/spells/{slug}")
  else:
    flash("Failed to add comment")
    spell = None
    author = None
    comments = Spell.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)

    response = requests.get(BASE_URL + f"spells/{slug}")

    if response:
      spell = response.json()
    else:
      found_spell = Spell.query.get(slug)
      if not found_spell:
        return render_template("404.jinja")
      author = found_spell.author
      spell = json.loads(found_spell.to_compat_json())

    return render_template(
      'spell_item.jinja',
      spell=spell,
      author=author,
      comments=comments, 
      comment_form=form, 
      form_action=f"/spells/{slug}/add-comment"
    )



############ Classes ############

@app.route('/classes', methods=['GET'])
def get_classes():
  response = requests.get(BASE_URL + f'classes')
  player_classes = response.json()['results']

  db_classes = PlayerClass.query.all()
  compat_classes = []

  for pc in db_classes:
    pc_dict = json.loads(pc.to_compat_json())
    pc_dict['author'] = pc.author
    compat_classes.append(pc_dict)

  compat_classes += player_classes

  form = PlayerClassForm(my_creation=True)
  return render_template('class_list.jinja', player_classes=compat_classes, form=form)

@app.route('/classes/new', methods=['POST'])
def add_class():
  pass

@app.route('/classes/<slug>', methods=['GET'])
def get_class(slug):
  """Get an individual class from API *or* local db"""
  pc = None
  comments = None
  author = None
  
  response = requests.get(BASE_URL + f'classes/{slug}')
    # no item returns 404, which is falsy
  if response:
    pc = response.json()
  else:
    found_pc = PlayerClass.query.get(slug)
    if not found_pc:
      return render_template("404.jinja")
    author = found_pc.author
    pc = json.loads(found_pc.to_compat_json())

  if pc:
    comments = PlayerClass.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)
    comment_form = CommentForm()

  return render_template(
    'class_item.jinja',
    pc=pc,
    author=author,
    comments=comments,
    comment_form=comment_form,
    form_action=f"/classes/{slug}/add-comment",
    markdown=markdown
  )


@app.route('/classes/<slug>/add-comment', methods=['POST'])
def add_class_comment(slug):
  """Add comment to a single player class"""

  form = CommentForm()

  if form.validate_on_submit():
    class_comment = ClassComment.add_comment(slug, g.user.id, form.text.data)
    db.session.add(class_comment)
    db.session.commit()
    flash("Comment Saved!")
    return redirect(f"/classes/{slug}")
  else:
    flash("Failed to add comment")

    pc = None
    author = None
    comments = PlayerClass.get_comments(slug)
    comments.sort(reverse=True, key=get_comment_time)
    
    response = requests.get(BASE_URL + f'classes/{slug}')
    # no item returns 404, which is falsy
    if response:
      pc = response.json()
    else:
      found_pc = PlayerClass.query.get(slug)
      if not found_pc:
        return render_template("404.jinja")
      author = found_pc.author
      pc = json.loads(found_pc.to_compat_json())

    return render_template(
      'class_item.jinja',
      pc=pc,
      author=author,
      comments=comments,
      comment_form=form,
      form_action=f"/classes/{slug}/add-comment",
      markdown=markdown
    )