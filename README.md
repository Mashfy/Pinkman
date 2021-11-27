This is a fully functional Ecommerce website implemented by Django.
try it youself - http://ecommercepinik.pythonanywhere.com/
![](app/static/app/images/1.png)

To run the project in your machine

Install virtual environment:
```
pip install virtualenv
```
Create your own environment
```
virtualenv yourenvname
```
Activate your environemnt
```
yourenvname\Scripts\activate
```
Now install requirements.txt
```
pip install -r requirements.txt
```

There is two database portion in this website, if you want to use the sqlite, which is easier then uncomment the Database setting portion of sqlite in settings.py and comment out the mysql portion.<br>
If you want to use mysql database, you have to locally create the database named ecom in your local machine, then migrate the model in it. Get help from [here](https://studygyaan.com/django/how-to-use-mysql-database-with-django-project).

Then run the server
```
python manage.py runserver
```
