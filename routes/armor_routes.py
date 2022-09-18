from flask import render_template, flash, redirect
from forms import ArmorForm, CommentForm
import json
import requests
from models import db, Armor, ArmorCategory, ArmorComment
from flask import Blueprint, g
from utils import get_comment_time, BASE_URL


armor = Blueprint('armor', __name__, template_folder='templates')

@armor.route('/')
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
  return render_template('armor_list.jinja', armors=armors, form=form)


@armor.route('/<slug>', methods=['GET'])
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


@armor.route('/new', methods=['POST'])
def add_armor():

  def rerender_failed_form():
    flash("Failed to create Armor")
    response = requests.get(BASE_URL + 'armor')
    armors = response.json()['results']
    
    db_armors = Armor.query.all()
    compat_armors = []
    for armor in db_armors:
      armor_dict = json.loads(armor.to_compat_json())
      armor_dict['author'] = armor.author
      compat_armors.append(armor_dict)

    armors += compat_armors

    return render_template('armor_list.jinja', armors=armors, form=form)
  
  form = ArmorForm()

  if form.validate_on_submit():
    valid = True

    if requests.get(BASE_URL + f'armor/{form.slug.data}'):
      form.slug.errors.append("URL is not unique")
      valid = False
    elif Armor.query.get(form.slug.data):
      form.slug.errors.append("URL is not unique")
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
        flash("Armor Created!")
        return redirect(f'/armor/{form.slug.data}')
      except Exception as e:
        print(e)
        return rerender_failed_form()
    else:
      return rerender_failed_form()
  else:
    # form.validate_on_submit failed
    return rerender_failed_form()


@armor.route('/<slug>/add-comment', methods=['POST'])
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
