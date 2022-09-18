from flask import render_template, flash, redirect
from forms import WeaponForm, CommentForm
import json
import requests
from models import db, Weapon, WeaponCategory, WeaponProperty, WeaponComment
from flask import Blueprint, g
from utils import get_comment_time, BASE_URL

weapons = Blueprint('weapons', __name__, template_folder='templates')

@weapons.route('/weapons', methods=['GET'])
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


@weapons.route('/new', methods=['POST'])
def add_weapon():

  def rerender_failed_form():
    flash("Failed to create Weapon")
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

    return render_template('weapon_list.jinja', weapons=compat_weapons, form=form)

  form = WeaponForm()

  if form.validate_on_submit():
    valid = True

    if requests.get(BASE_URL + f'weapons/{form.slug.data}'):
      form.slug.errors.append("URL is not unique")
      valid = False
    elif Weapon.query.get(form.slug.data):
      form.slug.errors.append("URL is not unique")
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
        # flash("Failed to create Weapon")
        return rerender_failed_form()
        # for error in form.errors:
        #   flash(error)
        # return redirect('/weapons')
    else:
      # flash("Failed to create Weapon")
      return rerender_failed_form()
      # flash("failed validation")
      # for error in form.errors:
      #   flash(error)
      # return redirect('/weapons')
  else:
    # flash("Failed to create Weapon")
    return rerender_failed_form()
    # flash("failed validation")
    # for error in form.errors:
    #   flash(error)
    # return redirect('/weapons')



@weapons.route('/<slug>', methods=['GET'])
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

@weapons.route('/<slug>/add-comment', methods=['POST'])
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
