from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin.models import admin,Types,Goods
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def index(request):
	# 因为与老师的模型不一样，在我的模型中
	# 没有固定顶级分类，所以一级分类的pid应该是获得顶级id
	objtop = Types.objects.get(pid =0)
	
	data = Types.objects.filter(pid = objtop.id)
	erdata = []
	for i in data:
		i.two = Types.objects.filter(pid = i.id)
		i.goods = Goods.objects.filter(typeid = i.id)
	
		erdata.append(i)
		for j in i.two:
			j.goods = Goods.objects.filter(typeid = j.id)

	content = {'data':data,'erdata':erdata}

	return render(request,'myapp/index.html',content)

def login(request):

	if request.method == "GET":

		return render(request,'myapp/login.html')
	elif request.method == "POST":
		try:
			ob = admin.objects.get(name = request.POST['name'])
			# 检测密码是否正确
			res = check_password(request.POST['password'],ob.password)
			if res:
				# 密码正确
				request.session['VipUser'] = {'uid':ob.id,'name':ob.name}
				return HttpResponse('<script>alert("登录成功");location.href="/myapp"</script>')
			else:
				return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')

		except:
			return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')

def logout(request):
	request.session['VipUser'] = {}
	
	return HttpResponse('<script>alert("退出成功");location.href="/myapp"</script>')

def register(request):
	if request.method == 'GET':
		return render(request,'myapp/register.html')
	elif request.method == 'POST':
		# 先判断验证码是否正确
		if request.POST['vcode'].upper() != request.session['verifycode'].upper():
			return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')

		# 接受表单提交的数据,
		data = request.POST.copy().dict()
		# 删除掉 csrf验证的字段数据
		del data['csrfmiddlewaretoken']
		del data['vcode']

		# print(data)
		try:
			# 进行密码加密            
			data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
			data['pic'] = '/static/myadmin/pic/user03.png'
			# 执行用户的注册
			ob = admin.objects.create(**data)

			# 记录用户登录的状态  session
			request.session['VipUser'] = {'uid':ob.id,'name':ob.name}

			return HttpResponse('<script>alert("注册成功");location.href="/myapp"</script>')
		# except pymysql.err.IntegrityError:
			# return HttpResponse('<script>alert("用户名已存在");history.back(-1)</script>')
		except:
			pass

		return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')

def list(request,gid):

	objtop = Types.objects.get(pid =0)
	
	data = Types.objects.filter(pid = objtop.id)
	erdata = []
	for i in data:
		i.two = Types.objects.filter(pid = i.id)
		i.goods = Goods.objects.filter(typeid = i.id)

	obj = Goods.objects.filter(typeid = gid)

	types = Types.objects.get(id = gid)

	content = {'data':data,'types':types,'obj':obj}

	return render(request,'myapp/list.html',content)

def testname(request):

	con = request.GET.get('con',None)

	obj = admin.objects.filter().values('name')

	if len(con) < 6:
		return JsonResponse({'msg':'当前已输入{}个字符，还差个{}字符'.format(len(con),6-len(con))})
	n = 0
	for i in obj:
		if i['name'] == con:
			n += 1
	if n == 0:
	
		return JsonResponse({'msg':'用户名可用'})

	else:

		return JsonResponse({'msg':'用户名不可用'})

def info(request,gid):

	# con = request.GET.get('con',None)

	return render(request,'myapp/info.html')

def vcode(request):
	#引入绘图模块
	from PIL import Image, ImageDraw, ImageFont
	#引入随机函数模块
	import random
	#定义变量，用于画面的背景色、宽、高
	bgcolor = (random.randrange(20, 100), random.randrange(
		20, 100), 255)
	width = 100
	height = 25
	#创建画面对象
	im = Image.new('RGB', (width, height), bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		draw.point(xy, fill=fill)
	#定义验证码的备选值
	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	#随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str1[random.randrange(0, len(str1))]
	#构造字体对象
	font = ImageFont.truetype('FreeMono.ttf', 23)
	#构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	#绘制4个字
	draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
	draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
	#释放画笔
	del draw
	#存入session，用于做进一步验证
	request.session['verifycode'] = rand_str
	#内存文件操作
	import io
	buf = io.BytesIO()
	#将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'image/png')

def search(request):
	keywords = request.GET.get('keywords',None)

	if not keywords:
		return HttpResponse('<script>history.back(-1)</script>')

	objtop = Types.objects.get(pid =0)
	
	data = Types.objects.filter(pid = objtop.id)
	erdata = []
	for i in data:
		i.two = Types.objects.filter(pid = i.id)
		i.goods = Goods.objects.filter(typeid = i.id)
	
		erdata.append(i)
		for j in i.two:
			j.goods = Goods.objects.filter(typeid = j.id)
	obj = Goods.objects.filter(title__contains=keywords)


	context = {'data':data,'obj':obj,'keywords':keywords}

	return render(request,'myapp/search.html',context)

def cartlist(request):

	data = request.GET.get('cart',None)