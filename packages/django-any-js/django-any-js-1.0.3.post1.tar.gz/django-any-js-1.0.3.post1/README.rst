Django Any-JS
=============

Description
-----------

Django-Any-JS helps you at including any combination of JavaScript/CSS
URLs in your site, with readable settings and template tags.

Usage
-----

In your settings:

::

    INSTALLED_APPS = [
                      ...,
                      'django_any_js',
                      ...
                     ]
    ANY_JS = {
              'DataTables': {
                             'js_url': '/javascript/jquery-datatables/dataTables.bootstrap4.min.js',
                             'css_url': '/javascript/jquery-datatables/css/dataTables.bootstrap4.min.css'
                            }
             }

In your template:

::

    {% load ... any_js %}
    {% include_js "DataTables" %}
    {% include_css "DataTables" %}
