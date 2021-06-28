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
### 25.认识Ajax与Vue
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
### 前后端分离好处：
	1>	能够让用户在整个交互过程中，不会让用户一直等待，即便后端数据没有过来，至少用户打开了页面，如果说后端发生错误，例如用户对api接口触发了一些奇怪的错误，我们可以通过这次访问单纯的抛出成功或者不成功两种选项让用户去选，前后端分离能够让我们在开发和维护的过程中更方便

	2>后端所要做的就是将数据整理成最简洁的方式通过api的接口发送到前端，前端所需要做的就是一次性把这些数据全部接收，如getData函数通过ajax把数据全部拿过来，至于页面中的交互逻辑应该是交给vue.js去管理视图交互
### 26.vuejs数据绑定的方法
	1.第一种绑定：
	<div v-if="onOff">    //v-if和v-show是一样的效果，但是后者可以在dom上看到开发者写的标签
	<button @click="onOffClick">开关</button>   //按钮控制上方的标签展示
	data: {
            onOff: true
        },
	methods: {
            onOffClick() {
                this.onOff = !this.onOff  //每次点击将onOff的值取反
            },
		}
	2.第二种绑定（动态输入）：
	<input v-model="inputText" type="text" name="" id="" style="height: 30px;width: 700px">
    <p>[[inputText]]</p>
	data: {
            inputText: '',
		}
### 27.安装NodeJS环境
	后端环境，可以让JavaScript彻底运行在计算机环境内
	node-v12.8.1
### 28.安装VueCli脚手架
	VueJS官网->生态系统->vuecli
	npm install -g @vue/cli    //如果安装较慢，可以淘宝搜索cnpm用淘宝镜像安装
### 29.VueCli项目的创建
	1>终端输入vue ui
	2>选择目录创建项目，选择预设默认vue2
	3>点击任务->serve->运行
### 30.VueUI管理项目插件
	1>添加vue-router   //路由
### 31.组件基础概念
	每一个.vue文件就是一个组件，下面是单独的一个html文件测试组件
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Document</title>
		<script src="vue.js"></script>
	</head>
	<body>
		<div id="app">
			<!-- <h1>当前开发状态：{{msg}}</h1> -->
			<gf-test></gf-test>
			<gf-test></gf-test>
			<gf-test></gf-test>
			<gf-test></gf-test>
		</div>

	<script>
		// 这个html主要为测试component组件的作用，下面定义的这个组件可以在body中当成一个个标签来使用
		Vue.component('gf-test',{
			data(){
				return{
					msg:"开发完毕"
				}
			},
			template:"<h1>当前开发状态：{{msg}}</h1>",
		})
		
		new Vue({
			el:"#app",
			// data:{
				// msg:"开发完毕"
			// },
			// template:"<h1>当前开发状态：{{msg}}</h1>",
			// methods:{

			// }
		})
	</script>

	</body>
	</html>
### 32.第一个视图组件（一个组件内只能有一个总的div）
	1>把之前在后端写的static下的css和图片资源复制到前端的src下的assets里
	2>在main.js里导入mystyle.css   //import '../src/assets/css/mystyle.css'
	3>因为mystyle.css写的样式id都是home，所以到App.vue把id=app改成home
	4>把Home.vue里的HelloWord组件删掉,将后端的index.html里的home div下的所有内容复制到Home.vue里整理格式
	5>把App.vue里的nav标签的路由和style里的样式删掉
### 33.为各组件分配路由
	1>把Home.vue里的内容剪切到App.vue里
	2>把<router-view/>放到userlist标签内，因为这里面是要切换的地方
	3>在views里新建django.vue
	4>在index.js里设置要展示的路由
	5>在App.vue内添加路由指向标签   //<router-link to="/" style="color:#fff">Django框架</router-link>
	6>继续添加其他的路由组件，重复4和5（手动写，很麻烦，下一节通过ajax请求实现数据绑定）
### 34.认识webpack,安装axios
	1>仪表盘->依赖->开发依赖->输入axios安装
	tips:vuecli的开发使用的是nodeJS下webpack管理方式，通过package.json来告知我们当前整个项目运行在nodeJs环境下需要的是哪些东西
	2>在django.vue里写入一次axios请求（用的是别人的数据）
		<div v-for="item in imglist" :key="item.pk" class="user">  //每次for循环必须绑定一个key
			<img :src="'https://api.dweb.club/'+item.pic" alt="">
			<p>{{item.title}}</p>
		</div>
		
		<script>
		import axios from 'axios'
		export default {
			data() {
				return{
					imglist:[]
				}
			},
			//用户在看到页面之前，最后Vue提供的一次函数操作
			mounted(){
				this.getData()
			},
			methods:{
				getData() {
					axios({
						url:'https://api.dweb.club/dweb-api/get-index-data/',
						type:'json',
						method:'get'
					}).then((res)=>{
						console.log(res)
						this.imglist=res.data.newsdata
					})
				}
			}
		}
		</script>
	3>启动后端python manage.py runserver 127.0.0.1:9000  (用我们自己的数据，因为8000端口被占用了，所以用9000端口)
	4>把url改成http://127.0.0.1:9000/api/
	5>刷新页面会看到CORS报错
### 35.理解cors跨源请求
	两个网站之间的请求，也叫跨域请求，用户访问A网站，但是A网站想用B网站的数据，这时就要在B网站设置一个corsheaders,这样B才能返回一个json数据给A
### 36.django-cors-headers的安装与配置
	1>pip install django-cors-headers
	2>将corsheaders挂载到INSTALL_APP里（放在我们的app上方）
	3>添加中间件(一定要通用组件的上方)
		MIDDLEWARE = [
			'corsheaders.middleware.CorsMiddleware',
			'django.middleware.common.CommonMiddleware',
			]
	4>配置CorsHeaders
		#跨域增加忽略
		CORS_ALLOW_CREDENTILS = True
		CORS_ORIGIN_ALLOW_ALL = True
		CORS_ORIGIN_WHITELIST = (
			'http://127.0.0.1',
		)
		CORS_ALLOW_METHODS = (
			'DELETE',
			'GET',
			'OPTIONS',
			'PATCH',
			'POST',
			'PUT',
			'VIEW',
		)
		CORS_ALLOW_HEADERS = ( 
			'XMLHttpRequest', 
			'X_FILENAME', 
			'accept-encoding', 
			'authorization', 
			'content-type', 
			'dnt', 
			'origin', 
			'user-agent', 
			'x-csrftoken', 
			'x-requested-with', 
			'Pragma'
		)
	5>刷新http://localhost:8080/#/即可看到成功访问到了后端的9000端口api下的数据，至此配置好了后端cors头的设置
### 37.VueCli中的v-for与v-if
	1>在App.vue中写入
	<script>
	import axios from "axios";
	export default {
	  data() {
		return {
		  choosed: 1,
		  menuList: [],
		};
	  },
	  mounted() {
		this.getMenuList();
	  },
	  methods: {
		//获取分类列表
		getMenuList() {
		  console.log("开始获取分类");
		  axios({
			url: "http://127.0.0.1:9000/get-menu-list/",
			type: "json",
			method: "get",
		  }).then((res) => {
			console.log(res);
			this.menuList = res.data;
		  });
		},
		chooseMenu(id) {
		  console.log(id);
		  this.choosed = id;
		},
	  },
	};
	</script>
	2>在后端urls.py中写入新的路由  path('get-menu-list/', api.getMenuList)
	3>在api.py中写入
		@api_view(['GET'])
		def getMenuList(request):
			allClasses = Classes.objects.all()

			//整理数据为json
			data = []
			for c in allClasses:
				//设计单挑数据结构
				data_item = {
					'id':c.id,
					'text':c.text
				}
				data.append(data_item)
			return Response(data)
	4>接下来以组件的形式装载数据，把django.vue中的请求删掉，并改名为UserList.vue，修改路由名称
	5>修改App.vue中的标签内容
		<div class="menu">
          <div v-for="item in menuList" :key="item.id" class="item">
            <div
              v-if="item.id == choosed"
              style="background: #777777; color: #ffffff"
            >
              <router-link to="/" style="color: #fff">{{
                item.text
              }}</router-link>
            </div>
            <div v-else style="" @click="chooseMenu(item.id)">
              <router-link to="/" style="color: #000">{{
                item.text
              }}</router-link>
            </div>
          </div>
        </div>
### 38.vue-router路由传参
	1>通过点击修改文本信息
		<div class="userlist">
          <p>{{choosed_text}}</p>
          <hr />
          <router-view />
        </div>
		data() {
			return {
			  choosed: 1,
			  choosed_text:'Django后端',
			  menuList: [],
			};
	    },
		chooseMenu(id) {
		  console.log(id);
		  this.choosed = id;
		  for (let index = 0; index < this.menuList.length; index++) {
			if (id==this.menuList[index].id) {
			  this.choosed_text=this.menuList[index].text
			}
			
		  }
		},
	2>进行id传参，路由跳转
		在App.vue的getchooseMenu方法内写入 this.$router.push({path:'/',query:{menuId:id}})   //进行id传参跳转
		在UserList.vue里添加监听
		<script>
		import axios from 'axios'
		export default {
			data() {
				return{
					apiurl:'http://127.0.0.1:9000/',
					imglist:[],
					menuId:1
				}
			},
			mounted(){
				this.getUserList(this.menuId)
			},
			watch:{
				$route(to){
					console.log(to.query.menuId)
					this.menuId=to.query.menuId
					this.getUserList(this.menuId)
				}
			},
			methods:{
				//从这里开始后端的请求
				getUserList(id){
					console.log("开始获取用户分类列表"+id)
					axios({
						url:'http://127.0.0.1:9000/get-user-list/',
						type:'json',
						params:{
							id
						},
						method:'get'
					}).then((res)=>{
						console.log(res)
						this.imglist=res.data
					})
				}
			}
		}
		</script>
		//可以看到每次点击都有两次路由跳转，是因为App.vue里的router-link默认执行了本地跳转，将其改为a标签即可
	3>后端添加路由方法
		path('get-user-list/', api.getUserList)
		@api_view(['GET'])
		def getUserList(request):
			menuId = request.GET['id']  //拿到前端传过来的id参数
			print(menuId)   //成功打印即可证明后端能收到前端传递的参数
			menu = Classes.objects.get(id=menuId)
			print(menu)
			userlist = Userinfo.objects.filter(belong=menu)
			print(userlist)
			# 开始整理数据列表
			data = []
			for user in userlist:
				data_item = {
					'id':user.id,
					'headImg':str(user.headImg),
					'nickName':user.nickName
				}
				data.append(data_item)
			return Response(data)
	4>修改标签
		<div id="userlist">
			<div v-for="item in imglist" :key="item.pk" class="user">
				<img :src="apiurl+'upload/'+item.headImg" alt="">
				<p>{{item.nickName}}</p>
			</div>
		</div>
### 40.执行一次POST请求
	1>在App.Vue最上方加入两个button,然后为了美观在mystyle.css中的h1内加入margin-top: 0;
	2>在components中新建LoginBox.vue，写入内容
	3>在App.vue中引入import LoginBox from "../src/components/LoginBox"
		export default {
		  components:{
			LoginBox
		  },
		}
	4>应用标签<LoginBox></LoginBox>
	5>在后端urls.py中写入path('login/', api.toLogin),然后在api.py中新建toLogin方法
	6>在前端LoginBox.vue中导入axios   //导入Qs处理数据，否则数据格式会有问题  import Qs from "qs"   Qs.stringify()
### 41.理解登录安全及流程
	1>验证用户名是否存在：在前端LoginBox.vue中写入
		if (username.length > 0 && password.length > 0) {...}else{alert("用户名或密码不能为空")}
	2>在后端api.py中的toLogin里写入
		from django.contrib.auth.models import User
		//查询用户数据库
		user = User.object.filter(username=username)
		if len(user) > 0:
			print(user)
		else:
			return Response('none')
		return Response('ok')
	3>在前端LoginBox.vue中写入if (res.data=='none') {alert('用户名不存在')}
	4>验证密码是否存在：在后端api.py中写入from django.contrib.auth.hashers import check_password 
		if len(user) > 0:
			user_pwd = user[0].password
			auth_pwd = check_password(password,user_pwd)
			//django里面的密码都是通过哈希算法加密的，这里将传入的密码字符串转为哈希值跟原密码对比
			print(auth_pwd)
			if auth_pwd:
				return Response('ok')
			else:
				return Response('pwderr')
	5>在前端LoginBox.vue中写入
		switch (res.data) {
            case "none":
              alert("用户名不存在");
              break;
            case "pwderr":
              alert("密码错误");
              break;
            default:
              alert("登录成功");
              break;
          }
### 42.Django后端 Token分发   
	//让用户保持登录状态，虽然Token也不安全，但是可以给它设置过期时间
	1>在django的settings.py下的INSTALLED_APP中加入'rest_framework.authtoken',然后合并数据库python manage.py makemigrations,python manage.py migrate
	2>在api.py中导入from rest_framework.authtoken.models import Token
		    if auth_pwd:
				token = Token.objects.update_or_create(user=user[0])
				token = Token.objects.get(user=user[0])
				print(token.key)
				data = {
					'token':token.key
				}
				return Response(data)
	3>在前端LoginBox.vue中写入
			default:
                console.log(res.data.token)
				break;
### 43.vueCli父向子组件通信
	1>在父组件app.vue中登录按钮加入判断
		data() {return {boxtarget:0}}
		<button @click="showLoginRegisterBox(1)">登录</button>
		<button @click="showLoginRegisterBox(2)">注册</button>
		<LoginBox v-if="boxtarget" :target="boxtarget" @hideBox="hideLoginRegisterBox"></LoginBox>
		
		//展示登录注册框体
		showLoginRegisterBox(value) {
		  this.boxtarget=value
		},
		//隐藏登录注册框体
		hideLoginRegisterBox() {
		  this.boxtarget=0
		}
	2>在子组件LoginBox.vue中加入
		<!-- click.self表示只影响自身标签，不会影响下面的子标签 -->
		<div id="login" @click.self="hideSelf">
		<div v-if="target == 2" class="item">
          <div class="span">重复密码：</div>
          <input v-model="password2" type="text" placeholder="再次输入密码" />
        </div>
		<button v-if="target == 1" @click="toLogin">登录</button>
        <button v-if="target == 2" @click="toRegister">注册</button>
		
		data() {return {password2: "",};},
		props:['target'],
		mounted() {
		  console.log(this.target)
		},
		methods: {
			hideSelf() {
			  this.$emit("hideBox");
			}，
			toRegister() {},
		}
### 44.前端提交到Django用户注册
	1>在LoginBox.vue中写入注册方法
		toRegister() {
		  var username = this.username;
		  var password = this.password;
		  var password2 = this.password2;
		  console.log(username, password, password2);
		  if (username.length > 0 && password.length > 0 && password2.length > 0) {
			if (password != password2) {
			  alert("密码两次输入不同");
			} else {
			  axios({
				url: "http://127.0.0.1:9000/register/",
				data: Qs.stringify({
				  username,
				  password,
				  password2,
				}),
				method: "post",
				headers: {
				  "Content-Type": "application/x-www-form-urlencoded",
				},
			  }).then((res) => {
				console.log(res);
				switch (res.data) {
					case 'same':
						alert('存在同名用户')
						break
					default:
						break;
				}
			  });
			}
		  }else{
			  alert('缺少必填项')}},
	2>在后端urls.py中加入路径path('register',api.toRegister)
	3>在api.py中写入from django.contrib.auth.hashers import make_password
		@api_view(['GET', 'POST'])
		def toRegister(request):
			username = request.POST['username']
			password = request.POST['password']
			password2 = request.POST['password2']
			print(username, password, password2)
			# 用户是否存在
			user = User.objects.filter(username=username)
			if user:
				return Response('same')
			else:
				newPwd = make_password(password,username)
				print(newPwd)
				newUser = User(username=username, password=newPwd)
				newUser.save()
			return Response('ok')