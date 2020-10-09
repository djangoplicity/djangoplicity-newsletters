# Djangoplicity Newsletters

![Coverage](https://img.shields.io/codecov/c/github/djangoplicity/djangoplicity-newsletters/develop)
![Size](https://img.shields.io/github/repo-size/djangoplicity/djangoplicity-newsletters)
![License](https://img.shields.io/github/license/djangoplicity/djangoplicity-newsletters)
![Language](https://img.shields.io/github/languages/top/djangoplicity/djangoplicity-newsletters)

Djangoplicity Newsletters is a dependency of the [Djangoplicity](https://github.com/djangoplicity/djangoplicity) CMS
created by the European Southern Observatory (ESO) for managing Newsletters, Mailing Lists, Subscribers and so much more.

## Installation

If you are using Docker, you can look for an example in `Dockerfile` and `docker-compose.yml` files located in the root
of the repository.
### Requirements

Djangoplicity Newsletters actually supports Python 2.7 and Python 3+.

You must install Djangoplicity Newsletters using the Github repository, so add the following packages to your
requirements depending on the Python version you are using.
```
# Asynchronous Task Queue
celery==4.3.0

# For Python 3+

# Djangoplicity actions
git+https://@github.com/djangoplicity/djangoplicity-actions@release/python3

# Djangoplicity newsletters
git+https://@github.com/djangoplicity/djangoplicity-newsletters.git@release/python3

# Djangoplicity
git+https://@github.com/djangoplicity/djangoplicity.git@release/python3

# For Python 2.7

# Djangoplicity actions
git+https://@github.com/djangoplicity/djangoplicity-actions@develop

# Djangoplicity newsletters
git+https://@github.com/djangoplicity/djangoplicity-newsletters.git@develop

# Djangoplicity
git+https://@github.com/djangoplicity/djangoplicity.git@develop
```
Celery is also required for some asynchronous tasks to work.

Now include the package in your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'djangoplicity.actions',
    'djangoplicity.admincomments',
    'djangoplicity.archives.contrib.security',
    'djangoplicity.archives',
    'djangoplicity.metadata',
    'djangoplicity.mailinglists',
    'djangoplicity.newsletters',
    'djangoplicity.reports',
    'django_mailman',
    'tinymce'
]
```

Djangoplicity requires some additional settings in order to work, so add this configuration to your `settings.py` 
file (you don't have to include those files in your assets):

```python
##############
# JavaScript #
##############
JQUERY_JS = "jquery/jquery-1.11.1.min.js"
JQUERY_UI_JS = "jquery-ui-1.12.1/jquery-ui.min.js"
JQUERY_UI_CSS = "jquery-ui-1.12.1/jquery-ui.min.css"
DJANGOPLICITY_ADMIN_CSS = "djangoplicity/css/admin.css"
DJANGOPLICITY_ADMIN_JS = "djangoplicity/js/admin.js"
SUBJECT_CATEGORY_CSS = "djangoplicity/css/widgets.css"

NEWSLETTERS_ARCHIVE_ROOT = 'archives/newsletters/'

ENABLE_ADVANCED_SEARCH = True
ADV_SEARCH_START_YEAR = 1998
```

You also have to add `tinymce` settings:
```python
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
        textcolor save link image media preview codesample table
        code lists fullscreen  insertdatetime  nonbreaking contextmenu
        directionality searchreplace wordcount visualblocks visualchars
        code fullscreen autolink lists  charmap print  hr anchor pagebreak
    ''',
    'toolbar1': '''
        fullscreen code | cut copy | searchreplace | alignleft aligncenter alignright alignjustify | formatselect forecolor backcolor | superscript subscript |
     ''',
    'toolbar2': '''
        bold italic underline strikethrough | bullist numlist table hr | indent outdent | undo redo | link unlink anchor image media charmap | nonbreaking |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'statusbar': True,
    'entity_encoding': 'raw',
    'convert_urls': False,
}
```

Now, add the following imports to your `CELERY_IMPORTS` variable. You can create it if you don't have one, just be sure that you have properly configured Celery for the project.
```python
CELERY_IMPORTS = [
    "djangoplicity.archives.contrib.security.tasks",
    "djangoplicity.celery.tasks",
]
```

Next, you have to register the models in your `admin.py` file.
```python
import django.contrib.auth.admin
import django.contrib.redirects.admin
import django.contrib.sites.admin
import djangoplicity.actions.admin
from djangoplicity.contrib.admin.discover import autoregister
from djangoplicity.contrib.admin.sites import AdminSite

import djangoplicity.mailinglists.admin
import djangoplicity.newsletters.admin

# Register each applications admin interfaces with
# an admin site.
admin_site = AdminSite(name="admin_site")
adminlogs_site = AdminSite(name="adminlogs_site")
adminshop_site = AdminSite(name="adminshop_site")

autoregister(admin_site, django.contrib.auth.admin)
autoregister(admin_site, django.contrib.sites.admin)

autoregister(admin_site, djangoplicity.mailinglists.admin)
autoregister(admin_site, djangoplicity.newsletters.admin)
autoregister(adminlogs_site, djangoplicity.actions.admin)

#
# Applications that does not support above method.
#
djangoplicity.reports.admin.advanced_register_with_admin(admin_site)

adminlogs_site.register(django.contrib.redirects.models.Redirect, django.contrib.redirects.admin.RedirectAdmin)

adminlogs_site.register(django.contrib.sites.models.Site, django.contrib.sites.admin.SiteAdmin)

admin_site.register(django.contrib.auth.models.User, django.contrib.auth.admin.UserAdmin)

admin_site.register(django.contrib.auth.models.Group, django.contrib.auth.admin.GroupAdmin)
```

## Migration

Next, make the migrations for the `django_mailman` package:
```bash
python manage.py makemigrations django_mailman
```
And run the migrations:
```bash
python manage.py migrate
```

## Development

This repository includes an example project for local development located in the test_project folder. You can find
there the basic configuration to get a project working.
 
### Cloning the repository

In your terminal run the command:

```` 
git clone https://gitlab.com/djangoplicity/djangoplicity-newsletters.git
````

### Running the project

All the configuration to start the project is present in the docker-compose files and Dockerfile,
then at this point a single command is required to download all the dependencies and run the project:

```` 
docker-compose up
````

> The previous command reads the config from docker-compose.yml. 

When the process finishes, the server will be available at *`localhost:8002`*

To stop containers press `CTRL + C` in Windows or `⌘ + C` in MacOS

If the dependencies change, you should recreate the docker images and start the containers again with this command:

```` 
docker-compose up --build
````

### Additional commands

Inside the `Makefile` there are multiple command shortcuts, they can be run in UNIX systems like this:

```
make <command-name>
```

E.g.

```
make migrate
```

> In Windows you can just copy and paste the related command
