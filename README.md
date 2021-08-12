# GEO rest api
*Contanerized Django RestApi*
<br></br>
## Deployment, dependencies
```
git clone https://github.com/Lisciowsky/geo-api && cd geo-api
cp .env.example .env
docker-compose up --build
docker-compose run web python manage migrate
docker-compose run web python manage createsuperuser
```

## Documentation
**geo_collection.json** and **geo_environment.json** provided as a api documentation