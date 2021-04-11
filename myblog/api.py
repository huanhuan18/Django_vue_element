from rest_framework.decorators import api_view
from rest_framework.response import Response
from myblog.models import Classes, Userinfo
from myblog.toJson import Classes_data, Userinfo_data

@api_view(['GET', 'POST'])
def api_test(request):
    classes = Classes.objects.all()
    # classes_data = Classes_data(classes, many=True)
    # userlist = Userinfo.objects.all()
    # userlist_data = Userinfo_data(userlist, many=True)
    #
    # data = {
    #     'classes': classes_data.data,
    #     'userlist': userlist_data.data
    # }

    data = {
        'classes':[]
    }
    for c in classes:
        data_item = {
            'id': c.id,
            'text': c.text,
            'userlist': []
        }
        userlist = c.userinfo_classes.all()   # 在models.py中写的related_name，反向查询
        for user in userlist:
            user_data = {
                'id': user.id,
                'nickName': user.nickName,
                'headImg': str(user.headImg)   # 图片路径转成字符串
            }
            data_item['userlist'].append(user_data)
        data['classes'].append(data_item)
    return Response({'data':data})
