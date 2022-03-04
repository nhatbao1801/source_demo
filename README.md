[api.hspaces.net](https://hspaces.net)

## Make sure you're at the folder where contains `docker-compose.yml` and `docker-compose.prod.yml`

**If you haven't built the images yet. Run the following command**

`[sudo] docker-compose -f docker-compose.yml up -d --build` --> [http://localhost:8080](http://localhost:8080)

_Above command will build and start container in background_

**Run docker at local development when you already have built images**

`[sudo] docker-compose -f docker-compose.yml up -d` --> [http://localhost:8080](http://localhost:8080)

**Check how many docker services are running**

`[sudo] docker-compose top`

**Stop all docker services which defining in `docker-compose.yml` file at once**

`[sudo] docker-compose -f docker-compose.yml down`

**Stop all docker services at once and remove all relevant volumes [be careful with data lossing]**

`[sudo] docker-compose -f docker-compose.yml down -v`

**Run command in the container at production stage for static files, migrations and so on**

`[sudo] docker-compose -f docker-compose.prod.yml exec webapp (command)`

