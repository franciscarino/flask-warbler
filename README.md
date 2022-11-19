# 🪶 Warbler

Inspired by Twitter, Warbler is a serverside microblogging application that allows users to follow others, favorite posts, and add posts.

[Demo](https://warbler-fc.herokuapp.com/)

#### Demo Login ####
- Username: user1
- Password: password

![SharebnbDemoGif](https://raw.githubusercontent.com/franciscarino/flask-warbler/main/static/images/warbler-demo.gif)


### Tech Stack
- Python
- Flask
- PostgreSQL
- SQL Alchemy
- Jinja 
- WTForms
- bcrypt
- HTML
- CSS
- Bootstrap


### Run on your machine
1. Clone the repository, create a virtual environment and install depencencies
```
$ git clone https://github.com/franciscarino/flask-warbler.git
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

2. Setup the database
```
(venv) $ psql
=# CREATE DATABASE warbler;
=# (control-d)
(venv) $ python seed.py
```

3. Create .env file for config
```
SECRET_KEY=*****
DATABASE_URL=postgresql:///warbler
```

4. Start the server and view in browser
```
$ flask run -p 5001
```
This runs the app in the development mode.
Open [http://localhost:5001](http://localhost:5001) to view it in your browser.

