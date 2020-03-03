pip3 install virtualenv
virtualenv ENV
source ENV/bin/activate
python3 -m pip install Django
django-admin startproject tcs
cd tcs
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

# changes required in settings
# add apps in installed apps
# in templates change 'DIRS': [os.path.join(BASE_DIR,'tcs/templates')],

pip3 install django-crispy-forms
# INSTALLED_APPS = [
# 	...
#     'crispy_forms',
# ]
# CRISPY_TEMPLATE_PACK = 'bootstrap4'
# <head><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"></head>
# {% load crispy_forms_tags %} in each html |crispy in each form