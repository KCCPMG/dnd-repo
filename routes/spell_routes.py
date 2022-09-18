from flask import render_template, flash, redirect
from forms import SpellForm, CommentForm
import json
import requests
from models import db, Spell, MagicSchool, SpellComment
from flask import Blueprint, g
from utils import get_comment_time, BASE_URL

spells = Blueprint('spells', __name__, template_folder='templates')

@spells.route('/', methods=['GET'])
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


@spells.route('/new', methods=['POST'])
def add_spell():
  
  def rerender_failed_form():
    flash("Failed to create Spell")
    response = requests.get(BASE_URL + 'spells')
    spells = response.json()['results']

    db_spells = Spell.query.all()
    compat_spells = []
    for spell in db_spells:
      spell_dict = json.loads(spell.to_compat_json())
      spell_dict['author'] = spell.author
      compat_spells.append(spell_dict)

    spells += compat_spells

    return render_template('spell_list.jinja', spells = spells, form = form)


  form = SpellForm()

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
      return rerender_failed_form()
  else:
    print(form.errors)
    return rerender_failed_form()


@spells.route('/<slug>', methods=['GET'])
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

@spells.route('/<slug>/add-comment', methods=['POST'])
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

