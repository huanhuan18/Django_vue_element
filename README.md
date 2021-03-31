## 安装
### 1.创建虚拟环境python -m venv xxx
### 2.进入虚拟环境中cd Script -->activate.bat
### 3.安装Django  pip install django
### 4.新建项目 django-admin startproject xxx(mysite)
### 5.新建app python manage.py startapp xxx(myblog)
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
	6>MIDEA_ROOT: 媒体目录 MEDIA_ROOT = os.path.join(BASE_DIR, 'upload').replace('\\', '/')，然后在项目下新建upload和在app项目下新建static文件夹，在urls.py中写入
		from django.conf import settings
		from django.conf.urls.static import static
		urlpatterns = [path('admin', admin.site.urls),]
						+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
						+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
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