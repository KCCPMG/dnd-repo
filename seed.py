from app import db
from models import User, ArmorComment, WeaponComment, SpellComment, ClassComment, Armor, ArmorCategory, DamageType, WeaponDamageRoll, WeaponProperty, WeaponPropertyAssignment, WeaponCategory, Weapon, Attribute, DocumentSlug, DocumentTitle, DocumentLicenseURL, SpellComponent, ClassSpellSlugAssignment, ArchetypeSpellAssignment, MagicSchool, Spell, PlayerClass, WeaponProficiency, SavingThrow, ArmorModifierAttribute


db.session.rollback()
db.drop_all()
db.create_all()


db.session.add_all([
  # armor types
  ArmorCategory(name='No Armor'), 
  ArmorCategory(name='Light Armor'), 
  ArmorCategory(name='Medium Armor'),
  ArmorCategory(name="Heavy Armor"), 
  ArmorCategory(name='Spell'),
  ArmorCategory(name='Class Feature'), 
  ArmorCategory(name='Shield'),  
  

  # weapon categories
  WeaponCategory(name='Simple Melee Weapons'), 
  WeaponCategory(name='Simple Ranged Weapons'), 
  WeaponCategory(name='Martial Melee Weapons'), 
  WeaponCategory(name='Martial Ranged Weapons'),


  # damage types
  DamageType(name='bludgeoning'),
  DamageType(name='piercing'),
  DamageType(name='slashing'),
  DamageType(name='acid'),
  DamageType(name='poison'),
  DamageType(name='fire'),
  DamageType(name='cold'),
  DamageType(name='force'),
  DamageType(name='lightning'),
  DamageType(name='thunder'),
  DamageType(name='necrotic'),
  DamageType(name='psychic'),
  DamageType(name='radiant'),


  # weapon properties (need to enable adding more)
  WeaponProperty(name='ammunition (range 30/120)'),
  WeaponProperty(name='ammunition (range 25/100)'),
  WeaponProperty(name='ammunition (range 100/400)'),
  WeaponProperty(name='ammunition (range 150/600)'),
  WeaponProperty(name='finesse'),
  WeaponProperty(name='heavy'),
  WeaponProperty(name='light'),
  WeaponProperty(name='loading'),
  WeaponProperty(name='range'),
  WeaponProperty(name='reach'),
  WeaponProperty(name='special'),
  WeaponProperty(name='thrown (range 5/15)'),
  WeaponProperty(name='thrown (range 20/60)'),
  WeaponProperty(name='thrown (range 30/120)'),
  WeaponProperty(name='two-handed'),
  WeaponProperty(name='versatile (1d8)'),
  WeaponProperty(name='versatile (1d10)'),



  # magic schools
  MagicSchool(name='illusion'),
  MagicSchool(name='transmutation'),
  MagicSchool(name='conjuration'),
  MagicSchool(name='necromancy'),
  MagicSchool(name='evocation'),
  MagicSchool(name='abjuration'),
  MagicSchool(name='enchantment'),
  MagicSchool(name='divination'),


  # attributes
  Attribute(name='Strength'),
  Attribute(name='Dexterity'),
  Attribute(name='Constitution'),
  Attribute(name='Wisdom'),
  Attribute(name='Intelligence'),
  Attribute(name='Charisma'),


  # documents slugs
  DocumentSlug(slug='wotc-srd'),
  DocumentSlug(slug='dmag'),
  DocumentSlug(slug='o5e'),

  # document titles
  DocumentTitle(title='Deep Magic for 5th Edition'),
  DocumentTitle(title='Systems Reference Document'),
  DocumentTitle(title='Open5e OGL'),

  # document license urls
  DocumentLicenseURL(url='http://open5e.com/legal')

])

# samples
user = User.create_user('jack@be.nimble','jackieboy', 'test123')

db.session.commit()

armor_comment = ArmorComment.add_comment('armor', user.id, "this is my armor comment content")

weapon_comment = WeaponComment.add_comment('weapon', user.id, "this is my weapon comment content")

spell_comment = SpellComment.add_comment('spell', user.id, "this is my spell comment content")

class_comment = ClassComment.add_comment('class', user.id, "this is my class comment content")

new_armor = Armor.create_armor(slug="slug", 
                                name="Slug", 
                                category_id=3, 
                                document__slug__id=1, 
                                document__title__id=1, 
                                document__license_url=1, 
                                ac_base=5, 
                                modifier_attributes=["Dexterity", "Wisdom"],
                                max_modifier=2, 
                                strength_required=12, 
                                cost_in_gp=0, 
                                # weight=10, 
                                stealth_disadvantage=False, 
                                author_user_id=user.id)

new_armor_comment = ArmorComment.add_comment('slug', user.id, "this is my new  armor joining comment content")


db.session.add_all([new_armor_comment])

new_modifier = ArmorModifierAttribute.create_armor_modifier_attribute(armor_slug="slug", attribute="Strength")

db.session.commit()



print(user.to_json())
print(armor_comment.to_json())
print(weapon_comment.to_json())
print(spell_comment.to_json())
print(class_comment.to_json())
print(Armor.get_comments(new_armor_comment.slug))