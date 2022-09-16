import os
from sqlite3 import IntegrityError
from unittest import TestCase
from sqlalchemy import exc
import requests
import json
from psycopg2 import errors

from models import Weapon, User

from tests.test_seed import run_test_seed

os.environ['DATABASE_URL'] = "postgresql:///dnd-repo-test"

from app import app



class WeaponTest(TestCase):

  def setUp(self):
    run_test_seed()
    
    sample_user = User.create_user('sample@user.com','sampleuser', 'test123')

  def tearDown(self) -> None:
    return super().tearDown()
  
  # valid construction
  def test_construction(self):

    # all arguments provided
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)

    # omitting document__slug__id
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-2', 
      name='Daedric Claymore', 
      weapon_category=3,
      # document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-2'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting document__title__id
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-3', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      # document__title__id=None, 
      document__license_url=None, 
      cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-3'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting document__license_url
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-4', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      document__title__id=None, 
      # document__license_url=None, 
      cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-4'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting cost_in_gp
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-5', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      # cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-5'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting weight
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-6', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      cost_in_gp=150, 
      # weight=10, 
      bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-6'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting bonus
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-7', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      cost_in_gp=150, 
      weight=10, 
      # bonus=2, 
      author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-7'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


    # omitting author_user_id WITH doc info
    new_weapon = Weapon.create_weapon(
      slug='daedric-claymore-8', 
      name='Daedric Claymore', 
      weapon_category=3,
      document__slug__id=1, 
      document__title__id=1, 
      document__license_url=1, 
      cost_in_gp=150, 
      weight=10, 
      bonus=2, 
      # author_user_id=1, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-8'}], 
      weapon_property_assignments=[6, 9], 
    )

    self.assertIsInstance(new_weapon, Weapon)


  # invalid construction 
  def test_invalid_construction(self):
    
    # omitting slug
    with self.assertRaises(TypeError):
      new_weapon = Weapon.create_weapon(
        # slug='daedric-claymore', 
        name='Daedric Claymore', 
        weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        author_user_id=1, 
        weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore'}], 
        weapon_property_assignments=[6, 9], 
      )

    # omitting name
    with self.assertRaises(TypeError):
      new_weapon = Weapon.create_weapon(
        slug='daedric-claymore', 
        # name='Daedric Claymore', 
        weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        author_user_id=1, 
        weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore'}], 
        weapon_property_assignments=[6, 9], 
      )

    # omitting author_user_id WITHOUT doc info
    with self.assertRaises(TypeError):
      new_weapon = Weapon.create_weapon(
        slug='daedric-claymore-8', 
        name='Daedric Claymore', 
        weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        # author_user_id=1, 
        weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-8'}], 
        weapon_property_assignments=[6, 9], 
      )

    # omitting weapon_category
    with self.assertRaises(ValueError):
      new_weapon = Weapon.create_weapon(
        slug='daedric-claymore-8', 
        name='Daedric Claymore', 
        # weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        author_user_id=1, 
        weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-8'}], 
        weapon_property_assignments=[6, 9], 
      )

    # invalid weapon_damage_rolls
    with self.assertRaises(TypeError):
      new_weapon = Weapon.create_weapon(
        slug='daedric-claymore-8', 
        name='Daedric Claymore', 
        weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        author_user_id=1, 
        weapon_damage_rolls={'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-8'}, 
        weapon_property_assignments=[6, 9], 
      )
    
    # invalid weapon_properties
    with self.assertRaises(TypeError):
      new_weapon = Weapon.create_weapon(
        slug='daedric-claymore-8', 
        name='Daedric Claymore', 
        weapon_category=3,
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        cost_in_gp=150, 
        weight=10, 
        bonus=2, 
        author_user_id=1, 
        weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 12, 'damage_type': 2, 'flat_damage': 10, 'weapon_slug': 'daedric-claymore-8'}], 
        weapon_property_assignments=6, 
      )


  # to_compat_json
  def test_to_compat_json(self):

    response = requests.get('https://api.open5e.com/weapons/greatsword/')
    api_greatsword_json = Weapon.api_doc_to_compat_json(response.json())

    my_greatsword = Weapon.create_weapon(
      slug="greatsword",
      name="Greatsword",
      weapon_category=3,
      document__slug__id=1, 
      document__title__id=1, 
      document__license_url=1, 
      cost_in_gp=50, 
      weight=6, 
      bonus=None, 
      author_user_id=None, 
      weapon_damage_rolls=[{'dice_no': 2, 'die_sides': 6, 'damage_type': 3, 'flat_damage': None, 'weapon_slug': 'greatsword'}], 
      weapon_property_assignments=[6, 15],
    )

    my_greatsword_json = my_greatsword.to_compat_json()
    # print(my_greatsword_json)    


    f = open('tests/api_greatsword.json', 'w')
    f.write(api_greatsword_json)
    f.close()
    f = open('tests/my_greatsword_json.json', 'w')
    f.write(my_greatsword_json)
    f.close()

    # check only keys in original json to avoid conflict on "bonus"
    my_greatsword_dict = json.loads(my_greatsword_json)
    api_greatsword_dict = json.loads(api_greatsword_json)
    for key in api_greatsword_dict.keys():
      self.assertEqual(api_greatsword_dict[key], my_greatsword_dict[key])
    
    # self.assertEqual(api_greatsword_json, my_greatsword_json)
