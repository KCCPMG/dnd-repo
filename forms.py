import email
from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SelectMultipleField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, EqualTo



############ Custom Validators ############

def FloatOrNone(form, field):
  """Returns without error if field has no input or if field is float"""
  if (len(field.data)) == 0:
    return
  else:
    return


############ Forms ############

class LoginForm(FlaskForm):
  """Login form."""

  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[Length(min=6, max=-1, message="password must be at least 6 characters")])


class SignupForm(FlaskForm):
  """Signup form."""

  username = StringField('Username', validators=[DataRequired()])
  email = StringField('E-mail', validators=[Email()])
  password = PasswordField("Password", validators=[Length(min=6,  message="password must be at least 6 characters")])
  confirm_password = PasswordField("Confirm Password", validators=[EqualTo('password', "Passwords must match")])

class CommentForm(FlaskForm):
  """Form for Comments (across types)"""

  text = TextAreaField("Comment", validators=[DataRequired(), Length(max=1000)])


class ArmorForm(FlaskForm):
  """Form for creating a new Armor Item"""

  slug = StringField("URL", validators=[DataRequired()])
  name = StringField("Name")
  # my_creation = BooleanField("My Creation")
  category = SelectField("Armor Category", choices=['No Armor', 'Light Armor', 'Medium Armor', "Heavy Armor", 'Spell','Class Feature', 'Shield'])
  ac_base = IntegerField("AC Base", validators=[Optional()])

  # modifier_attributes = SelectMultipleField("Ability Modifiers", choices=['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Intelligence', 'Charisma'])

  modifier_strength = BooleanField('Strength') 
  modifier_dexterity = BooleanField('Dexterity')
  modifier_constitution = BooleanField('Constitution')
  modifier_wisdom = BooleanField('Wisdom')
  modifier_intelligence = BooleanField('Intelligence')
  modifier_charisma = BooleanField('Charisma')

  max_modifier = IntegerField("Maximum ability modifier", validators=[Optional()])
  strength_required = IntegerField("Strength Required", validators=[Optional()])
  cost_in_gp = FloatField("Cost (In Gold Points)", validators=[Optional()])
  weight = FloatField("Weight (In lbs.)", validators=[Optional()])
  stealth_disadvantage = BooleanField("Stealth Disadvantage?")
  
  # document_slug = SelectField("Document Reference Slug (For open5e.com)", choices=["None", 'wotc-srd', 'dmag', 'o5e'])
  # document_title = SelectField("Document Reference", choices=["None", 'Systems Reference Document', 'Deep Magic for 5th Edition', 'Open5e OGL'])
  # document_license = SelectField("open5e legal reference", choices=['None', 'http://open5e.com/legal'])



class WeaponForm(FlaskForm): 
  slug = StringField("URL", validators=[DataRequired()])
  name = StringField("Name")


class SpellForm(FlaskForm): 
  slug = StringField("URL", validators=[DataRequired()])
  name = StringField("Name")


class PlayerClassForm(FlaskForm):
  slug = StringField("URL", validators=[DataRequired()])
  name = StringField("Name")