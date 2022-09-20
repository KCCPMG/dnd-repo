import os
from unittest import TestCase
from sqlalchemy import exc
import requests

from models import db, User, ArmorComment, WeaponComment, SpellComment, ClassComment, Armor, ArmorCategory, DamageType, WeaponDamageRoll, WeaponProperty, WeaponPropertyAssignment, WeaponCategory, Weapon, Attribute, DocumentSlug, DocumentTitle, DocumentLicenseURL, SpellComponent, ClassSpellSlugAssignment, ArchetypeSpellAssignment, MagicSchool, Spell, PlayerClass, WeaponProficiency, SavingThrow

from tests.test_seed import run_test_seed

os.environ['DATABASE_URL'] = "postgresql:///dnd-repo-test"

from app import app

def delete_all():
  User.query.delete() 
  ArmorComment.query.delete() 
  WeaponComment.query.delete() 
  SpellComment.query.delete() 
  ClassComment.query.delete() 
  Armor.query.delete() 
  ArmorCategory.query.delete() 
  DamageType.query.delete() 
  WeaponDamageRoll.query.delete() 
  WeaponProperty.query.delete() 
  WeaponPropertyAssignment.query.delete() 
  WeaponCategory.query.delete() 
  Weapon.query.delete() 
  Attribute.query.delete() 
  DocumentSlug.query.delete() 
  DocumentTitle.query.delete() 
  DocumentLicenseURL.query.delete() 
  SpellComponent.query.delete() 
  ClassSpellSlugAssignment.query.delete() 
  ArchetypeSpellAssignment.query.delete() 
  MagicSchool.query.delete() 
  Spell.query.delete() 
  PlayerClass.query.delete() 
  WeaponProficiency.query.delete() 
  SavingThrow.query.delete()




class ArmorTest(TestCase):
  """Test construction for success and failure, json method"""

  def setUp(self):
    run_test_seed()
    self.sample_user = User.create_user('sample@user.com','sampleuser', 'test123')

  
  def tearDown(self) -> None:
    return super().tearDown()


  # valid construction
  def test_construction(self):
    """Test Class method create_armor with several different configurations"""
    # omit modifier_attribute
    new_armor = Armor.create_armor(slug="slug", 
                                   name="Slug", 
                                   category_id=3, 
                                   document__slug__id=1, 
                                   document__title__id=1, 
                                   document__license_url=1, 
                                   ac_base=5, 
                                   modifier_attributes=["Dexterity"],
                                  #  modifier_attribute_id=2, 
                                   max_modifier=2, 
                                   strength_required=12, 
                                   cost_in_gp=40, 
                                   weight=10, 
                                   stealth_disadvantage=False, 
                                   author_user_id=self.sample_user.id)

    self.assertIsInstance(new_armor, Armor)

    # again, but omitting weight
    new_armor = Armor.create_armor(slug="slug2", 
                                  name="Slug", 
                                  category_id=3, 
                                  document__slug__id=1, 
                                  document__title__id=1, 
                                  document__license_url=1, 
                                  ac_base=5, 
                                  modifier_attributes=["Dexterity"],
                                #  2, 
                                  max_modifier=2, 
                                  strength_required=12, 
                                  cost_in_gp=40, 
                                  weight=10, 
                                  stealth_disadvantage=False,
                                  author_user_id=self.sample_user.id)

    self.assertIsInstance(new_armor, Armor)


    # without doc_slug_id, doc_title_id, doc_license_url
    new_armor = Armor.create_armor(slug="slug3", 
                                   name="Slug", 
                                   category_id=3,  
                                   ac_base=5, 
                                   modifier_attributes=["Dexterity"],
                                  #  modifier_attribute_id=2, 
                                   max_modifier=2, 
                                   strength_required=12, 
                                   cost_in_gp=40, 
                                   weight=10, 
                                   stealth_disadvantage=False, 
                                   author_user_id=self.sample_user.id)


    # without author_user_id
    new_armor = Armor.create_armor(slug="slug4", 
                                   name="Slug", 
                                   category_id=3, 
                                   document__slug__id=1, 
                                   document__title__id=1, 
                                   document__license_url=1, 
                                   ac_base=5, 
                                   modifier_attributes=["Dexterity"],
                                  #  2, 
                                   max_modifier=2, 
                                   strength_required=12, 
                                   cost_in_gp=40, 
                                   weight=10, 
                                   stealth_disadvantage=False)



  # invalid construction 
  def test_invalid_construction(self):
    
    # check_slug
    with self.assertRaises(TypeError):
      Armor.create_armor(slug=None, 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_slug
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="sl ug",                          
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_armor_category_id
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=13, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_doc_slug_id
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=11, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_doc_title_id
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                    name="Slug", 
                    category_id=3, 
                    document__slug__id=1, 
                    document__title__id=11, 
                    document__license_url=1, 
                    ac_base=5, 
                    modifier_attributes=["Dexterity"],
                  #  2, 
                    max_modifier=2, 
                    strength_required=12, 
                    cost_in_gp=40, 
                    weight=10, 
                    stealth_disadvantage=False)

    # check_doc_license_url
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                    name="Slug", 
                    category_id=3, 
                    document__slug__id=1, 
                    document__title__id=1, 
                    document__license_url=15, 
                    ac_base=5, 
                    modifier_attributes=["Dexterity"],
                  #  2, 
                    max_modifier=2, 
                    strength_required=12, 
                    cost_in_gp=40, 
                    weight=10, 
                    stealth_disadvantage=False)

    # check_int - ac_base
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base="5", 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # invalid modifier_attributes format
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes="Dexterity",
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)    


    # check_int - max_modifier
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier="2", 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_int - strength_required
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required="12", 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_float - cost_in_gp
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp="40", 
                          weight=10, 
                          stealth_disadvantage=False)

    # check_float - weight
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight="10", 
                          stealth_disadvantage=False)

    # check_boolean
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage="False")

    # check_user_id
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False,
                          author_user_id=self.sample_user)

    # check_user_id
    with self.assertRaises(ValueError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3, 
                          document__slug__id=1, 
                          document__title__id=1, 
                          document__license_url=1, 
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                        #  2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False,
                          author_user_id=-(self.sample_user.id))


    # no license information *or* author id
    with self.assertRaises(TypeError):
      Armor.create_armor(slug="slug", 
                          name="Slug", 
                          category_id=3,  
                          ac_base=5, 
                          modifier_attributes=["Dexterity"],
                          # modifier_attribute_id=2, 
                          max_modifier=2, 
                          strength_required=12, 
                          cost_in_gp=40, 
                          weight=10, 
                          stealth_disadvantage=False)


  # relationships

  # to_compat_json
  def test_to_compat_json(self):
    response = requests.get('https://api.open5e.com/armor/unarmored-defense-monk')
    api_json = Armor.api_doc_to_compat_json(response.json())

    monk_unarmored = Armor.create_armor(slug="unarmored-defense-monk", 
                                        name="Unarmored Defense (Monk)", 
                                        category_id=6,document__slug__id=1, 
                                        document__title__id=1, 
                                        document__license_url=1,  
                                        ac_base=10, 
                                        modifier_attributes=["Dexterity", "Wisdom"],
                                        # modifier_attribute_id=2, 
                                        # max_modifier=2, 
                                        # strength_required=12, 
                                        cost_in_gp=0, 
                                        # weight=10, 
                                        stealth_disadvantage=False)
    
    my_monk_json = monk_unarmored.to_compat_json()

    f = open('tests/api_monk_unarmored.json', 'w')
    f.write(api_json)
    f.close()
    f = open('tests/my_monk_unarmored.json', 'w')
    f.write(my_monk_json)
    f.close()

    self.assertEqual(api_json, my_monk_json)







