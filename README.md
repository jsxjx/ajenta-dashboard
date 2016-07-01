# Ajenta dashboard

## Overview
This Django app generates usage reports in the form of graphs and pie charts.

The available reports are the following:

* User Stats - Returns the 10 most active users for the given date range.
* Rooms Stats - Returns the 10 most active rooms for the given date range. 
* Calls per day - Returns the calls for each day for the given date range. 
* Maximum concurrent lines - Returns the concurrent line usage peaks for each day for the given date range.
* Calls per country - Returns the number of calls for each different country (available only for specific users).
* Platform Stats - Returns the number of calls performed from each different platform (e.g VidyoWeb, VidyoDesktop, VidyoMobile etc).
* OS Stats - Returns the number of calls performed from each different operating system (e.g Windows, OS X, Linux etc).

The app is is deployed on https://dashboard.ajenta.io. 

You need a username and a password provided by Ajenta in order to login to this page.

## Structure

The following tree diagram shows the code structure:

```
├── ajenta_dashboard
│   ├── __init__.py
│   ├── production_settings.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── authentication
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── dashboard
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── graphs.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── queries.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   ├── favicon.ico
│   └── UsersExport.csv
├── templates
│   ├── 403.html
│   ├── 404.html
│   ├── 500.html
│   ├── auth
│   │   ├── change_password.html
│   │   ├── create_user.html
│   │   └── login.html
│   ├── base.html
│   ├── index.html
│   └── stats
│       ├── calls_by_country.html
│       ├── calls_per_day.html
│       ├── concurrent_lines.html
│       ├── os_stats.html
│       ├── platform_stats.html
│       ├── room_stats.html
│       └── user_stats.html
```

The ```ajenta_dashboard``` directory contains the settings of this project (both for development and production) as well as the ```urls.py``` and ```wsgi.py```.


There are two main apps in this Django project:

* The ```authentication``` app handles the user creation and login functionality using Django's authentication system.

* The ```dashboard``` app contains the core functionality of the project:
     * The ```models.py``` reflects the models as read from the MySQL database using Django's ```inspcetdb``` command.
     * The ```queries.py``` performs all the queries required to generate the reports using Django's ORM.
     * The ```graphs.py``` generates the graphs and pie charts using Python's Plotly.

Finally there are two directories with the non-Python code
* The ```static``` directory contains the static files for this app, such as the CSS.
* The ```templates``` directory contains all the HTML forms used in this app.

