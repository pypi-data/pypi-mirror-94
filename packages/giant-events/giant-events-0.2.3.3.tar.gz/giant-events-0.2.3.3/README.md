# Giant Events

A re-usable package which can be used in any project that requires a generic `Events` app. 

This will include the basic formatting and functionality such as model creation via the admin.

## Installation

To install with the package manager, run:

    $ poetry add giant-events

You should then add `"events", "easy_thumbnails" and "filer"` to the `INSTALLED_APPS` in `base.py`.  


## Configuration

This application exposes the following settings:

- `EVENT_ADMIN_LIST_DISPLAY` is the field list for the admin index. This must be a list
- `EVENT_ADMIN_FIELDSETS` allows the user to define the admin fieldset. This must be a list of two-tuples
- `EVENT_ADMIN_READONLY_FIELDS` allows the user to configure readonly fields in the admin. This must be a list
- `EVENT_ADMIN_SEARCH_FIELDS` allows the user to configure search fields in the admin. This must be a list
- `EVENT_ADMIN_FILTER_FIELDS` allows the user to configure filter fields in the admin. This must be a list

By default the app will use the templates that are defined inside the app directory itself. However if you wish to override which template is used you will need to create a directory in the projects template directory
The structure should look something like this:

```
templates/
    events/
        index.html
        detail.html
```



## URLs

Add the following to `core.urls` for general functionality:

    path("events/", include("events.urls"), name="events"),

If you want to customize the urls to include a different path and/or templates, first you must import `from events import views as event_views` in `core.urls` and then you could add the following:

    path("events/", event_views.EventIndex.as_view(template_name="event/index.html"), name="event-index"),
    path("events/<slug:slug>/", event_views.EventDetail.as_view(template_name="event/detail.html"), name="event-detail"),
 
 ## Preparing for release
 
 In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.
 This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.
 
 ## Publishing
 
 Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.
 
    $ `poetry build` 

will package the project up for you into a way that can be published.
 
    $ `poetry publish`

will publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager