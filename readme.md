# Dungeons and Dragons Repository

## Introduction

The goal of the site is to give Dungeons and Dragons players the opportunity to see official game content from several categories (Armor, Weapons, Spells, Classes), to share comments about individual items, and to create their own items of those same categories which can be viewed and commented on in the exact same way as the official content.

This project is referred to as dnd-repo as far as the url on heroku and the name on github, but the name on the site itself is Dragon's Hoard, and it can be found at [https://dnd-repo.herokuapp.com/](https://dnd-repo.herokuapp.com/).


## User Flow

The basic user flow is that a user will log in (or proceed without logging in), and be presented with links to each of the four categories. Whichever one they click on, they will then be taken to a list of all items in that category, including both official content from the API as well as user-created content which is saved onto the local database. 

At the top of each list, a button will present itself to logged in users to create an item of that category. Clicking that form will cause a form to appear, which will prompt the user for all the details they wish to include for the item that they create. If the form is filled out correctly, a message will flash that that item was created, and the user will be redirected to the page for that item.

Back on the list itself, each item will have a link to a "Page", as well as a button which says "Expand". Clicking the Expand button on an item will cause it to expand and show the full detail in place, whereas clicking on Page will take the user to a page that is just for that item in full detail. The views on the Expand option and the Page option will be virutally identical, but on each item's individual page will be a comments section, with comments specific to that item. Logged in users will be presented with a button to add a comment, which when clicked, will pop up a textarea that allows them to add a comment and submit it. A successful comment will return a flash message that their comment was saved.



## API and Tech Stack

The API that I will be using for this project is [Open 5e](https://open5e.com/api-docs). As I worked through this, I discovered that there were several areas in which API information was incomplete, (limited archetypes on class options, missing description areas, etc.) As such, current database models are built to reflect the APIs response schema for these items rather than the "true" descriptions of items, and adding in the full functionality which would improve on the API is an additional feature in consideration for future release. There is more detail about this in the section "Notes about models.py".

The tech stack is a Python back end using Flask, with server rendered jinja pages. There is minimal JavaScript, mostly just for revealing and concealing content on pages through button clicks. The database is handled through Flask-SQLAlchemy interfacing for PostgreSQL, and form validation is handled through WTForms.

As an additional note, the content on the API is not so big that this project would be much easier to simply download all API documents and adapt them to the format of the SQL database used locally. However, I chose not to do this because it seemed that doing so would be outside of the assignment's challenge to regularly use API calls as part of a user flow, and because I wanted to challenge myself fully with the database aspect of this project. This may very well seem counterintuitive, but this was an additional challenge that was taken on intentionally.

## Notes about models.py

The goal of these models is to give the ability to create database documents that approximate as much as possible the same kinds of documents that we will get back from the API. However, because the API responds with JSON, including arrays and repeated information (document licenses, etc.), it is necessary for the purposes of efficiency and data integrity to break the main four models up and to rely on several intermediate tables. Here are the main specific changes to keep in mind:

-Each of the main four models has its own method of 'to_compat_json', which will return a json object of virtually the same format as the API. The stringified version is useful for a direct comparison, and it can be translated into a dictionary using json.loads()

-The primary key of each of the main four models is its slug, which is used to retrieve the document. This is true of both the API and of custom documents saved to the database. Custom database items are prohibited from using the same slug as official content.

-Because slugs are specific to their group (weapons, armor, etc.), slugs are unique only within their group and not universally. For example, there could be a weapon with the slug of 'acid-arrow' and a spell with the same slug. These could be retrieved with 'weapons/acid-arrow' and 'spells/acid-arrow' respectively, so there is no conflict between these items. As a result, any document that uses the slug as a foreign key must already have that model table specified as a foreign key. This means that there is no model (or table) for 'comments', but there are models and tables for 'armor_comments', 'weapon_comments', etc.

-Slugs are functionally foreign keys for comments, but it must be permissible for them to point at null documents, as they can point not only at custom content saved to the database, but to documents that are only available via the API.

-Class Archetypes have been abandoned here for two reasons:
1. The complexity of adding a nested document into another document would likely be fairly easy as far as the SQL layout, but would be much more challenging in terms of implementing the form and handling. It would also clutter the class view which is already extremely text-intensive.
2. The API itself seems to actually have incomplete information on archetypes, listing only one archetype per class though there should be many.
This is a feature that could be built out more in a future revision, but would likely need to be its own document with a separate page view and creation process, which would also allow users to create their own custom archetypes established player classes (both user-generated and official). 

Note: This also means that 'archetypes' as far as spells are concerned will just be text that do not exist anywhere besides the 'archetype_spell_assignments' table


## Future Features

The following features are in consideration for future releases:

- Allow users to click on a page from home to see their own creations and comments
- See other users' items and comments (by user)
- Add search functionality
- Add checks in API calls in case service is down
- Add icons and artwork
- Allow users to modify their own content. It may be helpful to save past versions, and therefore have an item declare that there are older and/or newer versions of the item available.
- Class archetype handling
- Better rendering of classes, especially class tables
- Refactor views to cut down on repetition
- Split documents across multiple pages (ie 10 per page on the list view)
- Add other items (tools, races, languages, etc.)
