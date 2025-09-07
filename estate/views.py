from django.shortcuts import render, get_object_or_404
from .models import Property


def property_list(request):
    # チェックボックスの状態を取得(GETパラメータから)
    nature = request.GET.get("nature")
    station = request.GET.get("station")
    remote = request.GET.get("remote")

    # 物件一覧ページから表示するビュー関数
    # 1)DBからPropertyを全部取得
    # 2)テンプレートに渡してHTML生成

    properties = Property.objects.all().order_by("-created_at")  # 新しい順に並べ替え

    # 検索条件に応じてフィルタリング
    if nature:
        properties = properties.filter(description__icontains="自然")
    if station:
        properties = properties.filter(description__icontains="駅")
    if remote:
        properties = properties.filter(description__icontains="リモート")

    # チェック状態もテンプレートに渡す
    context = {
        "properties": properties,
        "nature": nature,
        "station": station,
        "remote": remote,
    }

    # テンプレートに渡すデータの箱
    return render(request, "estate/property_list.html", context)


def property_detail(request, pk):  # 引数pkは"propertyes/<int:pk>/"のpkに渡されるid
    # 1件の物件だけを取得(存在しなければ404)
    property = get_object_or_404(Property, pk=pk)
    # get_object_pr_404()は存在しないIDでもエラーにならず404に飛ぶ関数
    # 第一引数にModel,第二引数にidで存在を確かめ存在すればModelのオブジェクトを返す

    return render(request, "estate/property_detail.html", {"property": property})
    # 任意のid一件のデータをpropertyという名前に渡して表示させる{"渡す任意の名前":18行目のproperty}
