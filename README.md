# <p style="color:#7FFFD4">DjangoTimer</p>
<hr>
<h2 style="color:#00FFFF ">
Timer for company employees to calculate every employee's worked time.</h2> <br>

<p style="font-size: 18px;font-style: italic; color:#00BFFF;">
Web app includes minimal html/css frontend for employee's before frontend is
created with API's. The rest of the project consists of REST API's. <br>
Administrator can request every employee's worked time,when he/she came and when 
left office,also when the employee had break time.<br>
Also Celery with Redis automatically saves Daily and Monthly worked time.<br>
Monthly worked time = The monthly time each employeer spend in office - monthly break time. <br>
Daily worked time = The daily time each employeer spend in office - daily break time.<br>
Dockerfile with docker-compose consists of the main project with it's files and depends on redis-server.
</p>
<hr>
<h2>
Usage:<br>
</h2>
<p style="font-size: 18px; font-style: italic; color: #00BFFF">
1.Clone git repo <br>
  git clone https://github.com/anonymous203030/DjangoTimer
2.Go into repo<br>
  cd DjangoTimer
3.Activate virtualenv <br>
  python3 -m venv venv
4. Install python modules from requirements.txt file <br>
  pip3 install -r requirements.txt
5.Make all migrations to make Django programm work<br>
  ./manage.py makemigrations
  ./manage.py migrate
6. Run program on local server<br>
  ./manage.py runserver
- or <br>
  ./manage.py runserver <port that u want>
Example:<br>
  ./manage.py runserver 8080
<hr>
<br>
</p>
<h2 style="color:#00FFFF ">
Qualifications:<br>
</h2>
<p style="font-size: 18px; font-style: italic; color:#00BFFF;">
Python3, SQL, Linux, Docker, Celery, Redis,<br>
Django, Django-Rest-Framework, Django-ORM, Pillow, Git
</p>
