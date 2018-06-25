from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import admin,Types
import os
from . usersviews import uploads
# Create your views here.

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

# 添加视图函数
def add(request):
	if request.method == 'GET':
		data = Types.objects.all()
		
		for i in data:

			num = i.path.count(',')-1
			i.tname = '------' * num + i.tname
		content = {'data':data}
		content['info'] = '<table class="standard-table" width="1239" style="width: 679px;"><tbody><tr class="standard-table-group firstRow" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">基础信息</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">品牌</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">魅族</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">型号</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">魅蓝6T</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">尺寸</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">152.3*73*8.4mm</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">电池容量</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">3300mAh</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">重量</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">145g</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">屏幕</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">屏幕尺寸</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">5.7英寸</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">对比度</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">1000:1</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">分辨率</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">1440x720</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">PPI</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">282</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">亮度</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">450cd/m²（典型值）</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">容量</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">运行内存（RAM）</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">3GB/4GB</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">机身内存</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">32GB<br/>64GB</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">处理器</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">CPU</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">MT6750 八核处理器</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">GPU</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">ARM Mali-T860 图形处理器</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">CPU频率</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">ARM®&nbsp;Cortex®-A53™ 1.5 GHz x4 +<br/>ARM® Cortex®-A53™ 1.0GHz x4</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">摄像</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">前置摄像头</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">800万像素<br/>ƒ/2.0 光圈<br/>4 片式镜头<br/>ArcSoft® 美颜算法 自适应美肤技术<br/>Face AE 自动人脸识别 亮度增强</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">后置摄像头</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">1300 万像素 200 万像素<br/>PDAF 相位对焦 自动对焦系统<br/>人像背景虚化模式<br/>ƒ/2.2 光圈 ƒ/2.4 光圈<br/>5片式镜头 3片式镜头<br/>连拍模式<br/>全景模式<br/>后置闪光灯 补光自然柔和</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">mTouch</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">响应速度</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">0.2s</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">识别角度</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">360°</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">指纹组数</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">5组</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">mTouch传感器</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">电容式触摸传感器</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">运营商与制式</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">全网通</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">全网通（公开版）<br/>移动 4G TD-LTE<br/>联通/电信 4G TD/FDD-LTE<br/>移动 3G TD-SCDMA<br/>联通 3G WCDMA<br/>电信 3G EVDO<br/>移动/联通 2G GSM<br/>电信 2G CDMA</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">其他参数</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">WLAN功能</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">支持 5GHz 和 2.4GHz 频段<br/>802.11 a/b/g/n 无线网络</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">蓝牙</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">Bluetooth 4.1<br/>支持 BLE</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">多媒体</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">视频</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">支持 MP4、3GP、MOV、MKV、AVI、FLV、MPEG 视频格式</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">音频</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">支持 FLAC、APE、AAC、MKA、OGG、MP3、MIDI、M4A、AMR 音频格式</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">图片</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">支持 JPEG、PNG、GIF、BMP 图片格式</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">系统与应用</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">传感器</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">重力感应<br/>红外距离感应<br/>环境光度感应<br/>触摸感应<br/>电子罗盘<br/>软陀螺仪</td></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">导航定位</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">GPS<br/>A-GPS<br/>GLONASS<br/>电子罗盘</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">操作环境</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">操作环境</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">工作环境温度 0 至 35°C<br/>存储温度 -20 至 45°C</td></tr><tr class="standard-table-group" style="background: rgb(244, 245, 246); text-indent: 30px;"><th colspan="2" style="border-color: rgb(220, 220, 220); width: 1238px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">包装清单</th></tr><tr><th style="border-color: rgb(220, 220, 220); width: 296px; color: rgb(51, 51, 51); font-weight: 400; padding: 14px 0px;">包装清单</th><td style="border-color: rgb(220, 220, 220); padding: 10px 40px; line-height: 28px; color: rgb(153, 153, 153);">主机 x 1<br/>电源适配器 x 1<br/>保修证书 x 1<br/>SIM卡顶针 x 1<br/>数据线 x 1</td></tr></tbody></table><p><br/></p>'

		# 跳转到添加页面
		return render(request,'myadmin/goods/add.html',content)
	# if request.method == 'POST':

 #        # 先判断是否右图片上传
 #        if not request.FILES.get('pic',None):
 #            return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')

 #        pic = uploads(request)
 #        if pic == 1:
 #            return HttpResponse('<script>alert("图片类型错误");location.href="'+reverse('myadmin_goods_add')+'"</script>')

 #        # 执行商品的添加
 #        # 接受表单提交的数据,
 #        data = request.POST.copy().dict()
 #        # 删除掉 csrf验证的字段数据
 #        del data['csrfmiddlewaretoken']
 #        data['pics'] = pic
 #        data['typeid'] = Types.objects.get(id = data['typeid'])

 #        # 执行用户的创建
 #        ob = Goods.objects.create(**data)

	# 	return HttpResponse('<script>alert("");location.href="'+reverse('myadmin_goods_add')+'"</script>')
        

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
			if keywords == '会员':
				keywords = 0
	        # 按照 status 搜索
				obj = admin.objects.filter(status__contains=keywords)

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

def delete(request):

	uid = request.GET.get('uid',None)

	obj = admin.objects.get(id = uid)

	if obj.pic != '/static/myadmin/pic/user03.png':
		os.remove('.'+obj.pic)

	obj.delete()

	return HttpResponse('<script>alert("删除成功");location.href="'+reverse('myadmin_users_list')+'"</script>')

def update(request):

	uid = request.GET.get('uid',None)

	obj = admin.objects.get(id = uid)

	if request.method == 'GET':

		content = {'admin':obj}

		return render(request,'myadmin/users/update.html',content)

	elif request.method == 'POST':

		print(12345678946411111)
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

def ajax(request):

	a = {'a':1,'b':2}


	return HttpResponse()