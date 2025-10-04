from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ["title", "description", "address", "price", 'image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        #チェックが入ってれば画像削除
        if self.cleaned_data.get('delete_image'):
            if instance.image:
                instance.image.delete(save=False)
                instance.image = None
        if commit:
            instance.save()
        return instance

    # 　フィールドごとのバリデーション
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("価格は0以上で入力して下さい")
        return price

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if title and len(title) > 30:
            raise forms.ValidationError("タイトルは30文字以内で入力してください")
        return title
