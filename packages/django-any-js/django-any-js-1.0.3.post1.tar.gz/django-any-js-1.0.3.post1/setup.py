import os
from setuptools import setup

MYDIR = os.path.dirname(__file__)

setup(
    name='django-any-js',
    version='1.0.3.post1',
    keywords=['django', 'javascript'],
    description='Include JavaScript libraries with readable template tags',
    long_description=open(os.path.join(MYDIR, "README.rst"),
                          "r", encoding="utf-8").read(),
    url='https://edugit.org/AlekSIS/libs/django-any-js',
    author='Dominik George',
    author_email='dominik.george@teckids.org',
    packages=['django_any_js', 'django_any_js.templatetags'],
    include_package_data=True,
    install_requires=['Django>=1.11'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
