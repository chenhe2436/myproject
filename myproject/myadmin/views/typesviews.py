from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import admin,Types
import os
# Create your views here.
def addtop(request):
	if request.method == 'GET':
		return render(request,'myadmin/types/addtop.html')

	if request.method == 'POST':

		# 保存数据
		obj = Types()
		obj.tname = request.POST['name']
		obj.pid = request.POST['pid']
		obj.path = '0,'
		obj.save()
		# 跳转到分类列表页
		return HttpResponse('<script>alert("添加成功,请添加其他类");location.href="'+reverse('myadmin_types_add')+'"</script>')


def add(request):
	# 如果是get 方式  那么就执行添加
	if request.method == 'GET':

		data = Types.objects.extra(select={'paths':'concat(path,id)'}).order_by('paths')
			
		# content = {'tnamelist':data}
		if not data:
			return HttpResponse('<script>alert("没有顶级分类,请先添加!");location.href="'+reverse('myadmin_types_addtop')+'"</script>')
		else:
			for i in data:
				num = i.path.count(',')-1
				i.tname = '------' * num + i.tname
			content = {'data':data}
			# 跳转到添加页面
			return render(request,'myadmin/types/add.html',content)

	# 如果是post方式  那么就执行保存
	if request.method == 'POST':
		# 保存数据

		obj = Types()
		name = request.POST['name']
		get_all_data = Types.objects.all()
		n = 0
		for i in get_all_data:
			if i.tname == name:
				n += 1
		if n == 0:

			obj.tname = request.POST['name']


			obj.pid = request.POST['pid']

			if obj.pid == '0':
				obj.path = '0,'
			else:
				pa = Types.objects.get(id = obj.pid)
				obj.path = pa.path + str(obj.pid) + ','
			obj.save()
			# 跳转到分类列表页
			return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')
		else:

			return HttpResponse('<script>alert("分类已存在,请重新添加");location.href="'+reverse('myadmin_types_add')+'"</script>')


def list(request):

	sor = request.GET.get('uid','id')
	types = request.GET.get('type',None)
	keywords = request.GET.get('keywords',None)
	sear = []

	if types:

        # 有搜索条件
		if types == 'all':
            # 全条件搜索
            # select * from user where username like '%aa%' 
            
			from django.db.models import Q
			obj = Types.objects.filter(
                Q(tname__contains=keywords)|
                Q(id__contains=keywords)|
                Q(pid__contains=keywords)|
                Q(path__contains=sear)
            )

		elif types == 'typesname':
            # 按照用户名搜索
			obj = Types.objects.filter(tname__contains=keywords)
        
		elif types == 'id':
            # 按照年龄搜索
			obj = Types.objects.filter(id__contains=keywords)

		elif types == 'pid':
            # 按照 email 搜索
			obj = Types.objects.filter(pid__contains=keywords)

		elif types == 'level':
			if keywords.isdigit():
				obj = Types.objects.filter()
			for i in obj:
			
				if i.path.count(',') == int(keywords):
					sear.append(i.id)
			obj = Types.objects.filter(id__in=sear)
	else:
        # 获取所有的用户数据
		obj = Types.objects.filter()

	data = obj.order_by(sor)

	
	for i in data:
		num = i.path.count(',')-1
		i.tname = '------' * num + i.tname
		if i.pid == 0:
			i.pname = i.tname
		else:
			
			p = Types.objects.get(id = i.pid)
			i.pname = p.tname


	from django.core.paginator import Paginator
    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
	paginator = Paginator(data,10)
    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	data = paginator.page(p)
	# 参数设置
	
	content = {'data':data}
	# 跳转到添加页面
	return render(request,'myadmin/types/list.html',content)
	
	# data = Types.objects.all()

	# content = {'data':data}

	# return render(request,'myadmin/types/list.html',content)
	# return HttpResponse(123)

def delete(request):
	uid = request.GET.get('uid',None)
	num = Types.objects.filter(pid = uid).count()
	obj = Types.objects.get(id = uid)
	if num != 0:
		return HttpResponse('<script>alert("当前类下有子类,不能删除");location.href="'+reverse('myadmin_types_list')+'"</script>')
	else:

		obj.delete()
		return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

def update(request):

	if request.method == 'GET':

		uid = request.GET.get('uid',None)

		obj = Types.objects.all()

		content = {'data':obj}

		return render(request,'myadmin/types/update.html',content)
	
	if request.method == 'POST':

		uid = request.POST.get('uid',None)

		name = request.POST.get('name',None)

		obj = Types.objects.get(id = uid)
		print(obj.tname)
		obj.tname = name

		obj.path = obj.path
		obj.pid = obj.pid
		obj.save()

		return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_types_list')+'"</script>')




