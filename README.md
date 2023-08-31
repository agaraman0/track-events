# track-events

### Steps To Run

```commandline
$ git clone git@github.com:agaraman0/track-events.git

$ cd track-events
```

Before running this make sure you do not have any existing migration in Repo named migrations/

```commandline
$ docker-compose up -d --build

$ docker ps # you should be able to see 2 docker images running one as application server and another as db server
```

Our Application is successfully up and running to test it run localhost:5000 in Browser

Now set up db 
```commandline
$ docker exec -it <application_server_contianer_name> bash

root@ba6d63/usr/src/app# python manage.py db init

root@ba6d63/usr/src/app# python manage.py db migrate

root@ba6d63/usr/src/app# python manage.py db upgrade
```

Now use Postman collection all endpoints and workflows



FE screenshot (under development)
<img width="1432" alt="Screenshot 2023-08-31 at 8 04 03 AM" src="https://github.com/agaraman0/track-events/assets/29687692/6cb2a691-1b51-4844-925b-4cfb87ae0a38">
