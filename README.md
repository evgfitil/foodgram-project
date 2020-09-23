# foodgram-project
foodgram-project
![example workflow name](https://github.com/evgfitil/foodgram-project/workflows/Foodgram-CI/badge.svg)

***Foodgram*** - сайт рецептов - продуктовый помощник, позволяющий просматривать и создавать рецепты, 
добавлять их в избранное, подписываться на авторов рецептов, формировать список покупок
с ингредиентами для приготовления понравившихся блюд.

Демо сайт доступен по этой ссылке https://ea-praktikum.ml

### Запуск проекта с использованием Docker

  Клонируйте репозиторий или скопируйте следующие файлы и папки:
   ```
    nginx/
    docker-compose.yaml
    .env-example
    .db.env-example
   ```
  1. При необходимости измените файлы `.env.local-example`, `.db.env-example` 
  и переименуйте их в `.env` и `.db.env`
  2. Для запуска проекта выполните команду: `make run` или `docker-compose up -d`
     После успешного запуска, проект доступен по адресу http://localhost:80
  3. При первом запуске необходимо применить миграции: `make migrate` или `docker exec -ti foodgram-web ./manage.py migrate`
  4. Для загрузки тестовых данных выполните команду: `make load_data` или `docker exec -ti foodgram-web ./manage.py loaddata dump.json`
  5. Для получения актуальной версии образа проекта выполните: `make pull` или `docker pull evgfitil/foodgram`
  