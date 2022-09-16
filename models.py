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


def check_weapon_category_id(cat_id, allow_none=False):
  if allow_none is True and cat_id is None:
    return

  if not isinstance(WeaponCategory.query.get(cat_id), WeaponCategory):
    raise ValueError(f"Invalid category_id {cat_id}")


def check_magic_school(magic_school, allow_none=True):
  if allow_none is True and magic_school is None:
    return

  if not isinstance(MagicSchool.query.get(magic_school), MagicSchool):
    raise ValueError(f"Invalid magic_school {magic_school}")

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


def check_die_validity(die_sides, allow_none=False):
  if allow_none is True and die_sides is None:
    return

  if die_sides not in [2, 4, 6, 8, 10, 12, 20, 100]:
    raise TypeError(f"Invalid die with sides: {die_sides}. Die must have 2, 4, 6, 8, 10, 12, 20, or 100 sides.")
  else:
    return


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
  @classmethod
  def create_roll(cls, dice_no, die_sides, flat_damage, damage_type, weapon_slug):

    check_int(dice_no, "dice_no", allow_none=True)
    check_die_validity(die_sides, allow_none=True)
    check_int(flat_damage, "flat_damage", allow_none=True)

    try:
      DamageType.query.get(damage_type)
    except:
      # print(f"DamageType {damage_type} (type {type(damage_type)}) not found")
      raise exc.IntegrityError(f"DamageType {damage_type} not found")

    try:
      Weapon.query.get(weapon_slug)
    except:
      print(f"Weapon {weapon_slug} not found")
      raise exc.IntegrityError(f"Weapon {weapon_slug} not found")

    weapon_damage_roll = WeaponDamageRoll(dice_no=dice_no,
                                          die_sides=die_sides,
                                          flat_damage=flat_damage,
                                          damage_type=damage_type,
                                          weapon_slug=weapon_slug)
    db.session.add(weapon_damage_roll)
    return weapon_damage_roll


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

  __tablename__ = "weapon_property_assignments"

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
  @classmethod
  def create_assignment(cls, weapon_property_id=None, weapon_slug=None):
    """Create a Weapon Property Assignment"""
    try:
      WeaponProperty.query.get(weapon_property_id)
    except:
      raise exc.IntegrityError(f"WeaponProperty {weapon_property_id} not found")

    try:
      Weapon.query.get(weapon_slug)
    except:
      raise exc.IntegrityError(f"Weapon {weapon_slug} not found")

    weapon_property_assignment = WeaponPropertyAssignment(
      weapon_property_id=weapon_property_id,
      weapon_slug=weapon_slug
    )

    db.session.add(weapon_property_assignment)
    return weapon_property_assignment



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

  weapon_category = db.Column(
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

  weapon_properties = db.relationship(
    'WeaponProperty',
    secondary = 'weapon_property_assignments',
    backref = 'weapon'
  )

  damage_rolls = db.relationship(
    'WeaponDamageRoll',
    backref = 'weapon'
  )

  ############ Methods ############

  def to_compat_json(self):

    weapon_category_str = ""
    try:
      weapon_category = WeaponCategory.query.get(self.weapon_category)
      weapon_category_str = weapon_category.name
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

    cost_str = ""
    if self.cost_in_gp != None:
      if self.cost_in_gp == int(self.cost_in_gp):
        cost_str = f"{int(self.cost_in_gp)} gp"
      else:
        cost_str = f"{self.cost_in_gp} gp"

    weight_str = ""
    if self.weight != None:
      if self.weight == int(self.weight):
        weight_str = f"{int(self.weight)} lb."
      else:
        weight_str = f"{self.weight} lb."

    properties_list = []
    try:
      properties_list = [wp.name for wp in self.weapon_properties]
    except:
      pass

    main_damage_str = ""
    try:
      dr_strings = []
      for dr in self.damage_rolls:
        damage_str=""
        try:
          if dr.dice_no and dr.die_sides:
            damage_str+=str(dr.dice_no)
            damage_str+="d"
            damage_str+=str(dr.die_sides)
        except:
          pass
        try:
          if damage_str and dr.flat_damage:
            damage_str+=" + "
            damage_str+=str(dr.flat_damage)
          elif dr.flat_damage:
            damage_str+=str(dr.flat_damage)
        except:
          pass
        try:
          if damage_str:
            damage_str+=" "
            damage_str+=DamageType.query.get(dr.damage_type).name
        except:
          pass
        dr_strings.append(damage_str)
      main_damage_str = ", ".join(dr_strings)
    except:
      pass

    bonus_str = ""
    try: 
      if self.bonus:
        if self.bonus > 0:
          bonus_str = f"+ {self.bonus}"
        else:
          bonus_str = str(self.bonus)
    except:
      pass

    return json.dumps({
      "name": self.name,
      "slug": self.slug,
      "category": weapon_category_str,
      "document__slug": doc_slug_string,
      "document__title": doc_title_string,
      "document__license_url": doc_license_url_string,
      "cost": cost_str,
      "weight": weight_str,
      "properties": properties_list,
      "author_user_id": self.author_user_id,
      "damage": main_damage_str,
      "bonus": bonus_str
    })

  ############ Class Methods ############

  @classmethod
  def get_comments(cls, slug):
    return WeaponComment.query.filter(WeaponComment.slug==slug).all()

  @classmethod
  def create_weapon(cls, slug=None, name=None, weapon_category=None, document__slug__id=None, document__title__id=None, document__license_url=None, cost_in_gp=None, weight=None, bonus=None, author_user_id=None, weapon_damage_rolls=None, weapon_property_assignments=None):

    user_created_doc = bool(author_user_id)

    check_slug(slug)
    check_weapon_category_id(weapon_category)
    check_doc_slug_id(document__slug__id, allow_none=user_created_doc)
    check_doc_title_id(document__title__id, allow_none=user_created_doc)
    check_doc_license_url(document__license_url, allow_none=user_created_doc)
    check_float(cost_in_gp, "cost_in_gp", allow_none=True)
    check_float(weight, "weight", allow_none=True)
    check_int(bonus, "bonus", allow_none=True)
    check_user_id(author_user_id, allow_none=(not user_created_doc))

    weapon = Weapon(
      slug=slug,
      name=name,
      weapon_category=weapon_category,
      document__slug__id=document__slug__id, 
      document__title__id=document__title__id, 
      document__license_url=document__license_url,
      cost_in_gp=cost_in_gp,
      weight=weight,
      bonus=bonus,
      author_user_id=author_user_id 
    )

    db.session.add(weapon)

    if not type(weapon_damage_rolls) is list:
      db.session.rollback()
      raise TypeError("weapon_damage_rolls must be of type list")

    for wdr in weapon_damage_rolls:
      try:
        WeaponDamageRoll.create_roll(dice_no=wdr['dice_no'],
                                     die_sides=wdr['die_sides'],
                                     damage_type=wdr['damage_type'],
                                     flat_damage=wdr['flat_damage'],
                                     weapon_slug=weapon.slug)
      except Exception as e:
        db.session.rollback()
        raise e
        raise ValueError(f"Weapon Damage Roll {wdr} is invalid")

    if not type(weapon_property_assignments) is list:
      db.session.rollback()
      raise TypeError("weapon_damage_rolls must be of type list")

    for wpr in weapon_property_assignments:
      try:
        WeaponPropertyAssignment.create_assignment(
          weapon_property_id=wpr,
          weapon_slug=weapon.slug
        )
      except:
        db.session.rollback()
        raise ValueError(f"Weapon Property Assignment {wpr} is invalid")

    return weapon

  @classmethod
  def api_doc_to_compat_json(cls, api_doc):
    api_doc['author_user_id'] = None
    api_doc['damage'] = api_doc['damage_dice'] + " " + api_doc['damage_type']
    if not api_doc['properties']:
      api_doc['properties'] = []
    del api_doc['damage_dice']
    del api_doc['damage_type']
    return json.dumps(api_doc)



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
      raise exc.IntegrityError("Component must be 'V', 'S', or 'M'")

    else:
      spell_component = SpellComponent(
        component_initial=component,
        spell_slug=spell_slug
      )
      db.session.add(spell_component)
      return spell_component


class ClassSpellSlugAssignment(db.Model):

  __tablename__ = "class_spell_slug_assignments"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  class_slug = db.Column(
    db.Text,
    db.ForeignKey('player_classes.slug')
  )

  spell_slug = db.Column(
    db.Text,
    db.ForeignKey('spells.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_spell_slug_assignment(cls, class_slug, spell_slug):
    """
    check validity of class_slug and spell_slug, create assignment
    """
    if not isinstance(PlayerClass.query.get(class_slug), PlayerClass):
      raise exc.IntegrityError(f"Class Slug {class_slug} is invalid")

    elif not isinstance(Spell.query.get(spell_slug), Spell):
      raise exc.IntegrityError(f"Spell Slug {spell_slug} is invalid")

    else:
      class_spell_slug_assignment = ClassSpellSlugAssignment(
        class_slug=class_slug,
        spell_slug=spell_slug
      )
      db.session.add(class_spell_slug_assignment)
      return class_spell_slug_assignment


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
  @classmethod
  def create_archetype_spell_assignment(cls, archetype, spell_slug):
    """Create an archetype spell assignment"""
    if not isinstance(Spell.query.get(spell_slug), Spell):
      db.session.rollback()
      raise exc.IntegrityError(f"Spell slug {spell_slug} is not a valid spell")

    else:
      assignment = ArchetypeSpellAssignment(archetype=archetype, spell_slug=spell_slug)
      db.session.add(assignment)
      return assignment

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
    nullable=True
  )

  spell_range = db.Column(
    db.Text,
    nullable=False
  )

  material = db.Column(
    db.Text,
    nullable=True
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

  spell_components = db.relationship('SpellComponent', backref='spells')

  # classes = db.relationship('PlayerClass',
  #   secondary='class_spell_slug_assignments',
  #   backref='spells'
  # )

  archetypes = db.relationship('ArchetypeSpellAssignment',
    backref='spells'
  )

  ############ Methods ############

  def to_compat_json(self):
    
    page_str = self.page if self.page else ""

    components_str = ", ".join([c.component_initial for c in self.spell_components])

    material_str = self.material if self.material else ""

    ritual_str = "yes" if self.ritual else "no"
    concentration_str = "yes" if self.concentration else "no"

    level_str = ""
    if self.level == 0:
      level_str = "Cantrip"
    elif self.level == 1:
      level_str = "1st-level"
    elif self.level == 2:
      level_str = "2nd-level"
    elif self.level == 3:
      level_str = "3rd-level"
    else:
      level_str = str(self.level)+"th-level"
    
    school_str = MagicSchool.query.get(self.magic_school).name

    dnd_class_str = ", ".join([pc.name for pc in self.player_class])

    archetype_str = ", ".join([arch.archetype for arch in self.archetypes])

    circles_str = self.circles if self.circles else ""

    doc_slug_string = ""
    try:
      doc_slug = DocumentSlug.query.get(self.document__slug__id)
      doc_slug_string = doc_slug.slug
    except:
      pass
    
    doc_title_string = ""
    try:
      doc_title = DocumentTitle.query.get(self.document__title__id)
      doc_title_string = doc_title.title
    except:
      pass

    doc_license_url_string = ""
    try:
      doc_license_url = DocumentLicenseURL.query.get(self.document__license_url)
      doc_license_url_string = doc_license_url.url
    except:
      pass

    return json.dumps({
      "slug": self.slug,
      "name": self.name,
      "desc": self.description,
      "higher_level": self.higher_level,
      "page": page_str,
      "range": self.spell_range,
      "components": components_str,
      "material": material_str,
      "ritual": ritual_str,
      "duration": self.duration,
      "concentration": concentration_str,
      "casting_time": self.casting_time,
      "level": level_str,
      "level_int": self.level,
      "school": school_str,
      "dnd_class": dnd_class_str,
      "archetype": archetype_str,
      "circles": circles_str,
      "document__slug": doc_slug_string,
      "document__title": doc_title_string,
      "document__license_url": doc_license_url_string,
      "author_user_id": self.author_user_id
    })




  ############ Class Methods ############
  
  @classmethod
  def get_comments(cls, slug):
    return SpellComment.query.filter(SpellComment.slug==slug).all()

  @classmethod
  def create_spell(cls,
                  slug=None,
                  name=None,
                  description=None,
                  higher_level=None,
                  page=None,
                  spell_range=None,
                  material=None,
                  ritual=None,
                  duration=None,
                  concentration=False,
                  casting_time=None,
                  level=None,
                  magic_school=None,
                  document__slug__id=None,
                  document__title__id=None,
                  document__license_url=None,
                  circles=None,
                  author_user_id=None,
                  spell_components=[],
                  class_slug_spell_assignments=[],
                  archetype_spell_assignments=[]):

    user_created_doc = bool(author_user_id)


    check_slug(slug)
    check_boolean(ritual, "ritual")
    check_boolean(concentration, "concentration")
    check_int(level, "level", allow_none=True)
    check_magic_school(magic_school)
    check_doc_slug_id(document__slug__id, allow_none=user_created_doc)
    check_doc_title_id(document__title__id, allow_none=user_created_doc)
    check_doc_license_url(document__license_url, allow_none=user_created_doc)
    check_user_id(author_user_id, allow_none=(not user_created_doc))

    
    spell = Spell(
      slug=slug,
      name=name,
      description=description,
      higher_level=higher_level,
      page=page,
      spell_range=spell_range,
      material=material,
      ritual=ritual,
      duration=duration,
      concentration=concentration,
      casting_time=casting_time,
      level=level,
      magic_school=magic_school,
      document__slug__id=document__slug__id,
      document__title__id=document__title__id,
      document__license_url=document__license_url,
      circles=circles,
      author_user_id=author_user_id
    )

    db.session.add(spell)
    
    # create spell components
    if not type(spell_components) is list:
      db.session.rollback()
      raise TypeError("spell_components must be of type list")

    for sc in spell_components:
      try:
        SpellComponent.create_spell_component(sc, spell.slug)
      except:
        db.session.rollback()
        raise ValueError(f"Spell Component {sc} is invalid")

    # create class slug spell assignments
    if not type(class_slug_spell_assignments) is list:
      db.session.rollback()
      raise TypeError("class_slug_spell_assignments must be of type list")

    for cssa in class_slug_spell_assignments:
      try:
        ClassSpellSlugAssignment.create_spell_slug_assignment(cssa, spell.slug)
      except Exception as e:
        db.session.rollback()
        raise e
        raise ValueError(f"Class Slug Spell Assignment {cssa} is invalid")

    # create archetype spell assignments
    if not type(archetype_spell_assignments) is list:
      db.session.rollback()
      raise TypeError("archetype_spell_assignments must be of type list")

    for arch_assignment in archetype_spell_assignments:
      try:
        ArchetypeSpellAssignment.create_archetype_spell_assignment(archetype=arch_assignment, spell_slug=spell.slug)
      except:
        db.session.rollback()
        raise ValueError(f"ArchetypeSpellAssignment \"{arch_assignment}\" is invalid")

    return spell



  @classmethod
  def api_doc_to_compat_json(cls, api_doc):
    api_doc['author_user_id'] = None
    return json.dumps(api_doc)


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

  # archetypes = db.Column(
  #   db.Text,
  #   nullable=True
  # )

  prof_weapons = db.Column(
    db.Text,
    nullable=False
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

  armor_proficiencies = db.relationship(
    'ArmorCategory',
    secondary = 'armor_proficiencies',
    backref = "player_class"
  )

  # weapon_proficiencies = db.relationship(
  #   'WeaponCategory',
  #   secondary = 'weapon_proficiencies',
  #   backref = "player_class"
  # )

  saving_throws = db.relationship(
    'Attribute',
    secondary = 'saving_throws',
    backref = 'player_class'
  )

  homebrew_spells = db.relationship(
    'Spell',
    secondary = 'class_spell_slug_assignments',
    backref = 'player_class',
  )

  api_spells = db.relationship(
    'APISpell',
    secondary = 'class_slug_api_spell_assignments',
    backref = 'player_class'
  )

  ############ Methods ############

  def to_compat_json(self):

    hit_dice_str = "1d"+str(self.hit_die)

    base_hp_str = f"{self.base_hp_at_1st_level} + your Constitution modifier"

    higher_lvl_hp_str = "1d"+str(self.base_hp_at_1st_level)
    higher_lvl_hp_str += f" (or {int((self.base_hp_at_1st_level + 2)/2)})"
    higher_lvl_hp_str += f" + your Constitution modifier per {self.name} level after 1st"

    # weapon_prof_str = ", ".join([wp.name for wp in self.weapon_proficiencies])

    saving_throw_str = ", ".join([st.name for st in self.saving_throws])

    armor_prof_str = ", ".join([ap.name for ap in self.armor_proficiencies])
 
    spell_ability_str = ""
    if self.spellcasting_ability:
      spell_ability_str = Attribute.query.get(self.spellcasting_ability).name

    doc_slug_string = ""
    try:
      doc_slug = DocumentSlug.query.get(self.document__slug__id)
      doc_slug_string = doc_slug.slug
    except:
      pass
    
    doc_title_string = ""
    try:
      doc_title = DocumentTitle.query.get(self.document__title__id)
      doc_title_string = doc_title.title
    except:
      pass

    doc_license_url_string = ""
    try:
      doc_license_url = DocumentLicenseURL.query.get(self.document__license_url)
      doc_license_url_string = doc_license_url.url
    except:
      pass

    author_str = ""
    try:
      author_str = self.author_user_id
    except:
      pass

    return json.dumps({
      "name": self.name,
      "slug": self.slug,
      "desc": self.description,
      "hit_dice": hit_dice_str,
      "hp_at_1st_level": base_hp_str,
      "hp_at_higher_levels": higher_lvl_hp_str,
      "prof_armor": armor_prof_str,
      "prof_weapons": self.prof_weapons,
      "prof_tools": self.tool_proficiency,
      "prof_saving_throws": saving_throw_str,
      "prof_skills": self.skill_proficiency,
      "equipment": self.starting_equipment,
      "table": self.table,
      "spellcasting_ability": spell_ability_str, 
      "subtypes_name": self.subtypes_name,
      "document__slug": doc_slug_string,
      "document__title": doc_title_string, 
      "document__license_url": doc_license_url_string,
      "author_user_id": author_str
    })


  ############ Class Methods ############

  @classmethod
  def get_comments(cls, slug):
    return ClassComment.query.filter(ClassComment.slug==slug).all()
  
  @classmethod
  def create_player_class(cls,
    slug=None,
    name=None,
    description=None,
    hit_die=None,
    base_hp_at_1st_level=None,
    tool_proficiency=None,
    skill_proficiency=None,
    starting_equipment=None,
    table=None,
    spellcasting_ability=None,
    subtypes_name=None,
    # archetypes=None,
    document__slug__id=None,
    document__title__id=None,
    document__license_url=None,
    author_user_id=None,
    armor_proficiencies = [],
    prof_weapons = None,
    saving_throw_ids = [],
    homebrew_spell_slugs = [],
    api_spell_slugs = []
  ):

    user_created_doc=bool(author_user_id)
    check_slug(slug)
    check_die_validity(hit_die)
    check_int(base_hp_at_1st_level, "base_hp_at_1st_level", allow_none=False)
    check_attribute_id(spellcasting_ability, allow_none=True)
    check_doc_slug_id(document__slug__id, allow_none=user_created_doc)
    check_doc_title_id(document__title__id, allow_none=user_created_doc)
    check_doc_license_url(document__license_url, allow_none=user_created_doc)
    check_user_id(author_user_id, allow_none=(not user_created_doc))

    
    player_class = PlayerClass(
      slug=slug,
      name=name,
      description=description,
      hit_die=hit_die,
      base_hp_at_1st_level=base_hp_at_1st_level,
      tool_proficiency=tool_proficiency,
      skill_proficiency=skill_proficiency,
      starting_equipment=starting_equipment,
      table=table,
      spellcasting_ability=spellcasting_ability,
      subtypes_name=subtypes_name,
      prof_weapons = prof_weapons,
      # archetypes=archetypes,
      document__slug__id=document__slug__id,
      document__title__id=document__title__id,
      document__license_url=document__license_url,
      author_user_id=author_user_id
    )

    db.session.add(player_class)


    # if not isinstance(player_class, PlayerClass):
    #   db.session.rollback()
    #   raise ValueError("Failed to create PlayerClass")
    
    # create armor_proficiencies
    for armor_proficiency in armor_proficiencies:
      try:
        ArmorProficiency.create_armor_proficiency(armor_proficiency, player_class.slug)
      except Exception as e:
        db.session.rollback()
        raise ValueError(f"Armor Proficiency {armor_proficiency} is invalid")

    # create saving_throws
    for saving_throw_id in saving_throw_ids:
      try:
        SavingThrow.create_saving_throw(saving_throw_id, player_class.slug)
      except:
        db.session.rollback()
        raise ValueError(f"Saving Throw ID {saving_throw_id} is invalid")

    # create api spell dependencies
    for spell_slug in homebrew_spell_slugs:
      try:
        ClassSpellSlugAssignment.create_spell_slug_assignment(player_class.slug, spell_slug)
      except:
        db.session.rollback()
        raise ValueError(f"Homebrew spell slug {spell_slug} is invalid")

    # create homebrew spell dependencies
    for spell_slug in api_spell_slugs:
      try:
        ClassSlugAPISpellAssignment.create_api_spell_assignment(spell_slug, player_class.slug)
      except:
        db.session.rollback()
        raise ValueError(f"Homebrew spell slug {spell_slug} is invalid")

    return player_class

  @classmethod
  def api_doc_to_compat_json(cls, api_doc):
    api_doc['author_user_id'] = ""
    del api_doc["archetypes"]
    return json.dumps(api_doc)


class WeaponProficiency(db.Model):

  __tablename__ = "weapon_proficiencies"

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
    db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_weapon_proficiency(cls, weapon_category_id, class_slug):
    """Create weapon proficiency"""

    check_weapon_category_id(weapon_category_id)

    if not isinstance(PlayerClass.query.get(class_slug), PlayerClass):
      raise ValueError(f'Invalid class_slug {class_slug}')

    weapon_proficiency = WeaponProficiency(
      weapon_category_id=weapon_category_id,
      class_slug=class_slug
    )
    db.session.add(weapon_proficiency)


class ArmorProficiency(db.Model):

  __tablename__ = "armor_proficiencies"

  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  armor_category_id = db.Column(
    db.Integer,
    db.ForeignKey('armor_categories.id')
  )

  class_slug = db.Column(
    db.Text,
    db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_armor_proficiency(cls, armor_category_id, class_slug):
    """Create weapon proficiency"""

    check_armor_category_id(armor_category_id)

    if not isinstance(PlayerClass.query.get(class_slug), PlayerClass):
      raise ValueError(f'Invalid class_slug {class_slug}')

    armor_proficiecny = ArmorProficiency(
      armor_category_id=armor_category_id,
      class_slug=class_slug
    )
    db.session.add(armor_proficiecny)


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
    db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_saving_throw(cls, attribute_id, class_slug):
    """Create weapon proficiency"""

    check_attribute_id(attribute_id)

    if not isinstance(PlayerClass.query.get(class_slug), PlayerClass):
      raise ValueError(f'Invalid class_slug {class_slug}')

    saving_throw = SavingThrow(
      attribute_id=attribute_id,
      class_slug=class_slug
    )
    db.session.add(saving_throw)


class APISpell(db.Model):
  """Constant reference table to know which spells exist in the API"""

  __tablename__ = "api_spells"

  ############ Columns ############
  slug = db.Column(
    db.Text,
    primary_key = True
  )

  name = db.Column(
    db.Text,
    nullable=False
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_api_spell(cls, slug, name):

    api_spell = APISpell(
      slug=slug,
      name=name
    )
    db.session.add(api_spell)
    return api_spell



class ClassSlugAPISpellAssignment(db.Model):
  """Assignments of API spells to player_class"""

  __tablename__ = "class_slug_api_spell_assignments"
  
  ############ Columns ############

  id = db.Column(
    db.Integer,
    primary_key=True
  )

  api_spell_slug = db.Column(
    db.Text,
    db.ForeignKey('api_spells.slug')
  )

  player_class_slug = db.Column(
    db.Text,
    db.ForeignKey('player_classes.slug')
  )

  ############ Relationships ############

  ############ Methods ############

  ############ Class Methods ############
  @classmethod
  def create_api_spell_assignment(cls, api_spell_slug, player_class_slug):
    """Create a row on many-to-many assignment table"""

    assignment = ClassSlugAPISpellAssignment(
      api_spell_slug=api_spell_slug,
      player_class_slug=player_class_slug
    )
    db.session.add(assignment)
    return assignment
