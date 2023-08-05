# После установки

Добавить приложения в список **INSTALLED_APPS** в settings.py
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_swagger',
    'sso_server'
]
```

Добавить в settings.py переменную, содержащую корневой домен для установки cookies

```python
DOMAIN = '.local'
```

Добавить в settings.py следующую строку:
```python
REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
```

Выполнить миграции:
```shell
python manage.py migrate
```

**Добавить в settings.py в middleware:**
```'sso_server.middleware.UserCookieMiddleWare'```

Добавить в urls.py следующий маршрут:

```python
urlpatterns = [
    ...
    path('sso/', include('sso_server.urls'))
]
```