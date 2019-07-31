from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets,filters
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import filters

import uuid
import re
import jwt
import base64
import time,datetime
import random
from django.core.cache import cache
from werkzeug.security import generate_password_hash, check_password_hash

from apps.admin_operation import models
from utils.yanzheng.duanxin import smsseng,verify_sms,zhankui_smsseng
from utils import redis_cli
from utils.token import authenticated,debug1

# Create your views here.

class SendVerificationCode(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 发送短信验证码
        '''
        mobile = request.GET.get("mobile", None)
        print(mobile, 100000001211111)
        assert mobile,110002
        captcha_code = random.randint(1000,9999)
        nowtime = int(time.time() * 100000000) + random.randint(10, 99)
        timestamp_key = str(nowtime) + str(uuid.uuid4().hex)
        cache.set(timestamp_key, captcha_code, 600*5)
        # 发送短信
        # msn = smsseng(msg="平台",mobile=mobile,code=captcha_code)
        # print(msn,"------------------*----------*----------------*-----------")
        # if msn["result"] != '0':
        #     raise Exception("短信发送失败！！")
        msn = zhankui_smsseng(msg="平台",mobile=mobile,code=captcha_code)
        print(msn,"------------------*----------*----------------*-----------")
        if msn["code"] != '0000':
            raise Exception("短信发送失败！！")
        return JsonResponse({"code":1,"msg":"短信已发送","timestamp_key":timestamp_key})

    def post(self,request,*args,**kwargs):
        '''
            TODO: 验证短信验证码
        '''
        time_key = request.data.get("time_key", None)
        code = request.data.get("code", None)
        is_verify = verify_sms(captcha=code,timestamp_key=time_key)
        print(is_verify,111111111111111)
        assert is_verify == 4,110003
        return JsonResponse({"code":1,"msg":"验证成功"})

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        '''
            TODO: 用户登录
        '''
        login_way = request.data.get('login_way', "a01")
        mobile = request.data.get('mobile', None)
        password = request.data.get('password', None)
        sms_code = request.data.get('sms_code', None)
        time_key = request.data.get("time_key", None)
        assert mobile,110002
        assert password,110004
        assert login_way=="a01" or login_way=="a02",110005
        re_data = {}
        if login_way == "a01":
            try:
                user = models.Users.objects.get(mobile=mobile)
                
                if check_password_hash(user.password, password) is True:
                    data = {
                        'mobile':user.mobile,
                        'name':user.u_id,
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    }
                    token = jwt.encode(data, "12345", algorithm='HS256')
                    re_data['code'] = 1
                    re_data['u_id'] = user.u_id
                    re_data['mobile'] = user.mobile
                    re_data['token'] = token.decode('utf8')

                else:
                    re_data['non_fields'] = '用户名或者密码错误'

            except Exception as e:
                print(e)
                re_data['mobile'] = '用户不存在'
        if login_way == "a02":
            assert sms_code,110003
            assert time_key,110005
            try:
                user = models.Users.objects.get(mobile=mobile)
                is_verify = verify_sms(captcha=sms_code,timestamp_key=time_key)
                if is_verify == 4:
                    data = {
                        'mobile':user.mobile,
                        'name':user.u_id,
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    }
                    token = jwt.encode(data, "12345", algorithm='HS256')
                    re_data['code'] = 1
                    re_data['u_id'] = user.u_id
                    re_data['mobile'] = user.mobile
                    re_data['token'] = token.decode('utf8')

                else:
                    re_data['non_fields'] = '验证码错误'

            except Exception as e:
                print(e)
                re_data['mobile'] = '用户不存在'
        return JsonResponse(re_data)

# 添加商品总类
class ProductCategoryView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取商品种类列表
        '''
        try:
            obj_list = models.CommodType.dahl_objects.all().values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'系统错误'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(obj_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    
    @authenticated
    @debug1
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加商品类型
        '''
        
        name = request.data.get('name', None)
        description = request.data.get('description', '')
        # assert name,110055
        try:
            with transaction.atomic():
                ct_id = 'CT' + str(10000 + int(redis_cli.cache.incr('test1112')))
                print(ct_id,'---------2552222222222----------')
                ct_obj = models.CommodType(ct_id=ct_id,
                                    name=name,
                                    description=description)
                ct_obj.save()
        except Exception as e:
            print('------------------------',type(e),111111111111)
            return JsonResponse({'code':110013,'msg':"操作失败"})
        return JsonResponse({'code':1,"msg":"操作成功"})
    @authenticated
    def patch(self,request,*args,**kwargs):
        '''
            TODO: 查看单条
        '''
        pass



# 添加可订购商品
class WROrderableGoodsView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取可订购商品列表
        '''
        pass
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加可订购商品
        '''
        user = request.user
        g_id = 'GC' + str(10000 + int(redis_cli.cache.incr('test1113')))
        g_type = request.data.get('g_type', None)
        g_type_name = request.data.get('g_type_name', None)
        g_name = request.data.get('g_name', None)
        g_image = request.data.getlist('g_image', None)
        g_description = request.data.get('g_description', None)
        try:
            with transaction.atomic():
                g_obj = models.OrderableGoods(g_id=g_id,
                                            g_type=g_type,
                                            g_type_name=g_type_name,
                                            g_name=g_name,
                                            g_image=g_image,
                                            g_description=g_description,
                                            u_id=user.u_id)
                g_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':"操作失败"})
        return JsonResponse({'code':1,"msg":"操作成功"})

# 添加可订购商品详情
class WROrderableGoodsInfoView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 或去商品详情
        '''
        g_id = request.GET.get('g_id', None)
        try:
            g_obj = models.OrderableGoodsInfo.objects.get(g_id=g_id)
            data = {

            }
        except Exception as e:
            print(e)
            data = {

            }
        return JsonResponse({'code':1,'data':data})
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑/添加商品详情
        '''
        user = request.user
        g_id = request.data.get('g_id', None)
        place_origin_province = request.data.get('place_origin_province', None)
        place_origin_city = request.data.get('place_origin_city', None)
        place_origin_county = request.data.get('place_origin_county', None)
        place_origin_village = request.data.get('place_origin_village', None)
        address_detailed = request.data.get('address_detailed', None)
        unit_price = request.data.get('unit_price', None)
        unit_name = request.data.get('unit_name', None)
        traceability_id = request.data.get('traceability_id', '')
        print(g_id,'----')
        try:
            og_obj = models.OrderableGoodsInfo.objects.get(g_id=g_id)
            adict = {}
            if place_origin_province and place_origin_city and place_origin_county and place_origin_village:
                adict['place_origin_province'] = place_origin_province
                adict['place_origin_city'] = place_origin_city
                adict['place_origin_county'] = place_origin_county
                adict['place_origin_village'] = place_origin_village
            if address_detailed:
                adict['address_detailed'] = address_detailed
            if unit_price:
                adict['unit_price'] = unit_price
            if traceability_id:
                adict['traceability_id'] = traceability_id
            try:
                with transaction.atomic():
                    models.OrderableGoodsInfo.objects.filter(g_id=g_id).update(**adict)
                    msg = '编辑成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110024,'msg':'编辑失败'})

        except Exception as e:
            print(e)
            try:
                with transaction.atomic():
                    print(1)
                    g_obj = models.OrderableGoods.objects.get(g_id=g_id)
                    print(2)
                    add_obj = models.OrderableGoodsInfo(g_id=g_id,
                                                        place_origin_province=place_origin_province,
                                                        place_origin_city=place_origin_city,
                                                        place_origin_county=place_origin_county,
                                                        place_origin_village=place_origin_village,
                                                        address_detailed=address_detailed,
                                                        unit_price=unit_price,
                                                        traceability_id=traceability_id,
                                                        g_name=g_obj.g_name,
                                                        unit_name=unit_name)
                    add_obj.save()
                    msg = '添加成功'
            except Exception as e:
                print(e,'1111')
                return JsonResponse({'code':110024,'msg':'添加失败'})
        return JsonResponse({'code':1,'msg':msg})
        
# 编辑可订购商品图文
class WROrderableGoodsGraphicView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看可订购商品图文
        '''
        g_id = request.GET.get('g_id', None)
        try:
            g_obj = models.OrderableGoodsGraphic.objects.get(g_id=g_id)
            data = {

            }
        except Exception as e:
            print(e)
            data = {

            }
        return JsonResponse({'code':1,'data':data})
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑/添加可订购商品图文
        '''
        user = request.user
        g_id = request.data.get('g_id', None)
        title = request.data.get('title', None)
        body = request.data.get('body', None)
        images = request.data.getlist('images', None)
        u_id = user.u_id
        
        try:
            ogg_obj = models.OrderableGoodsGraphic.objects.get(g_id=g_id)
            adict = {}
            if title:
                adict['title'] = title
            if body:
                adict['body'] = body
            if images:
                adict['images'] = images
            try:
                with transaction.atomic():
                    models.OrderableGoodsGraphic.objects.filter(g_id=g_id).update(**adict)
                    msg = '编辑成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110024,'msg':'编辑失败'})
        except Exception as e:
            print(e)
            try:
                with transaction.atomic():
                    u_info = models.UsersInfo.objects.get(u_id=u_id)
                    g_obj = models.OrderableGoods.objects.get(g_id=g_id)
                    g_info = models.OrderableGoodsInfo.objects.get(g_id=g_id)
                    ogg_obj = models.OrderableGoodsGraphic(g_id=g_id,
                                                        g_name = g_obj.g_name,
                                                        title = title,
                                                        body = body,
                                                        images = images,
                                                        u_id = user.u_id,
                                                        nick_name = u_info.nick_name,
                                                        unit_price=g_info.unit_price,
                                                        unit_name=g_info.unit_name,
                                                        avatar = u_info.avatar)
                    ogg_obj.save()
                    msg = '添加成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110024,'msg':'添加失败'})
        return JsonResponse({'code':1,'msg':msg})
# 添加直购商品
class WRDirectCommodView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 直购商品列表(条件：是否上架，时间排序)
        '''
        user = request.user
        try:
            dc_obj = models.DirectCommod.objects.all().values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'系统错误'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(dc_obj, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    @authenticated 
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加直购商品
        '''
        user = request.user
        dc_id = 'DC' + str(10000 + int(redis_cli.cache.incr('test11111')))
        dc_type = request.data.get('dc_type', None)
        dc_name = request.data.get('dc_name', None)
        dc_image = request.data.getlist('dc_image', None)
        dc_description = request.data.get('dc_description', None)
        try:
            with transaction.atomic():
                d_obj = models.DirectCommod(dc_id=dc_id,
                                            dc_type=dc_type,
                                            dc_name=dc_name,
                                            dc_image=dc_image,
                                            dc_description=dc_description,
                                            u_id=user.u_id)
                d_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':"操作失败"})
        return JsonResponse({'code':1,"msg":"操作成功"})

# 编辑直购商品详情
class WRDirectCommodInfoView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 商品详情
        '''
        dc_id = request.GET.get('dc_id', None)
        try:
            g_obj = models.DirectCommodInfo.objects.get(dc_id=dc_id)
            data = {

            }
        except Exception as e:
            print(e)
            data = {

            }
        return JsonResponse({'code':1,'data':data})
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑/添加直购商品详情
        '''
        user = request.user
        dc_id = request.data.get('dc_id', None)
        place_origin_province = request.data.get('place_origin_province', None)
        place_origin_city = request.data.get('place_origin_city', None)
        place_origin_county = request.data.get('place_origin_county', None)
        place_origin_village = request.data.get('place_origin_village', '')
        address_detailed = request.data.get('address_detailed', None)
        producer_name = request.data.get('producer_name', '')
        producer_id = request.data.get('producer_id', '')
        unit_price = request.data.get('unit_price', None)
        traceability_id = request.data.get('traceability_id', '')
        re_data = {}
        try:
            d_obj = models.DirectCommodInfo.objects.get(dc_id=dc_id)
            adict = {}
            if place_origin_province and place_origin_city and place_origin_county:
                adict['place_origin_province'] = place_origin_province
                adict['place_origin_city'] = place_origin_city
                adict['place_origin_county'] = place_origin_county
            if place_origin_village:
                adict['place_origin_village'] = place_origin_village
            if address_detailed:
                adict['address_detailed'] = address_detailed
            if producer_name:
                adict['producer_name'] = producer_name
            if producer_id:
                adict['producer_id'] = producer_id
            if unit_price:
                adict['unit_price'] = unit_price
            if traceability_id:
                adict['traceability_id'] = traceability_id
            try:
                with transaction.atomic():
                    models.DirectCommodInfo.objects.filter(dc_id=dc_id).update(**adict)
                    re_data['code'] = 1
                    re_data['msg'] = '编辑成功'
            except Exception as e:
                re_data['code'] = 110013
                re_data['msg'] = '编辑失败'
                return JsonResponse(re_data)
        except Exception as e:
            print(e)
            try:
                with transaction.atomic():
                    dc_obj = models.DirectCommod.objects.get(dc_id=dc_id)
                    c_obj = models.DirectCommodInfo(
                                                    dc_id=dc_id,
                                                    dc_name=dc_obj.dc_name,
                                                    place_origin_province=place_origin_province,
                                                    place_origin_city=place_origin_city,
                                                    place_origin_county=place_origin_county,
                                                    place_origin_village=place_origin_village,
                                                    address_detailed=address_detailed,
                                                    producer_name=producer_name,
                                                    producer_id=producer_id,
                                                    unit_price=unit_price,
                                                    traceability_id=traceability_id
                                                )
                    c_obj.save()
                    re_data['code'] = 1
                    re_data['msg'] = '添加成功'
            except Exception as e:
                print(e)
                re_data['code'] = 110013
                re_data['msg'] = '添加失败'
                return JsonResponse(re_data)
        return JsonResponse(re_data)
# 编辑直购商品图文
class WRDirectCommodGraphicView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看商品图文
        '''
        dc_id = request.GET.get('dc_id', None)
        try:
            dcg_obj = models.DirectCommodGraphic.objects.get(dc_id=dc_id)
            data = {

            }
        except Exception as e:
            print(e)
            data = {

            }
        return JsonResponse({'code':1,'data':data})
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑/添加图文
        '''
        user = request.user
        dc_id = request.data.get('dc_id', None)
        # dc_name = request.data.get('dc_id', None)
        title = request.data.get('title', None)
        body = request.data.get('body', None)
        images = request.data.get('images', None)
        u_id = user.u_id
        re_data = {}
        try:
            dc_obj = models.DirectCommodGraphic.objects.get(dc_id=dc_id)
            adict = {}
            if title:
                adict['title'] = title
            if body:
                adict['body'] = body
            if traceability_id:
                adict['images'] = images
            try:
                with transaction.atomic():
                    models.DirectCommodGraphic.objects.filter(dc_id=dc_id).update(**adict)
                    re_data['code'] = 1
                    re_data['msg'] = '编辑成功'
            except Exception as e:
                re_data['code'] = 110013
                re_data['msg'] = '编辑失败'
                return JsonResponse(re_data)

        except Exception as e:
            print(e)
            try:
                with transaction.atomic():
                    d_obj = models.DirectCommod.objects.get(dc_id=dc_id)
                    c_obj = models.DirectCommodGraphic(
                                                        dc_id=dc_id,
                                                        dc_name=d_obj.dc_name,
                                                        title=title,
                                                        body=body,
                                                        images=images,
                                                        u_id=u_id
                                                    )
                    c_obj.save()
                    re_data['code'] = 1
                    re_data['msg'] = '添加成功'
            except Exception as e:
                print(e)
                re_data['code'] = 110013
                re_data['msg'] = '添加失败'
                return JsonResponse(re_data)
        return JsonResponse(re_data)

# 添加直购商品库存
class WRDirectCommodStockView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取商品库存列表
        '''
        dc_id = request.GET.get('dc_id', None)
        try:
            dcs_list = models.DirectCommodStock.objects.filter(dc_id=dc_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'系统错误'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(dcs_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加库存
        '''
        user = request.user
        product_specif_id = 'DCS' + str(10000 + int(redis_cli.cache.incr('test111112')))
        dc_id = request.data.get('dc_id', None)
        product_specif = request.data.get('product_specif', None)
        stock_quantity = request.data.get('stock_quantity', None)
        unit_name = request.data.get('unit_name', None)
        unit_price = request.data.get('unit_price', None)
        images = request.data.get('images', None)
        u_id = user.u_id
        try:
            with transaction.atomic():
                dcs_obj = models.DirectCommodStock(
                                                    product_specif_id=product_specif_id,
                                                    dc_id=dc_id,
                                                    product_specif=product_specif,
                                                    stock_quantity=stock_quantity,
                                                    unit_name=unit_name,
                                                    unit_price=unit_price,
                                                    u_id=u_id,
                                                    images=images
                                                )
                dcs_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':"操作失败"})
        return JsonResponse({'code':1,"msg":"操作成功"})
# 编辑库存
class EditDirectCommodStockView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取单条库存信息
        '''
        product_specif_id = request.GET.get('product_specif_id', None)
        re_data = {}
        try:
            ed_obj = models.DirectCommodStock.objects.get(product_specif_id=product_specif_id)
            re_data['code'] = 1
            re_data['msg'] = '成功'
            re_data['data'] = {}
        except Exception as e:
            print(e)
            re_data['code'] = -3
            re_data['msg'] = '获取失败'
            re_data['status'] = '查询不到任何信息'
        return JsonResponse(re_data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑库存信息等
        '''
        user = request.user
        product_specif_id = request.data.get('product_specif_id', None)
        product_specif = request.data.get('product_specif', None)
        stock_quantity = request.data.get('stock_quantity', None)
        unit_name = request.data.get('unit_name', None)
        unit_price = request.data.get('unit_price', None)
        u_id = user.u_id
        adict = {}
        re_data = {}
        if product_specif:
            adict['product_specif'] = product_specif
        if stock_quantity:
            adict['stock_quantity'] = stock_quantity
        if unit_name:
            adict['unit_name'] = unit_name
        if unit_price:
            adict['unit_price'] = unit_price
        try:
            with transaction.atomic():
                models.DirectCommodStock.objects.filter(product_specif_id=product_specif_id).update(**adict)
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110013
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)
# 编辑溯源信息

# 商品上架/下架
class GoodsShelfView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 商品上架/下架
        '''
        id = request.GET.get('id', None)
        begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
        re_data = {}
        print(begin_id,id,'-------')
        try:
            with transaction.atomic():
                if begin_id == 'DC':
                    good_obj = models.DirectCommod.objects.get(dc_id=id)
                if begin_id == 'GC':
                    good_obj = models.OrderableGoods.objects.get(g_id=id)
                a_if = good_obj.is_shelf
                if a_if == 0:
                    good_obj.is_shelf = 1
                    re_data['msg'] = '上架成功'
                if a_if == 1:
                    good_obj.is_shelf = 0
                    re_data['msg'] = '下架成功'
                good_obj.save()
                re_data['code'] = 1
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败' 
        return JsonResponse(re_data)


# 种养合作社、农业公司录入
class AgriculturalEnterpriseEntryView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 农业企业列表
        '''
        try:
            obj_list = models.SupplierMerchantFile.objects.all().values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'系统错误'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(obj_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 录入农业企业
        '''
        user = request.user
        sm_id = 'SM' + str(10000 + int(redis_cli.cache.incr('test001')))
        name = request.data.get('name', None)
        abbreviation = request.data.get('abbreviation', None)
        introduction = request.data.get('introduction', None)
        show_pictures = request.data.getlist('show_pictures', None)
        business_license = request.data.get('business_license', None)

        operators = request.data.get('operators', None)
        operators_mobile = request.data.get('operators_mobile', None)

        address_province = request.data.get('address_province', None)
        address_city = request.data.get('address_city', None)
        address_county = request.data.get('address_county', None)
        address_detailed = request.data.get('address_detailed', None)

        encyclopedia = request.data.get('encyclopedia', None)
        remarks = request.data.get('remarks', None)
        up_user = user.u_id
        re_data = {}
        try:
            with transaction.atomic():
                sm_obj = models.SupplierMerchantFile(
                                                    sm_id=sm_id,
                                                    name=name,
                                                    abbreviation=abbreviation,
                                                    introduction=introduction,
                                                    show_pictures=show_pictures,
                                                    business_license=business_license,
                                                    operators=operators,
                                                    operators_mobile=operators_mobile,
                                                    address_province=address_province,
                                                    address_city=address_city,
                                                    address_county=address_county,
                                                    address_detailed=address_detailed,
                                                    encyclopedia=encyclopedia,
                                                    remarks=remarks,
                                                    up_user=up_user
                                                )
                sm_obj.save()
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)

class AgriculturalEnterpriseEditView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 单个农业企业资料
        '''
        sm_id = request.GET.get('sm_id', None)
        re_data = {}
        try:
            sm_obj = models.SupplierMerchantFile.objects.filter(sm_id=sm_id).values()
            re_data['code'] = 1
            # re_data['data'] = {'sm_id':, 'name':, 'abbreviation':,'introduction':,
            #                 'show_pictures':,'business_license':,'operators':,'operators_mobile':, 
            #                 'address_province':, 'address_city':, 'address_county':, 'address_detailed':,
            #                 'encyclopedia':,'information_verif':,'up_time':, 'up_user':, 
            #                 'remarks':,'sub_method':}
            re_data['data'] = sm_obj
        except Exception as e:
            print(e)
            re_data['code'] = 110012
            re_data['msg'] = '查询失败'
        return JsonResponse(re_data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 农业企业资料编辑
        '''
        user = request.user
        sm_id = request.data.get('sm_id', None)
        name = request.data.get('name', None)
        abbreviation = request.data.get('abbreviation', None)
        introduction = request.data.get('introduction', None)
        show_pictures = request.data.getlist('show_pictures', None)
        business_license = request.data.get('business_license', None)

        operators = request.data.get('operators', None)
        operators_mobile = request.data.get('operators_mobile', None)

        address_province = request.data.get('address_province', None)
        address_city = request.data.get('address_city', None)
        address_county = request.data.get('address_county', None)
        address_detailed = request.data.get('address_detailed', None)

        encyclopedia = request.data.get('encyclopedia', None)
        remarks = request.data.get('remarks', None)
        up_user = user.u_id
        re_data = {}
        adict = {}
        if name:
            adict['name'] = name
        if abbreviation:
            adict['abbreviation'] = abbreviation
        if introduction:
            adict['introduction'] = introduction
        if show_pictures:
            adict['show_pictures'] = show_pictures
        if business_license:
            adict['business_license'] = business_license
        if operators:
            adict['operators'] = operators
        if operators_mobile:
            adict['operators_mobile'] = operators_mobile
        if address_province and address_city and address_county:
            adict['address_province'] = address_province
            adict['address_city'] = address_city
            adict['address_county'] = address_county
        if address_detailed:
            adict['address_detailed'] = address_detailed
        if encyclopedia:
            adict['encyclopedia'] = encyclopedia
        if remarks:
            adict['remarks'] = remarks
        try:
            with transaction.atomic():
                models.SupplierMerchantFile.objects.filter(sm_id=sm_id).update(**adict)
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)

class SupplierMerchantProductEntryView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 农业企业商品列表
        '''
        sm_id = request.GET.get('sm_id', None)
        try:
            obj_list = models.SupplierMerchantProduct.objects.filter(sm_id=sm_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'系统错误'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(obj_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加农业企业产品资料
        '''
        user = request.user
        sm_id = request.data.get('sm_id', None)

        type_no = request.data.get('type_no', None)

        product_name = request.data.get('product_name', None)
        product_scale = request.data.get('product_scale', None)
        product_unit = request.data.get('product_unit', None)
        
        estimated_unit_price = request.data.get('estimated_unit_price', None)

        production_time = request.data.get('production_time', None)
        show_image = request.data.getlist('show_image', None)
        introduction = request.data.get('introduction', None)
        description = request.data.get('description', None)
        up_user = user.u_id
        re_data = {}
        try:
            ty_obj = models.CommodType.objects.get(ct_id=type_no)
        except Exception as e:
            return JsonResponse({'code': -101,'msg':'该商品类型错误'})
        try:
            with transaction.atomic():
                smp_obj = models.SupplierMerchantProduct(
                                                        sm_id=sm_id,
                                                        type_no=type_no,
                                                        type_name=ty_obj.name,
                                                        product_name=product_name,
                                                        product_scale=product_scale,
                                                        product_unit=product_unit,
                                                        estimated_unit_price=estimated_unit_price,
                                                        production_time=production_time,
                                                        show_image=show_image,
                                                        introduction=introduction,
                                                        description=description,
                                                        up_user=up_user
                                                    )
                smp_obj.save()
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)

class SupplierMerchantProductEditView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 农业企业单个商品信息
        '''
        id = request.GET.get('id', None)
        re_data = {}
        try:
            sm_obj = models.SupplierMerchantProduct.objects.filter(id=id).values()
            re_data['code'] = 1
            # re_data['data'] = {'sm_id':, 'name':, 'abbreviation':,'introduction':,
            #                 'show_pictures':,'business_license':,'operators':,'operators_mobile':, 
            #                 'address_province':, 'address_city':, 'address_county':, 'address_detailed':,
            #                 'encyclopedia':,'information_verif':,'up_time':, 'up_user':, 
            #                 'remarks':,'sub_method':}
            re_data['data'] = sm_obj
        except Exception as e:
            print(e)
            re_data['code'] = 110012
            re_data['msg'] = '查询失败'
        return JsonResponse(re_data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑农业企业产品资料
        '''
        user = request.user
        id = request.data.get('id', None)

        type_no = request.data.get('type_no', None)

        product_name = request.data.get('product_name', None)
        product_scale = request.data.get('product_scale', None)
        product_unit = request.data.get('product_unit', None)
        
        estimated_unit_price = request.data.get('estimated_unit_price', None)

        production_time = request.data.get('production_time', None)
        show_image = request.data.getlist('show_image', None)
        introduction = request.data.get('introduction', None)
        description = request.data.get('description', None)
        re_data = {}
        adict = {}

        if type_no:
            try:
                ty_obj = models.CommodType.objects.get(ct_id=type_no)
                adict['type_no'] = type_no
                adict['type_name'] = ty_obj.name
            except Exception as e:
                return JsonResponse({'code': -101,'msg':'该商品类型错误'})
            
        if product_name:
            adict['product_name'] = product_name
        if product_scale:
            adict['product_scale'] = product_scale
        if product_unit:
            adict['product_unit'] = product_unit
        if estimated_unit_price:
            adict['estimated_unit_price'] = estimated_unit_price
        if production_time:
            adict['production_time'] = production_time
        if show_image:
            adict['show_image'] = show_image
        if introduction:
            adict['introduction'] = introduction
        if description:
            adict['description'] = description
        try:
            with transaction.atomic():
                models.SupplierMerchantProduct.objects.filter(id=id).update(**adict)
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)


