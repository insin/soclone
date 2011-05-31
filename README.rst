SOClone
=======

10 days' worth of furious hacking at a Stack Overflow clone for Django
in October 2008.

`OSQA`_ seems to have taken the ball and run with it, so not sure if I'll
ever take this one any further.

.. _`OSQA`: http://www.osqa.net/

Dependencies
------------

1. `django_html`_ for rendering ``django.forms`` components using HTML
   instead of XHTML.

2. `python-markdown2`_ for converting Markdown-formatted user input
   into HTML.

3. `html5lib`_ for HTML sanitisation.

4. `lxml`_ for HTML diffing.

5. Oh, and `Django`_ 1.2 or greater, of course.

.. _`django_html`: http://github.com/simonw/django-html
.. _`python-markdown2`: http://code.google.com/p/python-markdown2/
.. _`html5lib`: http://code.google.com/p/html5lib/
.. _`lxml`: http://codespeak.net/lxml/
.. _`Django`: http://www.djangoproject.com/

Installation
------------

To play around with SOClone:

1. Use the pip-requirements.txt file to install dependencies with pip.

2. Run the following command to create the database::

      django-admin.py syncdb --settings=soclone.settings

   You will be prompted to create a superuser.

3. Run the following command to start the development server::

      django-admin.py runserver --settings=soclone.settings

4. Cross your fingers, open http://localhost:8000/questions/ and log in
   with the superuser account you created.

   Here be dragons.
