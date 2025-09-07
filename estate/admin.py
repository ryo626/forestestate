from django.contrib import admin
from .models import Property #models.pyからクラスを読み込む

admin.site.register(Property) #管理画面に表示するよう登録
