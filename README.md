# elemental-alerts
Alerting service based on Elemental Machines API

## Design
The app is built in the Django MVC framework. It needs a vanilla install of python 2.7 with the following imports: Django (version 1.11), twilio, and slumber (for calls to api.elementalmachines.io). The persistence layer is a SQLite db which is stored in a local file.

The app has a command called checkMachines which is called periodically from a crontab. That command iterates through all known machines and does the following:
* Get the machine alert settings (valid temperature range)
* Get the machine samples, starting after the last sample taken
* Compare each sample with the last sample to find state changes (if temp falls out of range or back in range)
* When there is a state change, call the twilio API code to send an alert (and log the same alert)
* Save the last known state of the machine to use on the next run

There is one python module for calls to api.elementalmachines.io (using the Slumber library), and another module for calls to Twilio (using their own python library)

The app has a single template, which shows the state of each machine along with a list of the last 20 alerts fired. This is available on [http://ec2-54-208-233-56.compute-1.amazonaws.com:8000/poller/].

Additionally, the Django built in Admin templates (which are scaffolded by the framework) can be used to view/edit/delete all Machine and Alert objects persisted in the local SQLite database: [http://ec2-54-208-233-56.compute-1.amazonaws.com:8000/admin/poller/] (credentials are admin/admin123)

## Next steps
Additional clean-up time on this code base should be spend on the following tasks:
* Write some tests for it with static input data (by mocking out the api.elementalmachines.io calls)
* Add code to check for pre-conditions/post-conditions (i.e. check that user has an attribute for 'mobile', alert settings is not null for a given machine, etc)
* Move sensitive settings (passwords, API keys) from settings.py file in the git repo to environment variables
* Add docstrings to each function in the python packages
