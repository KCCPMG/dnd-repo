import os
from unittest import TestCase
from sqlalchemy import exc
import requests
import json


from models import Spell, User, PlayerClass

from tests.test_seed import run_test_seed

os.environ['DATABASE_URL'] = "postgresql:///dnd-repo-test"

from app import app


description_string = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Molestias aut, repellat ipsum facere voluptate dicta obcaecati deserunt nobis suscipit eaque?"
higher_level_string = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Molestias aut, repellat ipsum facere voluptate dicta obcaecati deserunt nobis suscipit eaque?"

class SpellTest(TestCase):

  def setUp(self) :
    run_test_seed()
    
    sample_user = User.create_user('sample@user.com','sampleuser', 'test123')

  def tearDown(self) -> None:
    return super().tearDown()
  
  # valid construction
  def test_construction(self):

    new_spell = Spell.create_spell(
      slug='test-spell',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit document__slug__id
    new_spell = Spell.create_spell(
      slug='test-spell-1',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      # document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit document__title__id
    new_spell = Spell.create_spell(
      slug='test-spell-2',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      # document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit document__license_url
    new_spell = Spell.create_spell(
      slug='test-spell-3',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      # document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit circles
    new_spell = Spell.create_spell(
      slug='test-spell-4',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      # circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit author_user_id with doc info
    new_spell = Spell.create_spell(
      slug='test-spell-5',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=1, 
      document__title__id=1, 
      document__license_url=1, 
      circles="Nature", 
      # author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit spell_components
    new_spell = Spell.create_spell(
      slug='test-spell-6',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      # spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit class_slug_spell_assignments
    new_spell = Spell.create_spell(
      slug='test-spell-7',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      # class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit archetype_spell_assignments
    new_spell = Spell.create_spell(
      slug='test-spell-8',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      # archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit concentration
    new_spell = Spell.create_spell(
      slug='test-spell-9',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      # concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit magic_school
    new_spell = Spell.create_spell(
      slug='test-spell-10',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      # magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)

    # omit material
    new_spell = Spell.create_spell(
      slug='test-spell-11',
      name="Test Spell",
      description=description_string,
      higher_level=higher_level_string, 
      page=None, 
      spell_range="100 ft", 
      # material="Powder of Ibn-Ghazi", 
      ritual=False, 
      duration="instant", 
      concentration=False, 
      casting_time="1 action", 
      level=3, 
      magic_school=3, 
      document__slug__id=None, 
      document__title__id=None, 
      document__license_url=None, 
      circles="Nature", 
      author_user_id=1, 
      spell_components=["V", "S", "M"],
      class_slug_spell_assignments=[],
      archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
    )

    self.assertIsInstance(new_spell, Spell)


  # invalid construction
  def test_invalid_construction(self):
    
    # omit slug
    with self.assertRaises(TypeError):
      new_spell = Spell.create_spell(
        # slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit name
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        # name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit description
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        # description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit higher_level
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        # higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit spell_range
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        # spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    
    # omit ritual
    with self.assertRaises(TypeError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        # ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit duration
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        # duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )



    # omit casting_time
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        # casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    # omit level
    with self.assertRaises(ValueError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        # level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )

    
    # omit author_user_id without doc info
    with self.assertRaises(TypeError):
      new_spell = Spell.create_spell(
        slug='test-spell-fail',
        name="Test Spell",
        description=description_string,
        higher_level=higher_level_string, 
        page=None, 
        spell_range="100 ft", 
        material="Powder of Ibn-Ghazi", 
        ritual=False, 
        duration="instant", 
        concentration=False, 
        casting_time="1 action", 
        level=3, 
        magic_school=3, 
        document__slug__id=None, 
        document__title__id=None, 
        document__license_url=None, 
        circles="Nature", 
        # author_user_id=1, 
        spell_components=["V", "S", "M"],
        class_slug_spell_assignments=[],
        archetype_spell_assignments=["Warlock: Path of Test", "Druid: Circle of the Test"]
      )


  # to_compat_json
  def test_to_compat_json(self):
    
    response = requests.get('https://api.open5e.com/spells/anchoring-rope/')
    api_spell_json = Spell.api_doc_to_compat_json(response.json())

    # creating my version of Bard, Druid, Ranger for use with spell, only to get correct slug and name
    bard = PlayerClass.create_player_class(
      slug= 'bard',
      name= 'Bard',
      description= 'A man approaches. He speaks the word "doom". From everywhere, destruction ensues.',
      hit_die= 8,
      base_hp_at_1st_level= 10,
      tool_proficiency= 'Sextant, compass, game boy color',
      skill_proficiency= "Athletics, Regurgitation",
      starting_equipment= "A guitar, a bass, a rocket launcher",
      table= "Oh oh, no more table.",
      spellcasting_ability= 4,
      subtypes_name= "Night Child",
      document__slug__id= None,
      document__title__id= None,
      document__license_url= None,
      author_user_id= 1,
      armor_proficiencies = [1, 2, 5],
      prof_weapons = "Longsword",
      saving_throw_ids = [4, 5],
      homebrew_spell_slugs = ['make-explode'],
      api_spell_slugs = ["doom-of-serpent-coils", "doom-of-blue-crystal"]
    )
    druid = PlayerClass.create_player_class(
      slug= 'druid',
      name= 'Druid',
      description= 'A man approaches. He speaks the word "doom". From everywhere, destruction ensues.',
      hit_die= 8,
      base_hp_at_1st_level= 10,
      tool_proficiency= 'Sextant, compass, game boy color',
      skill_proficiency= "Athletics, Regurgitation",
      starting_equipment= "A guitar, a bass, a rocket launcher",
      table= "Oh oh, no more table.",
      spellcasting_ability= 4,
      subtypes_name= "Night Child",
      document__slug__id= None,
      document__title__id= None,
      document__license_url= None,
      author_user_id= 1,
      armor_proficiencies = [1, 2, 5],
      prof_weapons = "Longsword",
      saving_throw_ids = [4, 5],
      homebrew_spell_slugs = ['make-explode'],
      api_spell_slugs = ["doom-of-serpent-coils", "doom-of-blue-crystal"]
    )
    ranger = PlayerClass.create_player_class(
      slug= 'ranger',
      name= 'Ranger',
      description= 'A man approaches. He speaks the word "doom". From everywhere, destruction ensues.',
      hit_die= 8,
      base_hp_at_1st_level= 10,
      tool_proficiency= 'Sextant, compass, game boy color',
      skill_proficiency= "Athletics, Regurgitation",
      starting_equipment= "A guitar, a bass, a rocket launcher",
      table= "Oh oh, no more table.",
      spellcasting_ability= 4,
      subtypes_name= "Night Child",
      document__slug__id= None,
      document__title__id= None,
      document__license_url= None,
      author_user_id= 1,
      armor_proficiencies = [1, 2, 5],
      prof_weapons = "Longsword",
      saving_throw_ids = [4, 5],
      homebrew_spell_slugs = ['make-explode'],
      api_spell_slugs = ["doom-of-serpent-coils", "doom-of-blue-crystal"]
    )

    my_spell = Spell.create_spell(
      slug = 'anchoring-rope',
      name = 'Anchoring Rope',
      description = 'You create a spectral lanyard. One end is tied around your waist, and the other end is magically anchored in the air at a point you select within range. You can choose to make the rope from 5 to 30 feet long, and it can support up to 800 pounds. The point where the end of the rope is anchored in midair can’t be moved after the spell is cast. If this spell is cast as a reaction while you are falling, you stop at a point of your choosing in midair and take no falling damage. You can dismiss the rope as a bonus action.\n',
      higher_level =  "When you cast this spell using a spell slot of 3rd level or higher, you can create one additional rope for every two slot levels above 1st. Each rope must be attached to a different creature.",
      page = None,
      spell_range = "30 feet",
      material=None,
      ritual=False,
      duration="5 minutes",
      concentration=False,
      casting_time="1 action, or 1 reaction that you take while falling",
      level=1,
      magic_school=5,
      document__slug__id=2,
      document__title__id=2,
      document__license_url=1,
      circles=None,
      author_user_id=None,
      spell_components=["V", "S"],
      class_slug_spell_assignments=['bard', 'druid', 'ranger'],
      archetype_spell_assignments=[]
    )

    my_spell_json = my_spell.to_compat_json()

    api_spell_dict = json.loads(api_spell_json)
    my_spell_dict = json.loads(my_spell_json)

    
    self.assertTrue(api_spell_dict.keys() == my_spell_dict.keys())

    self.assertEqual(api_spell_dict, my_spell_dict)