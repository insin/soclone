SET DJANGO_SETTINGS_MODULE=soclone.settings
REM Requires http://code.google.com/p/django-command-extensions/ in INSTALLED_APPS
django-admin.py graph_models -a -g > models.dot
REM Requires Graphviz - http://www.graphviz.org/
dot models.dot -Tpng -o models.png