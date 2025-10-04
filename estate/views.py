from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Property
from .forms import PropertyForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm

# 物件一覧アプリ


# ユーザー登録機能
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ユーザー作成
            return redirect("login")  # 登録したらログインページに飛ばす
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# 物件一覧表示
def property_list(request):

    # DBからPropertyデータを全件取得、登録日時が最近のものから(降順)にする
    properties = Property.objects.all().order_by("-created_at")

    # クエリ用のキーワードと、画面表示用のラベルをセットで定義
    checkboxes = {
        "nature": ("自然", "自然豊か"),
        "station": ("駅", "駅近"),
        "remote": ("リモート", "リモート可"),
    }

    # テンプレートに渡す状態をlist型にする
    search_conditions = []

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

    # 　フリーワード検索
    q = request.GET.get("q")
    if q:
        properties = properties.filter(Q(title__icontains=q))
        applied = True

    # 価格の範囲検索
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    if price_min:
        properties = properties.filter(price__gte=price_min)
        applied = True

    if price_max:
        properties = properties.filter(price__lte=price_max)
        applied = True

    # GET送信データがあるかつキーワードとチェックボックスの条件が一つもなければ強制的にpropertiesが空になる
    if request.GET and not applied and "page" not in request.GET:
        properties = Property.objects.none()

    # ページネーション機能
    # 1ページ2件に区切る
    paginator = Paginator(properties, 10)

    # 現在のページ番号をGETパラメータから取得(例　?page=2)
    page_number = request.GET.get("page")

    # ページオブジェクトを取得(不正な番号でも安全に処理される)
    page_obj = paginator.get_page(page_number)

    # DBからPropertyを取得したデータをcontextに格納
    context = {
        "page_obj": page_obj,
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
@login_required
def property_create(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect("property_list")
    else:
        form = PropertyForm()

    return render(request, "estate/property_form.html", {"form": form})


# ユーザー更新機能
@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect("property_list")

    else:
        form = PropertyForm(instance=property_obj)

    return render(request, "estate/property_form.html", {"form": form,"property": property_obj})


# ユーザー削除機能
@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        property_obj.delete()
        return redirect("property_list")
    return render(request, "estate/property_delete.html", {"property": property_obj})
