# WeightLossTracker
This is a website created using Django and MySQL. 
To get started add you MySQL database by editing /weighttracker/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',#Name of the database created for this project
        'USER': 'user_name',#Enter your mysql username
        'PASSWORD': 'password',#Enter your mysql password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```