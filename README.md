# foodgram-project
## Описание
«Продуктовый помощник» (Дипломный Проект Яндекс.Практикум)
Проект - сайт Foodgram, «Продуктовый помощник», представляющий онлайн-сервис и API для него. В рамках сервиса пользователи могут:
создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в txt формате. Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx

В ходе реализации проекта были использованы:
1. бэкенд проекта на Django REST Framework (реализовано API по готовой спецификации)
2. созданы Dockerfile для контейнера бэкенда
3. создана конфигурация сервера nginx
4. созданы конфигурации для запуска docker контейнеров для базы данных (PostgreSQL),
для HTTP-сервера nginx, для фронтенда и бэкенда (файл docker-compose)

## Сайт
### Проект развернут в докер контейнере
```
backend - образ бэка проекта
frontend - образ фронта проекта
postgres - образ базы данных PostgreSQL 
nginx - образ web сервера nginx
```
Развернутый сайт доступен по ссылке:
[http://foodgramx.myftp.org/](http://foodgramx.myftp.org/)
```
  user: admin
  password: 112211
  email: xx@xx.xx
```
### Примеры запросов:

+ POST http://localhost:8000/api/users/ - регистрация
+ POST http://localhost:8000/api/auth/token/login - создание токена
+ GET http://localhost:8000/api/users/ - Просмотр информации о пользователях

+ POST http://localhost:8000/api/users/set_password/ - Изменение пароля
+ GET http://localhost:8000/api/users/4/subscribe/ - Подписаться на пользователя
+ DEL http://localhost:8000/api/users/4/subscribe/ - Отписаться от пользователя

+ POST http://localhost:8000/api/recipes/ - Создать рецепт
+ GET http://localhost:8000/api/recipes/ - Получить рецепты
+ GET http://localhost:8000/api/recipes/<id>/ - Получить рецепт по id
+ DEL http://localhost:8000/api/recipes/<id>/ - Удалить рецепт по id

+ GET http://localhost:8000/api/recipes/<id>/favorite/ - Добавить рецепт в избранное
+ DEL http://localhost:8000/api/recipes/<id>/favorite/ - Удалить рецепт из избранного

+ GET http://localhost:8000/api/users/<id>/subscribe/ - Подписаться на пользователя
+ DEL http://localhost:8000/api/users/<id>/subscribe/ - Отписаться от пользователя

+ GET http://localhost:8000/api/ingredients/ - Получить список всех ингредиентов

+ GET http://localhost:8000/api/tags/ - Получить список всех тегов

+ GET http://localhost:8000/api/recipes/<id>/shopping_cart/ - Добавить рецепт в корзину
+ DEL http://localhost:8000/api/recipes/<id>/shopping_cart/ - Удалить рецепт из корзины
  
![example workflow](https://github.com/xrito/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
