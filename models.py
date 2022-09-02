from datetime import datetime
import json
import re

from sqlalchemy import exc, ForeignKey

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)



############ Validators ############

def check_slug(slug, allow_none=False):
  if allow_none is True and slug is None:
    return

  if not type(slug) is str:
    raise TypeError("slug must be a string")

  if not re.search("^[a-z0-9]+(?:-[a-z0-9]+)*$", slug):
    raise ValueError("slug must be url compatible")


def check_armor_category_id(cat_id, allow_none=False):
  if allow_none is True and cat_id is None:
    return

  if not isinstance(ArmorCategory.query.get(cat_id), ArmorCategory):
    raise ValueError(f"Invalid category_id {cat_id}")


def check_doc_slug_id(slug_id, allow_none=False):
  if allow_none is True and slug_id is None:
    return

  if not type(slug_id) is int:
    raise TypeError("slug_id must be of type int")


  if not isinstance(DocumentSlug.query.get(slug_id), DocumentSlug):
    raise ValueError("Invalid document__slug__id")


def check_doc_title_id(title_id, allow_none=False):
  if allow_none is True and title_id is None:
    return

  if not type(title_id) is int:
    raise TypeError("title_id must be of type int")

  if not isinstance(DocumentSlug.query.get(title_id), DocumentSlug):
    raise ValueError("Invalid document__title__id")


def check_doc_license_url(license_url, allow_none=False):
  if allow_none is True and license_url is None:
    return

  if not type(license_url) is int:
    raise TypeError("license_url_id must be of type int")

  if not isinstance(DocumentLicenseURL.query.get(license_url), DocumentLicenseURL):
    raise ValueError("Invalid document__license_url")


def check_int(val, key, allow_none=False):
  if allow_none is True and val is None:
    return

  if not type(val) is int:
    raise TypeError(f"Value passed to {key} must be of type int")


def check_attribute_id(attribute_id, allow_none=False):
  if allow_none is True and attribute_id is None:
    return

  if not type(attribute_id) is int:
    raise TypeError("attribute_id must be of type int")

  if not attribute_id in [1,2,3,4,5,6]:
    raise ValueError("attribute_id must be number between 1 and 6")


def check_float(val, key, allow_none=False):
  if allow_none is True and val is None:
    return

  # accept integer
  if type(val) is int:
    val = float(val)

  if not type(val) is float:
    raise TypeError(f"Value passed to {key} must be of type float")


def check_boolean(val, key):
  if not type(val) is bool:
    raise TypeError(f"Value passed to {key} must be of type bool")


def check_user_id(user_id, allow_none=False):
  if allow_none is True and user_id is None:
    return

  if not type(user_id) is int:
    raise TypeError("user_id must be of type int")

  if not isinstance(User.query.get(user_id), User):
    raise ValueError(f"user_id {user_id} is not returning valid User")


############ Models ############

class User(db.Model):
  """A User with an account to use the site"""

  __tablename__ = 'users'

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  email = db.Column(
    db.Text,
    unique=True,
    nullable=False
  )

  username = db.Column(
    db.Text,
    unique=True,
    nullable=False
  )

  hashed_password = db.Column(
    db.Text,
    nullable=False
  )

  created_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow()
  )

  ############ Relationships ############

  armor_comments = db.relationship(
    'ArmorComment',
    backref='author'
  )

  weapon_comments = db.relationship(
    'WeaponComment',
    backref='author'
  )

  spell_comments = db.relationship(
    'SpellComment',
    backref='author'
  )

  class_comments = db.relationship(
    'ClassComment',
    backref='author'
  )

  armor = db.relationship(
    'Armor',
    backref='author'
  )

  weapons = db.relationship(
    'Weapon',
    backref='author'
  )

  spells = db.relationship(
    'Spell',
    backref='author'
  )

  player_classes = db.relationship(
    'PlayerClass',
    backref='author'
  )


  ############ Methods ############

  def to_json(self):
    return json.dumps({
      "id": self.id,
      "email": self.email,
      "username": self.username,
      "created_at": str(self.created_at)
    })

  ############ Class Methods ############

  @classmethod
  def create_user(cls, email, username, unhashed_password):

    hashed_password = bcrypt.generate_password_hash(unhashed_password).decode('UTF-8')

    user = User(
      email=email,
      username=username,
      hashed_password=hashed_password,
      created_at=datetime.utcnow()
    )

    db.session.add(user)
    return user

  @classmethod
  def authenticate_user(cls, username, password):
    found_user = cls.query.filter_by(username=username).first()

    if found_user:
      if bcrypt.check_password_hash(found_user.hashed_password, password):
        return found_user

    return False



class ArmorComment(db.Model):

  __tablename__ = 'armor_comments'

  ############ Columns ############
  
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  slug = db.Column(
    db.Text
    # db.ForeignKey('armor.slug')
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )

  text = db.Column(
    db.Text
  )

  posted_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow()
  )

  ############ Relationships ############

  ############ Methods ############

  def to_json(self):
    return json.dumps({
      "id": self.id,
      "slug": self.slug,
      "author_user_id": self.author_user_id,
      "text": self.text,
      "posted_at": str(self.posted_at)
    })

  ############ Class Methods ############

  @classmethod
  def add_comment(cls, slug, author_user_id, text):

    # check that author is valid user
    if not isinstance(User.query.get(author_user_id), User):
      raise exc.IntegrityError

    comment = ArmorComment(
      slug=slug,
      author_user_id=author_user_id,
      text=text,
      posted_at=datetime.utcnow()
    )

    db.session.add(comment)
    return comment



class WeaponComment(db.Model):

  __tablename__ = 'weapon_comments'

  ############ Columns ############
  
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  slug = db.Column(
    db.Text,
    # db.ForeignKey('weapons.slug')
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )

  text = db.Column(
    db.Text
  )

  posted_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow()
  )

  ############ Relationships ############

  ############ Methods ############

  def to_json(self):
    return json.dumps({
      "id": self.id,
      "slug": self.slug,
      "author_user_id": self.author_user_id,
      "text": self.text,
      "posted_at": str(self.posted_at)
    })

  ############ Class Methods ############

  @classmethod
  def add_comment(cls, slug, author_user_id, text):

    # check that author is valid user
    if not isinstance(User.query.get(author_user_id), User):
      raise exc.IntegrityError

    comment = WeaponComment(
      slug=slug,
      author_user_id=author_user_id,
      text=text,
      posted_at=datetime.utcnow()
    )

    db.session.add(comment)
    return comment



class SpellComment(db.Model):

  __tablename__ = 'spell_comments'

  ############ Columns ############
  
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  slug = db.Column(
    db.Text,
    # db.ForeignKey('spells.slug')
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )

  text = db.Column(
    db.Text
  )

  posted_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow()
  )

  ############ Relationships ############

  ############ Methods ############

  def to_json(self):
    return json.dumps({
      "id": self.id,
      "slug": self.slug,
      "author_user_id": self.author_user_id,
      "text": self.text,
      "posted_at": str(self.posted_at)
    })

  ############ Class Methods ############

  @classmethod
  def add_comment(cls, slug, author_user_id, text):

    # check that author is valid user
    if not isinstance(User.query.get(author_user_id), User):
      raise exc.IntegrityError

    comment = SpellComment(
      slug=slug,
      author_user_id=author_user_id,
      text=text,
      posted_at=datetime.utcnow()
    )

    db.session.add(comment)
    return comment


class ClassComment(db.Model):

  __tablename__ = 'class_comments'

  ############ Columns ############
  
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  slug = db.Column(
    db.Text,
    # db.ForeignKey('player_classes.slug')
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )

  text = db.Column(
    db.Text
  )

  posted_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.utcnow()
  )

  ############ Relationships ############

  ############ Methods ############

  def to_json(self):
    return json.dumps({
      "id": self.id,
      "slug": self.slug,
      "author_user_id": self.author_user_id,
      "text": self.text,
      "posted_at": str(self.posted_at)
    })

  ############ Class Methods ############

  @classmethod
  def add_comment(cls, slug, author_user_id, text):

    # check that author is valid user
    if not isinstance(User.query.get(author_user_id), User):
      raise exc.IntegrityError

    comment = ClassComment(
      slug=slug,
      author_user_id=author_user_id,
      text=text,
      posted_at=datetime.utcnow()
    )

    db.session.add(comment)
    return comment


class Armor(db.Model):

  __tablename__ = "armor"


  ############ Columns ############
  
  slug = db.Column(
    db.Text,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False,
    unique=False
  )

  category_id = db.Column(
    db.Integer,
    db.ForeignKey('armor_categories.id')
  )

  document__slug__id = db.Column(
    db.Integer,
    db.ForeignKey('document__slugs.id'),
    nullable=True
  )

  document__title__id = db.Column(
    db.Integer,
    db.ForeignKey('document__titles.id'),
    nullable=True
  )

  document__license_url = db.Column(
    db.Integer,
    db.ForeignKey('document__license_urls.id'),
    nullable=True
  )

  ac_base = db.Column(
    db.Integer,
    nullable=True
  )

  modifier_attribute_id = db.Column(
    db.Integer,
    db.ForeignKey('attributes.id')
  )

  max_modifier = db.Column(
    db.Integer,
    nullable=True
  )

  strength_required = db.Column(
    db.Integer,
    nullable=True
  )

  cost_in_gp = db.Column(
    db.Float,
    nullable=True
  )

  weight = db.Column(
    db.Float,
    nullable=True
  )

  stealth_disadvantage = db.Column(
    db.Boolean,
    nullable=False,
    default=False
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id'),
    nullable=True
  )

  ############ Relationships ############

  modifier_attributes = db.relationship(
    'Attribute',
    secondary = 'armor_modifier_attributes',
    backref = 'armor'
  )

  ############ Methods ############

  def to_compat_json(self):
    
    armor_category_str = ""
    try:
      armor_category = ArmorCategory.query.get(self.category_id)
      armor_category_str = armor_category.name
    except:
      pass

    doc_slug_string = ""
    try:
      doc_slug = DocumentSlug.query.get(self.document__slug__id)
      doc_slug_string = doc_slug.slug
    except:
      pass
    
    doc_title_string = ""
    try:
      doc_title = DocumentTitle.query.get(self.document__license_url)
      doc_title_string = doc_title.title
    except:
      pass

    doc_license_url_string = ""
    try:
      doc_license_url = DocumentLicenseURL.query.get(self.document__slug__id)
      doc_license_url_string = doc_license_url.url
    except:
      pass


    ac_string = ""
    ac_base_str = str(self.ac_base) or ""
    
    modifier_str = ""
    try:
      # modifier_str = Attribute.query.get(self.modifier_attribute_id).name
      modifier_str = " + ".join([(attribute.name[0:3] + " modifier") for attribute in self.modifier_attributes])
    except:
      pass

    max_modifier_str = ""
    if self.max_modifier:
      max_modifier_str = f" (max {str(self.max_modifier)})"

    if ac_base_str and modifier_str:
      ac_string = ac_base_str + " + " + modifier_str
    else:
      ac_string = ac_base_str + modifier_str
    ac_string += max_modifier_str

    # strength_requirement_str = ""
    # try:
    #   strength_requirement_str = str(self.strength_required)
    # except:
    #   pass

    cost_str = ""
    if self.cost_in_gp != None:
      if self.cost_in_gp == int(self.cost_in_gp):
        cost_str = f"{int(self.cost_in_gp)} gp"
      else:
        cost_str = f"{self.cost_in_gp} gp"


    weight_str = ""
    if self.weight != None:
      if self.weight == int(self.weight):
        weight_str = f"{int(self.weight)} lbs."
      else:
        weight_str = f"{self.weight} lbs."


    return json.dumps({
      "name": self.name,
      "slug": self.slug,
      "category": armor_category_str,
      "document__slug": doc_slug_string,
      "document__title": doc_title_string,
      "document__license_url": doc_license_url_string,
      "ac_string": ac_string,
      "strength_requirement": self.strength_required,
      "cost": cost_str,
      "weight": weight_str,
      "stealth_disadvantage": self.stealth_disadvantage,
      "author_user_id": self.author_user_id
    })

  ############ Class Methods ############

  @classmethod
  def get_comments(cls, slug):
    return ArmorComment.query.filter(ArmorComment.slug==slug).all()

  @classmethod
  def create_armor(cls, slug=None, name=None, category_id=None, document__slug__id=None, document__title__id=None, document__license_url=None, ac_base=None, modifier_attributes = [], max_modifier=None, strength_required=None, cost_in_gp=None, weight=None, stealth_disadvantage=None, author_user_id=None):

    user_created_doc = bool(author_user_id)

    check_slug(slug)
    check_armor_category_id(category_id)
    check_doc_slug_id(document__slug__id, allow_none=user_created_doc)
    check_doc_title_id(document__title__id, allow_none=user_created_doc)
    check_doc_license_url(document__license_url, allow_none=user_created_doc)
    check_int(ac_base, "ac_base", allow_none=True)
    # check_attribute_id(modifier_attribute_id)
    check_int(max_modifier, "max_modifier", allow_none=True)
    check_int(strength_required, "strength_required", allow_none=True)
    check_float(cost_in_gp, "cost_in_gp", allow_none=True)
    check_float(weight, "weight", allow_none=True)
    check_boolean(stealth_disadvantage, "stealth_disadvantage")
    check_user_id(author_user_id, allow_none=(not user_created_doc))

    armor = Armor(
      slug=slug, 
      name=name, 
      category_id=category_id, 
      document__slug__id=document__slug__id, 
      document__title__id=document__title__id, 
      document__license_url=document__license_url, 
      ac_base=ac_base, 
      max_modifier=max_modifier, 
      strength_required=strength_required, 
      cost_in_gp=cost_in_gp, 
      weight=weight, 
      stealth_disadvantage=stealth_disadvantage, 
      author_user_id=author_user_id
    )

    db.session.add(armor)

    if not type(modifier_attributes) is list:
      db.session.rollback()
      raise TypeError("modifier_attributes must be of type list")

    # create armor modifier assignments
    for ma in modifier_attributes:
      try:
        ArmorModifierAttribute.create_armor_modifier_attribute(armor_slug=slug, attribute=ma)

      except:
        db.session.rollback()
        raise ValueError(f"Modifier attribute {ma} is invalid")

    return armor

  @classmethod
  def api_doc_to_compat_json(cls, api_doc):
    api_doc['author_user_id'] = None
    return json.dumps(api_doc)


class ArmorModifierAttribute(db.Model):

  __tablename__ = 'armor_modifier_attributes'

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key = True
  )

  armor_slug = db.Column(
    db.Text,
    db.ForeignKey('armor.slug')
  )

  attribute_id = db.Column(
    db.Integer,
    db.ForeignKey('attributes.id')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############

  @classmethod
  def create_armor_modifier_attribute(cls, armor_slug="", attribute=""):
    """Create an assignment of armor modifier attribute"""

    try:
      Armor.query.get(armor_slug)
    except:
      raise exc.IntegrityError(f"Armor {armor_slug} not found")

    attribute_id=None

    try:
      attribute_id=Attribute.query.filter(Attribute.name==attribute).one().id
    except:
      raise exc.IntegrityError(f"Attribute {attribute} not found")

    armor_modifier_attribute = ArmorModifierAttribute(
                                armor_slug=armor_slug, 
                                attribute_id=attribute_id)
    db.session.add(armor_modifier_attribute)
    return armor_modifier_attribute


class ArmorCategory(db.Model):

  __tablename__ = 'armor_categories'

  ############ Columns ############
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class DamageType(db.Model):

  __tablename__ = "damage_types"

  ############ Columns ############
  
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class WeaponDamageRoll(db.Model):

  __tablename__ = "weapon_damage_rolls"

  ############ Columns ############
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  dice_no = db.Column(
    db.Integer,
    nullable=True
  )

  die_sides = db.Column(
    db.Integer,
    nullable=True
  )

  flat_damage = db.Column(
    db.Integer,
    nullable=True
  )

  damage_type = db.Column(
    db.Integer,
    db.ForeignKey('damage_types.id')
  )

  weapon_slug = db.Column(
    db.Text,
    db.ForeignKey('weapons.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############



class WeaponProperty(db.Model):

  __tablename__ = "weapon_properties"


  ############ Columns ############
  id = db.Column(
    db.Integer,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class WeaponPropertyAssignment(db.Model):

  __tablename__ = "weapon_propery_assignments"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  weapon_property_id = db.Column(
    db.Integer,
    db.ForeignKey('weapon_properties.id'),
  )

  weapon_slug = db.Column(
    db.Text,
    db.ForeignKey('weapons.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class WeaponCategory(db.Model):

  __tablename__ = 'weapon_categories'

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class Weapon(db.Model):

  __tablename__='weapons'
  
  ############ Columns ############

  slug = db.Column(
    db.Text,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  category_id = db.Column(
    db.Integer,
    db.ForeignKey('armor_categories.id')
  )

  document__slug__id = db.Column(
    db.Integer,
    db.ForeignKey('document__slugs.id')
  )

  document__title__id = db.Column(
    db.Integer,
    db.ForeignKey('document__titles.id')
  )

  document__license_url = db.Column(
    db.Integer,
    db.ForeignKey('document__license_urls.id')
  )

  ac_base = db.Column(
    db.Integer,
    default=0
  )

  modifier_attribute_id = db.Column(
    db.Integer,
    db.ForeignKey('attributes.id'),
    nullable=True
  )

  max_modifier = db.Column(
    db.Integer,
    nullable=True
  )

  strength_required = db.Column(
    db.Integer,
    nullable=True
  )

  cost_in_gp = db.Column(
    db.Float,
    nullable=True
  )

  weight = db.Column(
    db.Float,
    nullable=True
  )

  bonus = db.Column(
    db.Integer,
    nullable=True
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id'),
    nullable=True
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class Attribute(db.Model):
  
  __tablename__ = 'attributes'

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key = True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class DocumentSlug(db.Model):

  __tablename__ = "document__slugs"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  slug = db.Column(
    db.Text,
    nullable=False
  )


class DocumentTitle(db.Model):

  __tablename__ = "document__titles"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  title = db.Column(
    db.Text,
    nullable=False
  )


class DocumentLicenseURL(db.Model):

  __tablename__ = "document__license_urls"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  url = db.Column(
    db.Text,
    nullable=False
  )





class SpellComponent(db.Model):

  __tablename__ = "spell_components"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  component_initial = db.Column(
    db.Text,
    nullable=False
  )

  spell_slug = db.Column(
    db.Text,
    db.ForeignKey('spells.slug'),
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_spell_component(cls, component, spell_slug):
    if component not in ['V', 'S', 'M']:
      raise exc.IntegrityError

    else:
      spell_component = SpellComponent(
        component=component,
        spell_slug=spell_slug
      )
      return spell_component


class ClassSpellSlugAssignment(db.Model):

  __tablename__ = "class_slug_spell_assignments"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  class_slug = db.Column(
    db.Text,
    # db.ForeignKey('player_classes.slug')
  )

  spell_slug = db.Column(
    db.Text,
    db.ForeignKey('spells.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class ArchetypeSpellAssignment(db.Model):

  __tablename__ = "archetype_spell_assignments"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key = True
  )

  archetype = db.Column(
    db.Text,
    nullable=False
  )

  spell_slug = db.Column(
    db.Text,
    db.ForeignKey('spells.slug')
  )


  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class MagicSchool(db.Model):

  __tablename__ = "magic_schools"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  

class Spell(db.Model):
  
  __tablename__ = 'spells'

  ############ Columns ############

  slug = db.Column(
    db.Text,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  description = db.Column(
    db.Text,
    nullable=False
  )

  higher_level = db.Column(
    db.Text,
    nullable=False
  )

  page = db.Column(
    db.Text,
    nullable=False
  )

  range = db.Column(
    db.Text,
    nullable=False
  )

  material = db.Column(
    db.Text,
    nullable=False
  )

  ritual = db.Column(
    db.Boolean,
    default=False
  )

  duration = db.Column(
    db.Text,
    nullable=False
  )

  concentration = db.Column(
    db.Boolean,
    default=False
  )

  casting_time = db.Column(
    db.Text,
    nullable=False
  )

  level = db.Column(
    db.Integer,
    nullable=False
  )

  magic_school = db.Column(
    db.Integer,
    db.ForeignKey('magic_schools.id')
  )

  document__slug__id = db.Column(
    db.Integer,
    db.ForeignKey('document__slugs.id'),
    nullable=True
  )

  document__title__id = db.Column(
    db.Integer,
    db.ForeignKey('document__titles.id'),
    nullable=True
  )

  document__license_url = db.Column(
    db.Integer,
    db.ForeignKey('document__license_urls.id'),
    nullable=True
  )

  circles = db.Column(
    db.Text,
    nullable=True
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id'),
    nullable=True
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############





class PlayerClass(db.Model):

  __tablename__ = 'player_classes'
  
  ############ Columns ############

  slug = db.Column(
    db.Text,
    primary_key=True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  description = db.Column(
    db.Text,
    nullable=False
  )

  hit_die = db.Column(
    db.Integer,
    nullable=False
  )

  base_hp_at_1st_level = db.Column(
    db.Integer,
    nullable=False
  )

  tool_proficiency = db.Column(
    db.Text,
    nullable=False
  )

  skill_proficiency = db.Column(
    db.Text,
    nullable=False
  )

  starting_equipment = db.Column(
    db.Text,
    nullable=False
  )

  table = db.Column(
    db.Text,
    nullable=False
  )

  spellcasting_ability = db.Column(
    db.Integer,
    db.ForeignKey('attributes.id'),
    nullable=True
  )

  subtypes_name = db.Column(
    db.Text,
    nullable=True
  )

  archetypes = db.Column(
    db.Text,
    nullable=True
  )

  document__slug__id = db.Column(
    db.Integer,
    db.ForeignKey('document__slugs.id'),
    nullable=True
  )

  document__title__id = db.Column(
    db.Integer,
    db.ForeignKey('document__titles.id'),
    nullable=True
  )

  document__license_url = db.Column(
    db.Integer,
    db.ForeignKey('document__license_urls.id'),
    nullable=True
  )

  author_user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id'),
    nullable=True
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class WeaponProficiency(db.Model):

  __tablename__ = "weapon_proficiency"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  weapon_category_id = db.Column(
    db.Integer,
    db.ForeignKey('weapon_categories.id')
  )

  class_slug = db.Column(
    db.Text,
    # db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############


class SavingThrow(db.Model):

  __tablename__ = "saving_throws"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  attribute_id = db.Column(
    db.Integer,
    db.ForeignKey('attributes.id'),
    nullable=False
  )

  class_slug = db.Column(
    db.Text,
    # db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############

