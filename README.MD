
## Questions API
Тестовое задание Bewise.ai

### Требования
   - Установлены Docker, Docker-Compose

### Запуск
1) Склонировать репозиторий
2) Скопировать файл ./env_template в ./.env
3) В .env, при необходимости, изменить параметры (порты и т.д.)
4) Выполнить в консоли из корня проекта:

   ```Shell
   docker compose build
   ```
   ```Shell
   docker compose up -d
   ```
   или
   ```Shell
   docker-compose build
   ```
   ```Shell
   docker-compose up -d
   ```
### Документация
   - Доступна после запуска по http://localhost:8000/docs
   - Эндпоинт http://localhost:8000/questions/, принимает POST запрос с телом вида: {"questions_num": 0}
   - curl пример:
   ```Shell
   curl -X 'POST' \
  'http://127.0.0.1:8000/questions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"questions_num": 0}'
   ```