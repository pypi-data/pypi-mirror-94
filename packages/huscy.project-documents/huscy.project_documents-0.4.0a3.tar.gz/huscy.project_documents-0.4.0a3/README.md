huscy.project_documents
======

![alt](https://img.shields.io/pypi/v/huscy-project_documents.svg)
![alt](https://img.shields.io/pypi/pyversions/huscy-project_documents.svg)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.0, 2.1, 2.2 and 3.0.



Installation
------

To install `husy.project_documents` simply run:
```
pip install huscy.project_documents
```



Configuration
------

We need to hook `huscy.project_documents` into our project.
This package depends on `projects` so we have to add this as well.
We also have to add further requirements for django_guardian and django_restframework.

1. Add packages into your `INSTALLED_APPS` at settings module:

```python
INSTALLED_APPS = (
    ...
    'guardian',
    'rest_framework',

    'huscy.project_documents',
    'projects',
)
```

2. Create `huscy.project_documents` database tables by running:

```
python manage.py migrate
```


Development
------

After checking out the repository you should run

```
make install
```

to install all development and test requirements and

```
make migrate
```

to create the database tables.
We assume you have a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123'"
sudo -u postgres createdb huscy
```
