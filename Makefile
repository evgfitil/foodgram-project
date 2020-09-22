run:
	docker-compose up -d
load_data:
	docker exec -ti foodgram-web ./manage.py loaddata dump.json
pull:
	docker pull evgfitil/foodgram