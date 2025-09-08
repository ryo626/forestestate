from django.db import models


class Property(models.Model):

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 物件名
    price = models.IntegerField()  # 価格
    address = models.CharField(max_length=200)  # 住所
    description = models.TextField(blank=True)  # 詳細説明
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時(自動)

    def __str__(self):
        return self.title  # 管理画面などでタイトル表示されるように
