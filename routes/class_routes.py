from flask import render_template, flash, redirect
from forms import PlayerClassForm, CommentForm
import json
import requests
import markdown
from models import db, PlayerClass, ClassComment, ArmorCategory, Attribute
from flask import Blueprint, g
from utils import get_comment_time, BASE_URL


classes = Blueprint('classes', __name__, template_folder='templates')

@classes.route('/', methods=['GET'])
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
  return render_template('class_list.jinja', player_classes=compat_classes, form=form, markdown=markdown)


@classes.route('/new', methods=['POST'])
def add_class():
  """Create new player class, either show errors or redirect to new page on success"""

  def rerender_failed_form():
    """helper function to rerender on any failure"""
    flash("Failed to create Class")
    response = requests.get(BASE_URL + 'classes')
    player_classes = response.json()['results']

    db_classes = PlayerClass.query.all()
    compat_classes = []

    for pc in db_classes:
      pc_dict = json.loads(pc.to_compat_json())
      pc_dict['author'] = pc.author
      compat_classes.append(pc_dict)

    player_classes += compat_classes
    return render_template('class_list.jinja', player_classes=compat_classes, form=form)


  form = PlayerClassForm()

  if form.validate_on_submit():

    valid = True

    if requests.get(BASE_URL + f'/spells/{form.slug.data}'):
      form.slug.errors.append('URL is not unique')
      valid = False
    elif PlayerClass.query.get(form.slug.data):
      form.slug.errors.append('URL is not unique')
      valid = False

    # handle armor proficiency
    armor_proficiencies = []
    for ap in [
      form.armor_proficiency_none,
      form.armor_proficiency_light,
      form.armor_proficiency_medium,
      form.armor_proficiency_heavy,
      form.armor_proficiency_spell,
      form.armor_proficiency_class_feature,
      form.armor_proficiency_shield
    ]:
      if ap.data:
        armor_proficiencies.append(ArmorCategory.query.filter(ArmorCategory.name == ap.label.text).one().id)

    # handle saving throws
    saving_throw_ids = []
    for st in [
      form.saving_throw_str,
      form.saving_throw_dex,
      form.saving_throw_con,
      form.saving_throw_wis,
      form.saving_throw_int,
      form.saving_throw_cha
    ]:
      if st.data:
        saving_throw_ids.append(Attribute.query.filter(Attribute.name == st.label.text).one().id)

    # handle spellcasting ability
    spellcasting_ability = None
    if form.spellcasting_ability.data:
      spellcasting_ability = Attribute.query.filter(Attribute.name == form.spellcasting_ability.data).one().id

    if valid:
      try:
        new_pc = PlayerClass.create_player_class(
          slug=form.slug.data,
          name=form.name.data,
          description=form.description.data,
          hit_die=int(form.hit_die.data),
          base_hp_at_1st_level=form.base_hp_at_1st_level.data,
          tool_proficiency=form.tool_proficiency.data,
          skill_proficiency=form.skill_proficiency.data,
          starting_equipment=form.starting_equipment.data,
          table=form.table.data,
          spellcasting_ability=spellcasting_ability,
          subtypes_name=form.subtypes_name.data,
          document__slug__id=None,
          document__title__id=None,
          document__license_url=None,
          author_user_id=g.user.id,
          armor_proficiencies = armor_proficiencies,
          prof_weapons = form.prof_weapons.data,
          saving_throw_ids = saving_throw_ids,
        )

        db.session.commit()
        flash("Class Created!")
        return redirect(f'/classes/{form.slug.data}')
      
      except Exception as e:
        return rerender_failed_form()
    else:
      return rerender_failed_form()
  else:
    return rerender_failed_form()


@classes.route('/<slug>', methods=['GET'])
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


@classes.route('/<slug>/add-comment', methods=['POST'])
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