from django.shortcuts import render
from myblog.models import Siteinfo, Classes, Userinfo

# Create your views here.
def index(request):
    # 在这里写入业务逻辑和读取数据库
    print("开始读取数据")
    # siteinfo = Siteinfo.objects.all()   # 获取Siteinfo下的所有数据并赋值给一个变量
    # 站点基础信息
    siteinfo = Siteinfo.objects.all()[0]
    # 菜单分类
    # classes = Classes.objects.get(id=1)
    classes = Classes.objects.all()
    # 全部用户
    userlist = Userinfo.objects.all()
    print(siteinfo.title)
    print(siteinfo.logo)
    data = {
        "siteinfo": siteinfo,
        "classes": classes,
        "userlist": userlist
    }
    return render(request, 'index.html', data)
