from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from myadmin.models import admin,Types,Goods,Address,Orders,OrderInfo,Citys

from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# 首页
def index(request):

    # 先获取所有的顶级分类
    data1 = Types.objects.get(pid = 0)

    data = Types.objects.filter(pid=data1.id)

    erdata = []
    for x in data:
        # 获取当前类下的子类
        x.sub = Types.objects.filter(pid=x.id)
        for v in x.sub:
            #获取当前子类下的商品 
            v.goodssub = Goods.objects.filter(typeid=v.id)
            erdata.append(v)


    context = {'typegoodslist':data,'erdata':erdata}
    return render(request,'myhome/index.html',context)

# 列表
def list(request,tid):

    # 根据分类id获取商品信息
    data = Goods.objects.filter(typeid=tid)



    context = {'goodslist':data}

    return render(request,'myhome/list.html',context)

# 搜索
def search(request):

    # 获取搜索参数
    keywords = request.GET.get('keywords',None)
    if not keywords:
        return HttpResponse('<script>history.back(-1)</script>')

    #商品的模糊搜索
    from django.db.models import Q
    data = Goods.objects.filter(
                Q(descr__contains=keywords)|
                Q(info__contains=keywords)|
                Q(title__contains=keywords)
            )

    context = {'goodslist':data}

    return render(request,'myhome/search.html',context)

# 详情
def info(request,sid):
    try:
        # 根据商品id获取商品信息
        data = Goods.objects.get(id=sid)

        # 修改当前商品的点击量
        data.clicknum = data.clicknum+1
        data.save()

        context = {'ginfo':data}
        return render(request,'myhome/info.html',context)
        
    except:
        pass
    
# 登录
def login(request):
    nexturl = request.GET.get('next','/')
    if request.method == "GET":
        return render(request,'myhome/login.html')

    elif request.method == "POST":
        # 执行登录
        # 根据用户名先获取用户对象.在检测密码是否正确
        try:
            ob = admin.objects.get(name = request.POST['username'])
            # 检测密码是否正确
            res = check_password(request.POST['password'],ob.password)
            if res:
                # 密码正确
                request.session['VipUser'] = {'uid':ob.id,'username':ob.name}
                return HttpResponse('<script>alert("登录成功");location.href="'+nexturl+'"</script>')
        except:
            # 用户名错误
            pass
        
        return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')

# 注册
def register(request):
    if request.method == 'GET':
        return render(request,'myhome/register.html')

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
            data['status'] = 0
            ob = admin.objects.create(**data)

            # 记录用户登录的状态  session
            request.session['VipUser'] = {'uid':ob.id,'username':ob.name}

            return HttpResponse('<script>alert("注册成功");location.href="/"</script>')
        # except pymysql.err.IntegrityError:
            # return HttpResponse('<script>alert("用户名已存在");history.back(-1)</script>')
        except:
            pass

        return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')

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
# 退出
def logout(request):
    request.session['VipUser'] = {}
    
    return HttpResponse('<script>alert("退出成功");location.href="/"</script>')

# 验证码
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

# 加入购物车
def addcart(request):
    # 获取商品id,商品购买数量
    sid = request.GET['sid']
    
    num = int(request.GET['num'])

    # 先获取购物车的商品数据
    data = request.session.get('cart',{})

    # 判断要购物的商品是否已经存在购物车里
    if sid in data.keys():
        # 存在,修改数量
        data[sid]['num'] += num
    else:
        # 不存在,添加
        # 定义加入购物车的商品数据格式
        ob = Goods.objects.get(id=sid)
        goods = {'id':ob.id,'title':ob.title,'price':float(ob.price),'pics':ob.pics,'num':num}
        # 把商品加入购物车
        data[sid] = goods

    # 把购物车存入session
    request.session['cart'] = data

    return HttpResponse('1')

# 购物车列表
def cartlist(request):
    # 获取session的购物车
    data = request.session.get('cart',None)

    if data:

        data = data.values()

    return render(request,'myhome/cart.html',{'data':data})

# 清空购物车
def cartclear(request):
    request.session['cart'] = {}

    return HttpResponse('<script>location.href="/cartlist/"</script>')

# 删除购物车的商品
def delcart(request):
    sid = request.GET['sid']
    # 获取sessin中的购物车数据
    data = request.session['cart']

    del data[sid]

    # 把购物车重新写入session
    request.session['cart'] = data 

    return HttpResponse('0')

# 修改购物车数量
def editcart(request):
    sid = request.GET['sid']
    num = int(request.GET['num'])

    #在session获取购物车数据
    data = request.session['cart']

    # 修改
    data[sid]['num'] = num

    # 把购物车重新写入session
    request.session['cart'] = data

    return HttpResponse('0')

# 订单确认
def ordercheck(request):
    # 获取购物车提交的数据
    items = eval(request.GET['items'])

    # [{'num': 2, 'goodsid': '4'}, {'num': 3, 'goodsid': '22'}]

    data = {}
    totalprice = 0
    totalnum = 0

    for x in items:
        ob = Goods.objects.get(id=x['goodsid'])
        x['title'] = ob.title
        x['price'] = float(ob.price)
        x['pics'] = ob.pics
        # 计算总价和总数
        totalprice += x['num']*x['price']
        totalnum += x['num']

    data['totalprice'] = round(totalprice,2)
    data['totalnum'] = totalnum
    data['items'] = items

    # 把确认的商品信息.,存入session
    request.session['order'] = data



    # {
    #     list:[{'num': 2, 'goodsid': '4'}, {'num': 3, 'goodsid': '22'}],
    #     totalprice:999.99,
    #     totalnum:5,
    # }

    # 需要获取当前用户的收货地址
    addlist = Address.objects.filter(uid=request.session['VipUser']['uid'])


    context = {'data':data,'addlist':addlist}

    return render(request,'myhome/ordercheck.html',context)

# 地址修改
def addressedit(request):
    aid = int(request.GET['aid'])
    uid = request.session['VipUser']['uid']
    # 获取当前用户的所有收货地址
    obs = Address.objects.filter(uid=uid)
    for x in obs:
        if x.id == aid:
            x.status = 1
        else:
            x.status = 0
        x.save()

    return HttpResponse(0)

# 地址添加
def addressadd(request):



    data = eval(request.GET['data'])

    # {
    #     'xiangxi': '洪水街14号', 
    #     'address': ['浙江省', '温州市', '洪山区'], 
    #     'phone': '13701383017', 
    #     'name': '猪肉脯',
    # }
    areaname = []
    for i in data['address']:
        name = Citys.objects.get(id = int(i)).name
        areaname.append(name)

    data['address'] = ",".join(areaname)
    data['status'] = 1
    data['uid'] = admin.objects.get(id=request.session['VipUser']['uid'])

    # 添加地址信息
    res =  Address.objects.create(**data)

    # print(res)
    
    return HttpResponse(0)

# 生成订单
def ordercreate(request):

    # 接受用户id
    uid = request.session['VipUser']['uid']
    # 收货地址id
    addressid = request.POST['addressid']

    # 商品信息
    data = request.session['order']

    # 获取购物车中的数据
    cart = request.session['cart']

 

    '''
        {
            '4': {'price': 9.9, 'num': 2, 'id': 4, 'title': '小蛋糕真好吃:23', 'pics': '/static/pics/1530080135.535089758178.jpg'}, 
            '22': {'price': 9.9, 'num': 3, 'id': 22, 'title': '小蛋糕真好吃:24', 'pics': '/static/pics/1530080135.535089758178.jpg'}, 
            '3': {'price': 1999.99, 'num': 1, 'id': 3, 'title': '小蛋糕真好吃:22', 'pics': '/static/pics/1530080135.535089758178.jpg'}
        }


    '''


    # 生成订单
    ob = Orders()
    ob.uid = admin.objects.get(id=uid)
    ob.addressid = Address.objects.get(id=addressid)
    ob.totalprice = data['totalprice']
    ob.totalnum = data['totalnum']
    ob.save()

     # 'items': [
     # {'price': 1999.99, 'pics': '/static/pics/1530080135.535089758178.jpg', 'num': 1, 'title': '小蛋糕真好吃:22', 'goodsid': '3'}, 
     # {'price': 9.9, 'pics': '/static/pics/1530080135.535089758178.jpg', 'num': 3, 'title': '小蛋糕真好吃:24', 'goodsid': '22'}
     # ]

    # .订单详情
    for v in data['items']:
     
        oinfo = OrderInfo()
        oinfo.orderid = ob
        oinfo.gid = Goods.objects.get(id=v['goodsid'])
        oinfo.num = v['num']
        oinfo.save()
        # 在购物车中删除当前购买的商品
        del cart[v['goodsid']]


    # 清除购物车中已经下单的商品,清除order数据
    request.session['cart'] = cart
    request.session['order'] = ''

    # 把生成订单id get请求到一个新的付款页面

    return HttpResponse('<script>location.href="/buy/?orderid='+str(ob.id)+'"</script>')

# 支付
def buy(request):
    # 获取当前的订单id
    orderid = request.GET['orderid']

    obj = Orders.objects.get(id = orderid)

    addr = obj.addressid.address
    name = obj.addressid.name
    phone = obj.addressid.phone
    xiangxi = obj.addressid.xiangxi
  

    content = {'totalprice':obj.totalprice,'addr':addr,'name':name,'xiangxi':xiangxi,'phone':phone,'orderid':orderid}

    return render(request,'myhome/buy.html',content)

# 支付成功

def success(request):
    orderid = request.GET['orderid']
    obj = Orders.objects.get(id = orderid)

    addr = obj.addressid.address
    name = obj.addressid.name
    phone = obj.addressid.phone
    xiangxi = obj.addressid.xiangxi

    obj.status = 1
    obj.save()

    content = {'totalprice':obj.totalprice,'addr':addr,'name':name,'xiangxi':xiangxi,'phone':phone,'orderid':orderid}


    return render(request,'myhome/success.html',content)




# 我的个人中心
def mycenter(request):
    

    return render(request,'myhome/word/index.html')

# 我的订单
def myorders(request):
    # 获取当前用户的所有订单
    data = Orders.objects.filter(uid=request.session['VipUser']['uid'])

    context = {'orderlist':data}
    
    return render(request,'myhome/word/myorders.html',context)
# session测试
def sesset(request):
    
    # 设置session
    # request.session['abc'] = 'aabbcc'
    # request.session['def'] = 'ddeeff'
    # request.session['VipUser'] = {'uid':1}

    # request.session['name'] ='小明'


    request.session['age'] = 20   
    request.session.set_expiry(10)


    return HttpResponse('设置session')

def sesget(request):
    
    # 获取session数据
    # 获取session中键=abc的数据,如果不存在,报错
    # print(request.session['abc'])
    # print(request.session.get('abc',None))

    print(request.session.values())
    # 删除session

    # 删除单个key  如果key不存在,则报错
    # del request.session['VipUser']

    # if not request.session.get('VipUser',None):
    #     print('退出登录')


    # #清除所有会话,但不会删除数据库中会话数据
    # request.session.clear() 


    #删除当前的会话数据
    # request.session.flush()


    return HttpResponse('获取session')

def getcity(request):
    
    upid = request.GET.get('upid',0)
    
    obs = Citys.objects.filter(upid = upid)

    data = []

    for i in obs:

        a = {'id':i.id,'name':i.name}

        data.append(a)

    return JsonResponse(data,safe = False)

def citys(request):

    return render(request,'citys.html')
