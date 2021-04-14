## 安装
### 1.创建虚拟环境python -m venv xxx
### 2.进入虚拟环境中cd Script -->activate.bat
### 3.安装Django  pip install django
### 4.新建项目 django-admin startproject xxx(mysite)
###5.新建app python manage.py startapp xxx(myblog)
### 6.数据库迁移 
    python manage.py makemigrations //具体在某个应用下更新可在后面加上app名称,如myblog
    python manage.py migrate
### 7.运行Django python manage.py 
### 8.settings配置：
	1>将新建的app添加到mysite.settings中的INSTALLED_APPS列表中(ALLOWED_HOSTS表示允许的其他ip访问)
	2>MIDDLEWARE: 中间件，包括csrf跨站、登录验证等，刚开始并不用动
	3>TEMPLATES: 模板配置，在app项目下新建templates文件夹，然后在DIRS里配置os.path.join(BASE_DIR, 'templates').replace('\\', '/')
	4>STATIC_URL: 静态文件
	5>MIDEA_URL: 媒体目录的路由，自己添加，一般是用户上传图片文件等，配置为MEDIA_URL = '/upload/'
	6>MIDEA_ROOT: 媒体目录 MEDIA_ROOT = BASE_DIR / 'upload'，然后在项目下新建upload和在app项目下新建static文件夹，在urls.py中写入
		from django.conf import settings
		from django.conf.urls.static import static
		urlpatterns = [path('admin', admin.site.urls),]
						+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
						+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
### django后端部分
### 9.MTV模式，django的专属模式M：model(数据库)，T：template(模板-html), V: view(视图层，views.py)
	例：第一个页面，在urls.py中写入一个path
	from myblog import views
	path('index/', views.index)
	然后在views.py中新建index函数
	def index(request):
		//在这里写入业务逻辑和读取数据库
	return render(request, 'index.html'),然后在templates目录下新建index.html里面写入内容，刷新index即可看到我们自己写的网页。
### 10.创建第一个数据表
	在app项目的models.py中写入模型。如：
		class Siteinfo(models.Model):
			title = models.CharField(null=True, blank=True, max_length=50)
			logo = models.ImageField(upload_to='logo/', null=True, blank=True) //upload_to就是上传到设置的MEDIA_ROOT路径
			def __int__(self):
			"""展现的一个形式"""
				return self.id
### 11.每次修改完模型之后都要执行第6步的数据库迁移
### 12.将创建的模型Siteinfo导入到一个可视的地方
	在app项目下的admin.py中写入
	from myblog.models import Siteinfo
	//admin.site.register(Siteinfo)  //Django3注册可能会报错
	//所以用装饰器注册
	@admin.register(Siteinfo)
	class SiteinfoAdmin(admin.ModelAdmin):
		pass
### 13.创建超级管理员进入后台管理
	1>python manage.py createsuperuser,密码太简单可能会报错，中英结合8位(admin12345)
	2>http://127.0.0.1:8000/admin进入输入账号密码
	3>点击Siteinfo表-->Add-->输入title，上传图片，可看到图片已经上传到upload/logo文件夹内(可理解第10步和第8步)
### 14.配置MySQL数据库
	DATABASES = {
		'mysql': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'gaofei',
			'USER': 'root',
			'PASSWORD': 'gaofei12345',
			'HOST': '127.0.0.1',
			'PORT': '3306'
		}
	}
	1>pip install pymysql,然后在项目的__init__.py文件下导入
		import pymysql
		pymysql.install_as_MySQLdb()
	2>在数据库中新建数据库myblog(navicat右键连接名gaofei,新建数据库，选择utf8和utf8_general_ci)
	3>把之前的数据合并到数据库myblog中，python manage.py migrate --database mysql
	4>在settings.py中把sqlite3数据库注释，将mysql改为default
	5>后台重新创建超级管理员进入Siteinfo添加一条信息，即可在数据库中看到
	6>如果想将已有的数据迁移，不需要Django来完成，就要去了解sql文件的转换
### 15.从views视图层读取数据到HTML模板（传统的MTV模式，基本都要后端去完成，后续不会用这种方式，而是用前后端分离代替）
	1>在views.py中导入表
	from myblog.models import Siteinfo
	def index(request):
		siteinfo = Siteinfo.objects.all()[0] // 获取Siteinfo下的第一条数据并赋值给一个变量
		print(siteinfo.title)
		print(siteinfo.logo)
		data = {
        "siteinfo": siteinfo
		}
		return render(request, 'index.html', data)  //将数据装载成字典，传给html
	2>在index.html中用{{siteinfo.title}}获取数据
### 16.手写HTML样式
	样式保存在static/css/mystyle.css样式内
### 17.制作两张表，然后注册到admin中可视化，添加数据
	1>课程分类Classes
	2>用户Userinfo  
	//课程是1，用户是多，所以用户中用外键，belong=models.ForeignKey(Classes, on_delete=models.SET_NULL, related_name="userinfo_classes", null=True, blank=True)
	//on_delete是当删除上级的Classes表时，当前表的field行为,related_name是查询时的展现形式，写成字符串，个人习惯多的在前，少的在后
### 18.Django模板的for循环、if条件
	//如果有用户，把用户循环装载进来，否则显示没有用户
	{% if userlist %}
	  {% for user in userlist %}
		<div class="user">
			<img src="/static/admin.jpg" alt="">
			<p>{{ user.nickName }}</p>
		</div>
	  {% endfor %}
    {% else %}
		<p>没有用户</p>
    {% endif %}
### 19.Django的模板继承
	在index.html中使用a标签连接了/classes
	1>新建一个classes.html中写入{% extends "index.html" %}   这样就继承了index.html模板
	2>在views.py中新建函数classes，获取数据并发送给classes.html
### 20.路由传参
	在index.html中的a标签herf写上<a href="/classes/?id={{ class.id }}">
	在views.py中classes函数内写入choosed_id = request.GET['id']鼠标悬浮即可看到每一个标签对应的id
### 21.认识json与错误处理
	在views.py中导入from django.http import HttpResponse, JsonResponse     from django.shortcuts import redirect
	1>return HttpResponse('<h1>无结果</h1>')  //发送字符串
	2>return JsonResponse(data)  //发送json形式
	3>return redirect('/')  //重定向到首页
	try:
		choosed_id = request.GET['id']
		print(choosed_id)
		choosed = Classes.objects.filter(id=choosed_id)
    except:
        return redirect("/")

    if choosed:
        userlist = Userinfo.objects.filter(belong=choosed[0]) //因为filter获取的一定是列表，所以加位标
    else:
        userlist = []
### 22.安装django-rest-framework（api视图）
	1>pip install djangorestframework
	2>'rest_framework' 放到INSTALLED_APPS中
	3>在myblog中新建api.py,在这里面写入一些视图函数
		from rest_framework.decorators import api_view
		from rest_framework.response import Response
		@api_view(['GET', 'POST'])
		def api_test(request):
			if request.method == "POST":
				return Response('post')
			return Response('ok')
	4>在urls.py中写入路由path('api/', api.api_test)
### 23.数据的序列化
	1>在myblog中新建toJson.py,在这里面写入一些序列化的东西
		from rest_framework import serializers
		from myblog.models import Classes

		class Classes_data(serializers.ModelSerializer):
			class Meta:
				depth = 1
				model = Classes
				fields = '__all__'
	2>在api.py中写视图函数
		@api_view(['GET', 'POST'])
		def api_test(request):
			classes = Classes.objects.all()
			classes_data = Classes_data(classes, many=True)
			userlist = Userinfo.objects.all()
			userlist_data = Userinfo_data(userlist, many=True)   //有多条数据的时候一定要加many=True,否则会报错

			data = {
				'classes': classes_data.data,
				'userlist': userlist_data.data
			}
			return Response({'data':data})
### 24.python字典的数据整理
	因为23中的数据有重复，所以一般用手写数据
	@api_view(['GET', 'POST'])
	def api_test(request):
		classes = Classes.objects.all()
		data = {
			'classes':[]
		}
		for c in classes:
			data_item = {
				'id': c.id,
				'text': c.text,
				'userlist': []
			}
			userlist = c.userinfo_classes.all()   //在models.py中写的related_name，反向查询
			for user in userlist:
				user_data = {
					'id': user.id,
					'nickName': user.nickName,
					'headImg': str(user.headImg)   //图片路径转成字符串
				}
				data_item['userlist'].append(user_data)
			data['classes'].append(data_item)
		return Response({'data':data})
###认识Ajax与Vue
	1>在head标签内添加js
	<script src="/static/js/vue.js"></script>
    <script src="/static/js/axios.js"></script>
	2>在script标签内新建一个vue实例（仍在django内，暂未实现前后端分离）
	<script>
    new Vue({
        delimiters: ['[[',']]'] ,   //修改默认双大括号渲染数据为双中括号
        el: '#home',
        data: {
            choosed:1,    //打开页面默认选择的是id为1
            classes:[]
        },
        mounted() {
            this.getData()
        },
        methods: {
          getData(){
              axios({
                  url:'/api',
                  type:'json',
                  method:'get'
              }).then((res)=>{
                  console.log(res.data.data.classes)
                  this.classes = res.data.data.classes
                  }
          )},
		  chooseClass(id){
			 console.log(id)
			 this.choosed=id
		  }
        },
    })
	</script>
	3>标签判断和循环
	<div v-if="item.id==choosed" v-for="item in classes" class="item" style="background:#777777;color: #ffffff">
	<div v-if="item.userlist.length>0" v-for="user in item.userlist" class="user">
	<div v-on:click="chooseClass(item.id)" v-else class="item">
###前后端分离好处：		
能够让用户在整个交互过程中，不会让用户一直等待，即便后端数据没有过来，至少用户打开了页面，如果说后端发生错误，例如用户对api接口触发了一些奇怪的错误，我们可以通过这次访问单纯的抛出成功或者不成功两种选项让用户去选，前后端分离能够让我们在开发和维护的过程中更方便
	后端所要做的就是将数据整理成最简洁的方式通过api的接口发送到前端，前端所需要做的就是一次性把这些数据全部接收，如getData函数通过ajax把数据全部拿过来，至于页面中的交互逻辑应该是交给vue.js去管理视图交互
