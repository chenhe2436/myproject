from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from .. models import admin
import os
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def testrender(request):
	return render(request,'http://www.baidu.com')

def test(request):
	return HttpResponseRedirect('http://www.baidu.com')


def ajaxupload(request):

    import time,random

    myfile = request.FILES.get('pic',None)
    # 判断是否有文件上传
    if not myfile:
        return JsonResponse({'code':1,'msg':'没有文件上传'})

    # 执行文件上传
    # 自定义文件名 时间戳+随机数+.jpg
    filename = str(time.time())+str(random.randrange(10000,99999))

    # 获取当前上传文件的后缀名
    hzm = myfile.name.split('.').pop()
    # 允许上传的文件类型
    arr = ['png','jpg','gif','jpeg','bmp','icon']
    # 如果上传的文件类型不正确
    if hzm not in arr:
        return JsonResponse({'code':2,'msg':'上传的文件类型错误'})

    # 打开文件
    file = open('./static/pics/'+filename+'.'+hzm,'wb+')
    # 分块写入文件  
    for chunk in myfile.chunks():      
           file.write(chunk)  
    # 关闭文件
    file.close()

    # 返回文件的url路径
    return JsonResponse({'code':0,'msg':'上传成功','url':'/static/pics/'+filename+'.'+hzm})
    


    return HttpResponse('ajaxupload')

# 定义首页视图函数
def index(request):
	# 从数据库获取所有数据
	obj = admin.objects.filter()
	# 导入分页
	from django.core.paginator import Paginator
	# 实例化分页对象,参数1 数据集合,参数2 每页显示条数
	paginator = Paginator(obj,10)
	# 获取页码数
	p = request.GET.get('p',1)
	# 获取当前页码数
	obj = paginator.page(p)
	# 参数传递
	content = {'admin':obj}
	# 返回list页面
	return render(request,'myadmin/users/list.html',content)


def mylogin(request):
	if request.method == 'GET':

		return render(request,'myadmin/login.html')
	if request.method == 'POST':

		name = request.POST.get('username',None)
		password = request.POST.get('password',None)
	
		user = authenticate(request, username=name, password=password)
		if user:
            #登录
			login(request,user)
			return HttpResponse('<script>alert("登录成功");location.href="'+reverse('myadmin_users_index')+'"</script>')

		else:

			return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')



def mylogout(request):

	request.session['AdminLogin'] = {}
	
	return HttpResponse('<script>alert("退出成功");location.href="/myadmin/"</script>')


@permission_required('myadmin.insert_users',raise_exception = True)
# 添加视图函数
def add(request):
	# 判断方法类型GET
	if request.method == 'GET':
		# 返回增加页面
		return render(request,'myadmin/users/add.html')
	# 判断方法类型POST
	elif request.method == 'POST':
		# 返回字典格式请求值
		data = request.POST.copy().dict()
		# 删除csrf 
		del data['csrfmiddlewaretoken']
		# 导入密码加密包
		from django.contrib.auth.hashers import make_password, check_password
		data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
		# 判断是否有文件上传
		if request.FILES.get('pic',None):
			# 调用上传函数,并将pic键值对添加进字典
			data['pic'] = uploads(request)
			# 判断文件类型是否不正确
			print(data)
			if data['pic'] == 1:
				# 如果不正确返回信息
				return HttpResponse('<script>alert("上传的文件类型不符合要求");location.href="'+reverse('myadmin_users_add')+'"</script>')
		# 如果没有图片上传,即pic值为空
		if not data['pic']:

			# 设置默认图片路径
			data['pic'] = '/static/myadmin/pic/user03.png'
		# 添加信息进数据库
		data['status'] = 1
		obj = admin.objects.create(**data)
		# 添加成功返回信息
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_users_list')+'"</script>')
# 列表页

@permission_required('myadmin.insert_users',raise_exception = True)
def list(request):
	 # 获取搜索条件
	sor = request.GET.get('uid','id')
	types = request.GET.get('type',None)
	keywords = request.GET.get('keywords',None)

    # 判断是否具有搜索条件

	if types:
        # 有搜索条件
		if types == 'all':
            # 全条件搜索
            # select * from user where username like '%aa%' 
			from django.db.models import Q
			obj = admin.objects.filter(
                Q(name__contains=keywords)|
                Q(age__contains=keywords)|
                Q(email__contains=keywords)|
                Q(phone__contains=keywords)|
                Q(sex__contains=keywords)|
                Q(status__contains=keywords)
            )

		elif types == 'name':
            # 按照用户名搜索
			obj = admin.objects.filter(name__contains=keywords)
        
		elif types == 'age':
            # 按照年龄搜索
			obj = admin.objects.filter(age__contains=keywords)

		elif types == 'email':
            # 按照 email 搜索
			obj = admin.objects.filter(email__contains=keywords)

		elif types == 'phone':
            # 按照 phone 搜索
			obj = admin.objects.filter(phone__contains=keywords)

		elif types == 'sex':
            # 按照 sex 搜索
			obj = admin.objects.filter(sex__contains=keywords)

		elif types == 'status':
			if keywords == '异常':
				keywords = 1
	        # 按照 status 搜索
				obj = admin.objects.filter(status__contains=keywords)
			elif keywords == '会员':
				keywords = 0
	        # 按照 status 搜索
				obj = admin.objects.filter(status__contains=keywords)
			else:
				return HttpResponse('<script>alert("输入信息有误，请重试");history.back(-1)</script>')


	else:
        # 获取所有的用户数据
		obj = admin.objects.filter()
	obj = obj.order_by(sor)
	from django.core.paginator import Paginator
    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
	paginator = Paginator(obj, 10)
    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	obj = paginator.page(p)
	# 参数设置
	content = {'admin':obj}
	# 
	return render(request,'myadmin/users/list.html',content)


@permission_required('myadmin.del_users',raise_exception = True)

def delete(request):

	uid = request.GET.get('uid',None)

	obj = admin.objects.get(id = uid)

	if obj.pic != '/static/myadmin/pic/user03.png':
		os.remove('.'+obj.pic)

	obj.delete()

	return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_users_list')+'"</script>')


@permission_required('myadmin.edit_users',raise_exception = True)

def update(request):

	uid = request.GET.get('uid',None)

	obj = admin.objects.get(id = uid)

	if request.method == 'GET':

		content = {'admin':obj}

		return render(request,'myadmin/users/update.html',content)

	elif request.method == 'POST':

		if request.FILES.get('pic',None):
            # 判断是否使用的默认图
			if obj.pic:
                # 如果使用的不是默认图,则删除之前上传的头像
				os.remove('.'+obj.pic)

            # 执行上传
			obj.pic = uploads(request)
                

		obj.name = request.POST['name']
		obj.email = request.POST['email']
		obj.age = request.POST['age']
		obj.sex = request.POST['sex']
		obj.phone = request.POST['phone']
		obj.status = request.POST['status']
		obj.save()

		return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_users_list')+'"</script>')


def uploads(request):

	myfile = request.FILES.get('pic',None)

	be = myfile.name.split('.').pop()

	arr = ['jpg','png','jpeg','gif']

	if be not in arr:

		return 1

	import time,random
	filename = str(time.time())+str(random.randint(1,99999))+'.'+be

	destination = open("./static/myadmin/pic/"+filename,"wb+")

	for chunk in myfile.chunks():      
		destination.write(chunk)  

	destination.close()
	return '/static/myadmin/pic/'+filename

