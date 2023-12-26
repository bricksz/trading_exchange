## Running the backend locally
Run environment in CLI <br>
`env\scripts\activate`
<br><br>
Both Trade and Exchange worker must be running <br>
`python match_engine/setup_exchange.py` <br>
`python match_engine/setup_trade.py` 
<br><br>
Run backend locally <br>
`python manage.py runserver`
<br><br>
Run dummy trades on bash <br>
`cd match_engine` <br>
`./sh_sandbox.sh`

## Setting up Javascript & React & Babel & modules
NodeJS and React must be installed. CLI check `npm` <br>
<br>
Django `frontend` directory must contain `src` and `static` <br>
<br>
On terminal, activate environment and then run the following: <br>
```
npm init -y
npm i webpack webpack-cli --save-dev
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
npm i react react-dom --save-dev
npm install @mui/material @emotion/react @emotion/styled
npm install @babel/plugin-proposal-class-properties
npm install react-router-dom
npm install @mui/icons-material
```

Also create `babel.config.json` and `webpack.config.js` in the same directory. <br>
<br>
In `package.json` replace scripts with <br>
```js
  "scripts": {
    "dev": "webpack --mode development --watch",
    "build": "webpack --mode production"
  },
```

## Setup up Ubuntu Server

 
## Setup Postgres 12
server local address: `127.0.0.1/32` 
<br><br>
authentication settings<br>
`sudo nano /etc/postgresql/12/main/pg_hba.conf` 
<br><br>
config settings <br>
`sudo nano /etc/postgresql/12/main/postgresql.conf`
<br><br>

```SQL
select rolname, rolpassword from pg_authid;
```

##### pgBouncer
Install using apt: <br>
`sudo apt install pgbouncer -y` 
<br><br>
`sudo nano /etc/pgbouncer/pgbouncer.ini`
<br><br>
`sudo nano /etc/pgbouncer/userlist.txt`
<br><br>
go to pg_hba settings to add address <br>
`sudo nano /etc/postgresql/12/main/pg_hba.conf`
<br><br>
reload pgbouncer <br>
`sudo systemctl reload pgbouncer.service`
<br><br>
On compute engine grant all permission access to pgbouncer folder
`sudo chmod a+rwx etc/pgbouncer/`
<br><br>
Then switch user to postgres and initialize pgbouncer
`pgbouncer -d etc/pgbouncer/pgbouncer.ini`
<br><br>
## Setup RabbitMQ
Ubuntu prerequisites <br>
`sudo apt-get install curl gnupg apt-transport-https -y`
<br><br>
Team RabbitMQ's main signing key <br>
`curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null`
<br><br>
Cloudsmith: modern Erlang repository <br>
`curl -1sLf https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/gpg.E495BB49CC4BBE5B.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.cloudsmith.rabbitmq.E495BB49CC4BBE5B.gpg > /dev/null`
<br><br>
Cloudsmith: RabbitMQ repository <br>
`curl -1sLf https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/gpg.9F4587F226208342.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.cloudsmith.rabbitmq.9F4587F226208342.gpg > /dev/null`
<br><br>
Add apt repositories maintained by Team RabbitMQ
```
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases
##
deb [signed-by=/usr/share/keyrings/io.cloudsmith.rabbitmq.E495BB49CC4BBE5B.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/io.cloudsmith.rabbitmq.E495BB49CC4BBE5B.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/deb/ubuntu focal main

## Provides RabbitMQ
##
deb [signed-by=/usr/share/keyrings/io.cloudsmith.rabbitmq.9F4587F226208342.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/deb/ubuntu focal main
deb-src [signed-by=/usr/share/keyrings/io.cloudsmith.rabbitmq.9F4587F226208342.gpg] https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-server/deb/ubuntu focal main
EOF
```

Update package indices <br>
`sudo apt-get update -y`
<br><br>
Install Erlang packages
```
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
```

Install rabbitmq-server and its dependencies <br> 
`sudo apt-get install rabbitmq-server -y --fix-missing`


##### RabbitMQ User Interface
GCE external connection must be open with firewall settings, then go to url address <br> 
`http://[EXTERNAL IP]:15672` <br>
```
<EXTERNAL IP>:15672
user: master_user
pass: abc123
```
For local usage <br>

```
http://localhost:15672
user: guest
pass: guest
```

##### RabbitMQ commands
open rabbitmq command prompt <br>
`rabbitmq-plugins enable rabbitmq_management`
<br><br>
check status <br>
`rabbitmq-diagnostics status`
<br><br>
list of queues, in rabbitmq command prompt <br>
`sudo rabbitmqctl list_queues`
<br><br>
if on windows <br>
`rabbitmqctl.bat list_queues`
<br><br>
adds a new user and password <br>
`sudo rabbitmqctl add_user master_user abc123`
<br><br>
grants user administrator <br>
`sudo rabbitmqctl set_user_tags master_user administrator`
<br><br>
sets permissions for the user <br>
`sudo rabbitmqctl set_permissions -p / master_user ".*" ".*" ".*"`

##### RabbitMQ Tips
```python
# once the consumer connection is closed, the queue should be deleted. There's an exclusive flag for that:
channel.queue_declare(queue='', exclusive=True)
```
