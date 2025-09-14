from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Property
from .forms import PropertyForm

# 物件一覧機能


def property_list(request):
    # クエリ用のキーワードと、画面表示用のラベルをセットで定義
    checkboxes = {
        "nature": ("自然", "自然豊か"),
        "station": ("駅", "駅近"),
        "remote": ("リモート", "リモート可"),
    }

    # テンプレートに渡す状態をlist型にする
    search_conditions = []
    # DBからPropertyデータを全件取得、登録日時が最近のものから(降順)にする
    properties = Property.objects.all().order_by("-created_at")
    applied = False

    # checkboxesのkeyとvalueを順番に取り出す
    for key, (query_text, label) in checkboxes.items():
        # GETリクエストformからnameからvalueが取得されてるか確認
        if request.GET.get(key):
            # filterメソッドで全件取得したデータからquery_textのキーワードに絞り込む
            properties = properties.filter(description__icontains=query_text)
            # list型のsearch_conditionsにlabelを格納
            search_conditions.append(label)
            applied = True

    q = request.GET.get("q")
    if q:
        properties = properties.filter(Q(title__icontains=q))
        applied = True

    # GET送信がなしandキーワードとチェックボックスの条件が一つもなければ強制的にpropertiesが空になる
    if request.GET and not applied:
        properties = Property.objects.none()

    # DBからPropertyを取得したデータをcontextに格納
    context = {
        "properties": properties,
        "search_conditions": search_conditions,
    }

    # テンプレートに渡すデータの箱
    return render(request, "estate/property_list.html", context)


# 物件詳細機能


def property_detail(request, pk):  # 引数pkは"propertyes/<int:pk>/"のpkに渡されるid
    # 1件の物件だけを取得(存在しなければ404)
    property = get_object_or_404(Property, pk=pk)
    # get_object_pr_404()は存在しないIDでもエラーにならず404に飛ぶ関数
    # 第一引数にModel,第二引数にidで存在を確かめ存在すればModelのオブジェクトを返す

    return render(request, "estate/property_detail.html", {"property": property})
    # 任意のid一件のデータをpropertyという名前に渡して表示させる{"渡す任意の名前":18行目のproperty}


# ユーザー物件登録機能
def property_create(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("property_list")
    else:
        form = PropertyForm()

    return render(request, "estate/property_form.html", {"form": form})


# ユーザー更新機能
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect("property_list")

    else:
        form = PropertyForm(instance=property_obj)

    return render(request, "estate/property_form.html", {"form": form})


# ユーザー削除機能
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        property_obj.delete()
        return redirect("property_list")
    return render(request, "estate/property_delete.html", {"property": property_obj})
