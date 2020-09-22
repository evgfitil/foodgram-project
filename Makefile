run:
	docker-compose up -d
migrate:
	docker exec -ti foodgram-web ./manage.py migrate --no-input
load_data:
	docker exec -ti foodgram-web ./manage.py loaddata dump.json
pull:
	docker pull evgfitil/foodgram