from django.db import models
from django.contrib.auth.models import User
import os


class Property(models.Model):

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 物件名
    price = models.IntegerField()  # 価格
    address = models.CharField(max_length=200)  # 住所
    description = models.TextField(blank=True)  # 詳細説明
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時(自動)
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images", blank=True, null=True)

    # モデルインスタンス削除すると画像データが削除される
    # def delete(self, *args, **kwargs):
    #     if self.image and os.path.isfile(self.image.path):
    #         os.remove(self.image.path)
    #     super().delete(*args, **kwargs)

    def __str__(self):
        return self.title  # 管理画面などでタイトル表示されるように
