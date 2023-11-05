# Публикация комиксов

Автоматическая публикация комиксов автора xkcd ежедневно в ваше сообщество Вконтакте.
Случайный комикс будет публиковаться в одно и то же время вместе с описанием, 
написанным зарубежным автором.

### Как установить

1. Установить Python3 с [официального сайта](https://www.python.org/downloads/).

2. Установить зависимости (сторонние библиотеки, необходимые для корректной работы 
   кода). В случае конфликта с Python2 необходимо использовать `pip3`:
   ```sh
   pip install -r requirements.txt
   ```
3. Необходимо создать [приложение Вконтакте](https://vk.com/apps?act=manage). 
   В качестве типа приложения следует указать `standalone` — это подходящий тип 
   для приложений, которые просто запускаются на компьютере.
   
4. Получите ключ доступа пользователя. Он нужен для того, чтобы ваше приложение 
   имело доступ к вашему аккаунту и могло публиковать сообщения в группах. Вам 
   потребуются следующие права: `photos`, `groups`, `wall` и `offline`. Ключ можно 
   получить по [ссылке](https://vk.com/dev/implicit_flow_user).
   
5. В папке проекта создать файл `.env`, в него записать полученный файл в формате 
   `ACCESS_TOKEN="полученный_токен"`. 
   
6. В созданный в 5 шаге файл добавить вторую строку: 
   `GROUP_ID="id_сообщества"`. id сообщества, в которое вы будете выкладывать 
   комиксы, можно найти [здесь](https://regvk.com/id/).
   
7. Запустить файл `main.py`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).