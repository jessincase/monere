# Monere
A discussion forum with chat based threads with the backend built in Python and Django, and front end in ReactJS.  

# To Start
## Backend
`redis-server /usr/local/etc/redis.conf`

`daphne config.asgi:channel_layer --port 8888`

`python manage.py runworker`

`python manage.py runserver`

## Frontend
`npm run react-dev`

`npm run server-dev`

Then navigate to http://localhost:8080/


# Acknowledgements 
- https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
- https://medium.com/@Preda/getting-started-on-building-a-personal-website-with-react-b44ee93b1710

