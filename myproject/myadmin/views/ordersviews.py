from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import admin,Types,Goods,Orders,OrderInfo
import os
# Create your views here.



def list(request):
	# sor = request.GET.get('uid','id')
	# types = request.GET.get('type',None)
	# keywords = request.GET.get('keywords',None)

	# if types:

 #        # 有搜索条件
	# 	if types == 'all':
 #            # 全条件搜索
 #            # select * from user where username like '%aa%' 
            
	# 		from django.db.models import Q
	# 		obj = Goods.objects.filter(
 #                Q(title__contains=keywords)|
 #                Q(id__contains=keywords)|
 #                Q(status__contains=keywords)|
 #                Q(price__contains=keywords)|
 #                Q(store__contains=keywords)|
 #                Q(clicknum__contains=keywords)|
 #                Q(num__contains=keywords)|
 #                Q(addtime__contains=keywords)
                
 #            )
	# 	elif types == 'goodsname':
 #            # 按照用户名搜索
	# 		obj = Goods.objects.filter(title__contains=keywords)
        
	# 	elif types == 'id':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(id__contains=keywords)
		
	# 	elif types == 'price':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(price__contains=keywords)
	# 	elif types == 'store':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(store__contains=keywords)
	# 	elif types == 'clicknum':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(clicknum__contains=keywords)
	# 	elif types == 'num':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(num__contains=keywords)
	# 	elif types == 'status':
 #            # 按照id搜索
	# 		if keywords in '新发布':
	# 			keywords = 0
	# 		obj = Goods.objects.filter(status__contains=keywords)
	# 	elif types == 'addtime':
 #            # 按照id搜索
	# 		obj = Goods.objects.filter(addtime__contains=keywords)

	# else:
 #        # 获取所有的用户数据
	# 	obj = Goods.objects.filter()

	# data = obj.order_by(sor)

	

	# from django.core.paginator import Paginator
 #    # 实例化分页对象,参数1,数据集合,参数2 每页显示条数
	# paginator = Paginator(data,10)
 #    # 获取当前页码数
	# p = request.GET.get('p',1)
 #    # 获取当前页的数据
	# data = paginator.page(p)

	# context = {'data':data}


	oobj = Orders.objects.all()

	data = {}
	
	for i in oobj:

		single = {}

		oinfoobj = OrderInfo.objects.filter(orderid = i.id)

		for j in oinfoobj:
			single['name'] = i.addressid.name
			single['address'] = i.addressid.address
			single['pic'] = j.gid.pics
			single['title'] = j.gid.title
			single['price'] = int(j.gid.price)
			single['totalprice'] = int(i.totalprice)
			single['totalnum'] = i.totalnum
			single['status'] = i.status
			single['addtime'] = i.addtime
			single['uid'] = i.id
			data[i.id] = single

	content = {'data':data}
	return render(request,'myadmin/orders/list.html',content)

def xiangqing(request):
	uid = request.GET.get('uid',None)
	oobj = Orders.objects.get(id = uid)
	oinfoobj = OrderInfo.objects.filter(orderid = uid)
	data = {}

	for i in oinfoobj:

		single = {}
		single['pic'] = i.gid.pics
		single['title'] = i.gid.title
		single['status'] = i.gid.status
		single['addtime'] = i.orderid.addtime
		single['price'] = int(i.gid.price)
		single['num'] = i.num
		single['totalprice'] = i.num * i.gid.price
		data[i.id] = single
	content = {'data':data}
	return render(request,'myadmin/orders/xiangqing.html',content)


def update(request):
	
	if request.method == 'GET':
		uid = request.GET.get('uid',None)

		oobj = Orders.objects.get(id= uid)
		data = oobj.status
		content = {'data':data,'uid':uid}
		return render(request,'myadmin/orders/update.html',content)
	if request.method == 'POST':
		uid = request.POST.get('uid',None)
		
		statusid = request.POST.get('statusid',None)
	
		oobj = Orders.objects.filter(id= uid)
		
		for i in oobj:	
			i.status = statusid
			i.save()
	
		return render(request,'myadmin/orders/list.html')


