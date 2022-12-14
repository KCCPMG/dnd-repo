from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerRangeField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
import re


############ Custom Validators ############

def FloatOrNone(form, field):
  """Returns without error if field has no input or if field is float"""
  if (len(field.data)) == 0:
    return
  else:
    return


def SlugFormatRequired(form, field):

  if len(re.findall("[a-zA-Z0-9\-_]", field.data)) != len(field.data):
    raise ValidationError("Please use only letters, numbers, and the characters '-' and '_' in the slug")


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

  text = TextAreaField("Comment", validators=[DataRequired(message="Cannot create empty comment"), Length(max=1000)])


class ArmorForm(FlaskForm):
  """Form for creating a new Armor Item"""

  slug = StringField("URL", validators=[DataRequired(message="URL is required"), SlugFormatRequired])
  name = StringField("Name", validators=[DataRequired(message="Name is required")])
  category = SelectField("Armor Category", choices=['No Armor', 'Light Armor', 'Medium Armor', "Heavy Armor", 'Spell','Class Feature', 'Shield'])
  ac_base = IntegerField("AC Base", validators=[Optional()])

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
  


class WeaponForm(FlaskForm): 
  
  slug = StringField("URL", validators=[DataRequired(message="URL is required"), SlugFormatRequired])
  name = StringField("Name", validators=[DataRequired(message="Name is required")])
  bonus = IntegerField("Bonus", validators=[Optional()])
  weapon_category = SelectField("Weapon Category", choices=['Simple Melee Weapons', 'Simple Ranged Weapons', 'Martial Melee Weapons', 'Martial Ranged Weapons'])
  cost_in_gp = FloatField("Cost (In Gold Points)", validators=[Optional()])
  weight = FloatField("Weight (In lbs.)", validators=[Optional()])

  wp_finesse = BooleanField("finesse")
  wp_heavy = BooleanField("heavy")
  wp_light = BooleanField("light")
  wp_loading = BooleanField("loading")
  wp_reach = BooleanField("reach")
  wp_special = BooleanField("special")
  wp_two_handed = BooleanField("two-handed")
  
  
  wp_ammunition = BooleanField("ammunition")
  
  # lower and upper bounds
  ammo_range_lower_bound = IntegerField("Max Range", validators=[Optional()])
  ammo_range_upper_bound = IntegerField("With Disadvantage", validators=[Optional()])
  
  
  wp_thrown = BooleanField("thrown")
  
  # lower and upper bounds
  thrown_range_lower_bound = IntegerField("Max Range", validators=[Optional()])
  thrown_range_upper_bound = IntegerField("With Disadvantage", validators=[Optional()])

  wp_versatile = BooleanField("versatile")
  # alternate damage 
  versatile_dmg_dice_no = IntegerField("No. of Dice", validators=[Optional()])
  versatile_dmg_dice_sides = SelectField("Die Sides", choices=['', 2,4,6,8,10,12,20,100])

  # damage rolls
  first_weapon_damage_dice_no = IntegerField("No. of Dice", validators=[Optional()])
  first_weapon_damage_die_sides = SelectField("Die Sides", choices=['', 2,4,6,8,10,12,20,100])
  first_weapon_damage_flat_damage = IntegerField("Flat Damage", validators=[Optional()])
  first_weapon_damage_type = SelectField("Damage Type", choices=['', 'bludgeoning', 'piercing', 'slashing', 'acid', 'poison', 'fire', 'cold', 'force', 'lightning', 'thunder', 'necrotic', 'psychic', 'radiant'])

  second_weapon_damage_dice_no = IntegerField("No. of Dice", validators=[Optional()])
  second_weapon_damage_die_sides = SelectField("Die Sides", choices=['',2,4,6,8,10,12,20,100])
  second_weapon_damage_flat_damage = IntegerField("Flat Damage", validators=[Optional()])
  second_weapon_damage_type = SelectField("Damage Type", choices=['', 'bludgeoning', 'piercing', 'slashing', 'acid', 'poison', 'fire', 'cold', 'force', 'lightning', 'thunder', 'necrotic', 'psychic', 'radiant'])

  third_weapon_damage_dice_no = IntegerField("No. of Dice", validators=[Optional()])
  third_weapon_damage_die_sides = SelectField("Die Sides", choices=['', 2,4,6,8,10,12,20,100])
  third_weapon_damage_flat_damage = IntegerField("Flat Damage", validators=[Optional()])
  third_weapon_damage_type = SelectField("Damage Type", choices=['', 'bludgeoning', 'piercing', 'slashing', 'acid', 'poison', 'fire', 'cold', 'force', 'lightning', 'thunder', 'necrotic', 'psychic', 'radiant'])


class SpellForm(FlaskForm): 
  slug = StringField("URL", validators=[DataRequired(message="URL is required"), SlugFormatRequired])
  name = StringField("Name", validators=[DataRequired(message="Name is required")])
  description = TextAreaField("Description", validators=[DataRequired(message="Description is required")])
  higher_level = TextAreaField("At Higher Levels", validators=[DataRequired(message="At higher levels is required (can simply be 'N/A')")])
  page = IntegerField("Page", validators=[Optional()])
  spell_range = StringField("Range", validators=[DataRequired(message="Spell Range is required")])
  material = StringField("Material")
  ritual = BooleanField("Ritual")
  duration = StringField("Duration", validators=[DataRequired(message="Duration is required")])
  concentration = BooleanField("Concentration")
  casting_time = StringField("Casting Time", validators=[DataRequired(message="Casting Time is required")])
  level = IntegerField("Level", validators=[DataRequired(message="Level is required (0 for Cantrip)")])
  magic_school = SelectField("Magic School", choices=["illusion", "transmutation", "conjuration", "necromancy", "evocation", "abjuration", "enchantment", "divination"])
  circles = StringField("Circles")
  spell_component_v = BooleanField("Verbal (V)")
  spell_component_s = BooleanField("Somatic (S)")
  spell_component_m = BooleanField("Material (M)")
  

class PlayerClassForm(FlaskForm):
  slug = StringField("URL", validators=[DataRequired(message="URL is required"), SlugFormatRequired])
  name = StringField("Name", validators=[DataRequired(message="Name is required")])
  description = TextAreaField("Description (Markdown Compatible)", validators=[DataRequired(message="Description is required")])
  hit_die = SelectField("Hit Die (d:)", choices = [2, 4, 6, 8, 10, 12, 20, 100]) 
  base_hp_at_1st_level = IntegerField("Base HP at 1st Level")
  tool_proficiency = StringField("Proficient Tools", validators=[DataRequired(message="Tool Proficiency is required")])
  skill_proficiency = StringField("Proficient Skills",  validators=[DataRequired(message="Skill Proficiency is required")])
  starting_equipment = StringField("Starting Equipment", validators=[DataRequired(message="Starting Equipment is required")])
  table = TextAreaField("Table", validators=[DataRequired(message="Table is required (can be 'N/A')")])
  spellcasting_ability = SelectField("Spellcasting Ability", choices=["", "Wisdom", "Intelligence", "Charisma"])
  subtypes_name = StringField("Subtypes Name")
  armor_proficiency_none = BooleanField("No Armor")
  armor_proficiency_light = BooleanField("Light Armor")
  armor_proficiency_medium = BooleanField("Medium Armor")
  armor_proficiency_heavy = BooleanField("Heavy Armor")
  armor_proficiency_spell = BooleanField("Spell")
  armor_proficiency_class_feature = BooleanField("Class Feature")
  armor_proficiency_shield = BooleanField("Shield")
  
  prof_weapons = StringField("Weapons Proficiencies")
   
  saving_throw_str = BooleanField("Strength")
  saving_throw_dex = BooleanField("Dexterity")
  saving_throw_con = BooleanField("Constitution")
  saving_throw_wis = BooleanField("Wisdom")
  saving_throw_int = BooleanField("Intelligence")
  saving_throw_cha = BooleanField("Charisma")

  # Future feature to connect spells to a class
  # homebrew_spell_slugs = 
  # api_spell_slugs = 