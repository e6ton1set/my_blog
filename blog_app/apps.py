from django.apps import AppConfig


class BlogAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # конфигурация для id, который мигрируется в БД, 64 bit integer
    name = 'blog_app'
