from django.db import models

# 创建用户信息
class admin(models.Model):

	name = models.CharField(max_length=50)
	password = models.CharField(max_length=80)
	phone = models.CharField(max_length=50)
	email = models.CharField(max_length=50,null = True)
	age = models.IntegerField(null = True)
	sex = models.CharField(max_length=50,null = True)
	status = models.IntegerField(default = 0)
	addtime = models.DateTimeField(auto_now_add = True,null = True)
	pic = models.CharField(max_length=500,null = True)

# 创建分类信息
class Types(models.Model):

	tname = models.CharField(max_length=50)
	pid = models.IntegerField()
	path = models.CharField(max_length=255,null=True)
	addtime = models.DateTimeField(auto_now_add = True,null = True)

# 创建商品信息

class Goods(models.Model):
	 # 一对多
    typeid =  models.ForeignKey(to="Types", to_field="id")
    title = models.CharField(max_length=255)
    descr = models.CharField(max_length=255,null=True)
    info = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pics = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    store = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
	uid =  models.ForeignKey(to="admin", to_field="id")
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=11)
	address = models.CharField(max_length=20)
	xiangxi = models.CharField(max_length=50)
	status = models.IntegerField(default=0)

class Orders(models.Model):
	uid = models.ForeignKey(to="admin", to_field="id")
	addressid = models.ForeignKey(to="Address", to_field="id")
	totalprice = models.FloatField()
	totalnum = models.IntegerField()
	status = models.IntegerField(default=0)
	addtime = models.DateTimeField(auto_now_add=True,null=True)
class OrderInfo(models.Model):
	orderid = models.ForeignKey(to="Orders", to_field="id")
	gid = models.ForeignKey(to="Goods", to_field="id")
	num = models.IntegerField()
        

class Citys(models.Model):
	name = models.CharField(max_length = 50)
	level = models.IntegerField()
	upid = models.IntegerField()

	class Meta():
		db_table = 'district'