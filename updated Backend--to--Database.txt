####### Backend-flask project #############

process::
step-1
-->>Create rds with security group "port 3306 and all traffic enabled" 
-->>now connect sql work bench with your rds credentials
--->>now create database and run through workbench


CREATE DATABASE dev;
USE dev;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);


step-2
launch ec2 instance with security group "all traffic enabled"

step-3
attach iam role  "ec2-admin"

step-4
install dependencies

yum install python3-pip -y
pip install flask mysql-connector-python

step-5
suppose if we are importing data from git-hub, we need to install git first to access git-hub account
yum install git -y

step-6
clone the git-hub
git clone https://github.com/CloudTechDevOps/python-backend-testing.git

step-7
[root@ip-172-31-15-35 ~]# ls
python-backend-testing
[root@ip-172-31-15-35 ~]# cd python-backend-testing/
[root@ip-172-31-15-35 python-backend-testing]# ls
app.py

step-8
[root@ip-172-31-15-35 python-backend-testing]# vi app.py

insert rds crentiantials

# Database Configuration
db_config = {
    'host': 'database-1.cv06coymad1g.ap-south-1.rds.amazonaws.com',    ##endpoints
    'user': 'admin',                                                                                            ##username
    'password': 'admin123',                                                                             ###password
    'database': 'dev'  # Change to your actual database name

step-9

[root@ip-172-31-15-35 python-backend-testing]# python3 app.py                    #### run app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.31.15.35:5000

Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 124-338-485

note-if we want to stop press "ctrl+c" to exit

step-10
open new console window and switch to root
and then run command given below one-by-one


### API Methods -->> we need to conduct all activities after backend-to rds -connection establish ###



Updated Flask App with Full API Methods
This includes:

GET /users → Fetch all users
POST /users/add → Add a new user
GET /users/<id> → Fetch a single user by ID
PUT /users/update/<id> → Update a user's info
DELETE /users/delete/<id> → Delete a user

#### Post method ###   --->To add new user post method 

curl -X POST http://localhost:5000/users/add      -H "Content-Type: application/json"      -d '{"name":"John DDoe", "email":"john@example.com"}'

[root@ip-172-31-15-35 ~]# curl -X POST http://localhost:5000/users/add      -H "Content-Type: application/json"      -d '{"name":"John DDoe", "email":"john@example.com"}'
{
  "message": "User added successfully"
}


#### Get method ###   --->To Fetch all users
curl -X GET http://localhost:5000/users 

[root@ip-172-31-15-35 ~]# curl -X GET http://localhost:5000/users
[
  {
    "email": "john@example.com",
    "id": 1,
    "name": "John DDoe"
  }
]


#### Get method ###  --->To Fetch single users
curl -X GET http://localhost:5000/users/1 
[root@ip-172-31-15-35 ~]# curl -X GET http://localhost:5000/users/1 
{
  "email": "john@example.com",
  "id": 1,
  "name": "John DDoe"
}



#### Put method ###  --->To update user post method 

curl -X PUT http://localhost:5000/users/update/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated", "email": "john.updated@example.com"}'

[root@ip-172-31-15-35 ~]# curl -X PUT http://localhost:5000/users/update/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated", "email": "john.updated@example.com"}'
{
  "message": "User updated successfully"
}


### how to check API request from external #########

step-1
https://web.postman.co/            ### signup with your credentials " git-hub or any other account

step-2
once to logged-in
workspace----->>>>new---->>>select http

step-3
enter url to check api activities
 
http://43.204.228.245:5000/users    ### to check all users

http://43.204.228.245:5000/users/1  ### to check user with id-1

http://43.204.228.245:5000/users/2  ### to check user with id-2   etcccc



### Delete method ### ----> To Delete user 

curl -X DELETE http://localhost:5000/users/delete/1


ps aux | grep app.py   # to check running or not python background


pkill -f app.py    # to kill process 


## To run continuously  background without stop

nohup python3 app.py > flask.log 2>&1 &


### How It Works

nohup prevents the process from stopping when you log out.
& runs it in the background.
> flask.log 2>&1 redirects output (stdout & stderr) to flask.log.






