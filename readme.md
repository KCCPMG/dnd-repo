# Dungeons and Dragons Repository

The API that I will be using for this project is [Open 5e](https://open5e.com/api-docs)

## models.py

The goal of these models is to give the ability to create database documents that approximate as much as possible the same kinds of documents that we will get back from the API. However, because the API responds with JSON, including arrays and repeat information, it is necessary for efficiency and data integrity to break the main four models up and to rely on several intermediate tables. Here are the main specific changes to keep in mind:

-Each of the main four models has its own method of 'to_compat_json', which will return a json object of virtually the same format as the API

-The primary key of each of the main four models is its slug, which is used to retrieve the document. This is true of both the API and of custom documents saved to the database.

-Because slugs are specific to their group (weapons, armor, etc.), slugs are unique only within their group and not universally. For example, there could be a weapon with the slug of 'acid-arrow' and a spell with the same slug. These could be retrieved with 'weapons/acid-arrow' and 'spells/acid-arrow' respectively. As a result, any document that uses the slug as a foreign key must already have that model table specified as a foreign key. This means that there is a model and table not for 'comments', but for 'armor_comments', 'weapon_comments', etc.

-Slugs are foreign keys for comments, but it must be permissible for them to point at null documents, as they can point not only at custom content saved to the database, but to documents that are only available via the API.

-Class Archetypes have been abandoned here for two reasons:
1. The complexity of adding a nested document into another document would likely be fairly easy as far as the SQL layout, but much more challenging in terms of implementing the form and handling.
2. The API itself seems to actually have incomplete information on archetypes, listing only one archetype per class though there should be many.
This is a feature that could be built out more in a future revision, but would likely need to be its own document with a separate page view and creation process, which would also allow users to create their own archetypes on player classes that other users have created, as well as on official documents. (This also means that 'archetypes' as far as spells are concerned will just be text that do not exist anywhere besides the 'archetype_spell_assignments' table)


## Future Features

- Allow users to click on a page from home to see their own creations and comments
- See other users' items and comments
- Refactor views to cut down on repetition