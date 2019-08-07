from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db import transaction
from django import views

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
import threading
import json
import time
import hashlib
import requests
import hmac
from django.core.cache import cache

from apps.admin_operation import models
from utils import redis_cli
from utils.token import authenticated,debug1

# Create your views here.


# 审核操作
class ReviewOperateView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取待审核列表
        '''
        user = request.user
        review_type = request.GET.get('review_type', None)
        task_status = request.GET.get('task_status', 1)
        print(task_status,11111111111111)
        a_dict = {}
        b_dict = {}
        c_dict = {}
        d_dict = {}
        if review_type:
            a_dict['review_type'] = review_type
            b_dict['review_type'] = review_type
            c_dict['review_type'] = review_type
            d_dict['review_type'] = review_type
        a_dict['task_status'] = task_status
        b_dict['task_status'] = 0
        c_dict['task_status'] = 1
        d_dict['task_status'] = 2
        a_dict['task_recipient_num'] = user.u_id
        b_dict['task_recipient_num'] = user.u_id
        c_dict['task_recipient_num'] = user.u_id
        d_dict['task_recipient_num'] = user.u_id
        re_data = {}
        try:
            task_obj = models.AssignedUserReleaseRecordTask.objects.filter(**a_dict).values()
            print(task_obj,'-------------------')
            task_0_count = models.AssignedUserReleaseRecordTask.objects.filter(**b_dict).count()
            task_1_count = models.AssignedUserReleaseRecordTask.objects.filter(**c_dict).count()
            task_2_count = models.AssignedUserReleaseRecordTask.objects.filter(**d_dict).count()
        except Exception as e:
            print(e)
            re_data['code'] = -1
            re_data['msg'] = '获取出错，请联系管理员'
            return JsonResponse(re_data)
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(task_obj, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {'code':1,"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list,'task_0_count':task_0_count,'task_1_count':task_1_count,'task_2_count':task_2_count}
        return Response(data)

    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 审核操作
        '''
        user = request.user
        review_num = request.data.get('review_num', None)
        review_status = request.data.get('review_status', None)
        review_instructions = request.data.get('review_instructions', '') 
        remarks = request.data.get('remarks', None)
        begin_id = ''.join(re.findall(r'[A-Za-z]', str(review_num))) 
        re_data = {}
        if review_status == 0:
            assert review_instructions,110025
        print(11)
        print(begin_id)
        try:
            with transaction.atomic():
                aobj = models.AssignedUserReleaseRecordTask.objects.get(task_object_number=review_num)
                assert aobj.task_recipient_num == str(user.u_id),-102
                print(22)
                if begin_id == 'UG':
                    # Dynamic,UserGraphic,Comment (1,'图文'),(2,'动态'),(3,'评论')
                    review_type = 1
                    review_obj = models.UserGraphic.objects.filter(graphic_id=review_num,)
                if begin_id == 'UD':
                    review_type = 2
                    review_obj = models.Dynamic.objects.filter(dynamic_id=review_num)
                    
                if begin_id == 'GCOM':
                    review_type = 3
                    review_obj = models.Comment.objects.filter(comment_id=review_num)
                up_dict = {'audit_situation': review_status,'audit_user_id': user.u_id,'audit_time': datetime.datetime.now(),'audit_description': review_instructions}
                print(review_type,'------------------------------')
                ro_obj = models.UserReleaseRecord(
                                                review_num=review_num,
                                                review_status=review_status,
                                                review_type=review_type,
                                                review_instructions=review_instructions,
                                                remarks=remarks,
                                                review_admin_id=user.u_id
                                            )
                
                aobj.task_status = 2
                aobj.save()
                review_obj.update(**up_dict)
                ro_obj.save()
                re_data['code'] = 1
                re_data['msg'] = '操作成功'
        except Exception as e:
            print(e)
            re_data['code'] = 110018
            re_data['msg'] = '操作失败'
        return JsonResponse(re_data)

        
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 领取审核任务
class AuditTaskCollectionView(APIView):
    # threads = []
    def get_alist(self,slist):
        alist = []
        d_obj = models.Dynamic.objects.filter(audit_situation=2).exclude(dynamic_id__in=slist).values('dynamic_id','up_time')
        for d_one in d_obj:
            adict = {}
            adict['r_id'] = d_one['dynamic_id']
            adict['up_time'] = d_one['up_time']
            alist.append(adict)
        return alist

    def get_blist(self,slist):
        blist = []
        ug_obj = models.UserGraphic.objects.filter(audit_situation=2).exclude(graphic_id__in=slist).values('graphic_id','up_time')
        for ug_one in ug_obj:
            adict = {}
            adict['r_id'] = ug_one['graphic_id']
            adict['up_time'] = ug_one['up_time']
            blist.append(adict)
        return blist

    def get_clist(self,slist):
        clist = []
        c_obj = models.Comment.objects.filter(audit_situation=2).exclude(comment_id__in=slist).values('comment_id','up_time')
        for c_one in c_obj:
            adict = {}
            adict['r_id'] = c_one['comment_id']
            adict['up_time'] = c_one['up_time']
            clist.append(adict)
        return clist
    # def my_thread1(self,slist):
    #     t = MyThread(self.get_alist, (slist,), self.get_alist.__name__)
    #     self.threads.append(t)
    # def my_thread2(self,slist):
    #     t = MyThread(self.get_blist, (slist,), self.get_blist.__name__)
    #     self.threads.append(t)
    # def my_thread3(self,slist):
    #     t = MyThread(self.get_clist, (slist,), self.get_clist.__name__)
    #     self.threads.append(t)
    def get_result(self,slist):
        # ----------------
        # threads1 = []
        # # start_time = time.time() 
        # t1 = threading.Thread(target=self.my_thread1, args=(slist,))
        # threads1.append(t1)
        # t2 = threading.Thread(target=self.my_thread2, args=(slist,))
        # threads1.append(t2)
        # t3 = threading.Thread(target=self.my_thread3, args=(slist,))
        # threads1.append(t3)
        
        # print(threads1,'-----------411---------')
        # a = 0
        # for s in threads1:
            
        #     s.start()
            
        # for s in threads1:
        #     start_time = time.time() 
        #     s.join()
        #     a = a + 1
        #     end_time = time.time()
        #     print(str(a) + '开始时间: %s' % start_time)
        #     print(str(a) + '结束时间: %s' % end_time) #最后的结束时间
        #     print(str(a) + "总共耗时:{0:.5f}秒".format(end_time - start_time))  # 格式输出耗时
        # end_time = time.time()
        # print('开始时间: %s' % start_time)
        # print('结束时间: %s' % end_time) #最后的结束时间
        # print("总共耗时:{0:.5f}秒".format(end_time - start_time))  # 格式输出耗时
        # -----------------
        
        threads = []  # 定义一个线程池
        t = MyThread(self.get_alist, (slist,), self.get_alist.__name__)
        threads.append(t)

        t1 = MyThread(self.get_blist, (slist,), self.get_alist.__name__)
        threads.append(t1)

        t2 = MyThread(self.get_clist, (slist,), self.get_alist.__name__)
        threads.append(t2)
        
        
        for n in threads:
            
            n.start()
            # end_time = time.time()
            # print(str(a) + '开始时间: %s' % start_time)
            # print(str(a) + '结束时间: %s' % end_time) #最后的结束时间
            # print(str(a) + "总共耗时:{0:.5f}秒".format(end_time - start_time))  # 格式输出耗时
        # t.start()
        # t1.start()
        # t2.start()
        print(-2)
        for n in threads:
            
            n.join()
        b = threads[0].get_result()
        c = threads[1].get_result()
        d = threads[2].get_result()
        # print('b:',b[:10])
        # print('c:',c[:10])
        # print('d:',d[:10])
        elist = b + c + d
        elist.sort(key=lambda x: x["up_time"],reverse=False)
        return elist
    
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 任务领取
        '''
        # 查出所有待审核的记录
        user = request.user
        alist = []
        # adict = {}
        task_id = 'TASK' + str(1000000 + int(redis_cli.cache.incr('test111002')))
        re_data = {}
        yu_obj = models.AssignedUserReleaseRecordTask.objects.all()
        slist = []
        for yu in yu_obj:
            slist.append(yu.task_object_number)
        
        try:
            with transaction.atomic():
                # Dynamic,UserGraphic,Comment (1,'图文'),(2,'动态'),(3,'评论')
                # d_obj = models.Dynamic.objects.filter(audit_situation=2).exclude(dynamic_id__in=slist) 
                # for d_one in d_obj:
                #     adict = {}
                #     adict = {'r_id':d_one.dynamic_id,'up_time':d_one.up_time}
                #     # adict['r_id'] = d_one.dynamic_id
                #     # adict['up_time'] = d_one.up_time
                #     alist.append(adict)
                # print(alist[:10])
                # ug_obj = models.UserGraphic.objects.filter(audit_situation=2).exclude(graphic_id__in=slist) 
                # for ug_one in ug_obj:
                #     adict = {}
                #     adict['r_id'] = ug_one.graphic_id
                #     adict['up_time'] = ug_one.up_time
                #     alist.append(adict)
                # c_obj = models.Comment.objects.filter(audit_situation=2).exclude(comment_id__in=slist) 
                # for c_one in c_obj:
                #     adict = {}
                #     adict['r_id'] = c_one.comment_id
                #     adict['up_time'] = c_one.up_time
                #     alist.append(adict)
                # alist.sort(key=lambda x: x["up_time"],reverse=False)
                # 查出所有超时未解决的任务
                # 装饰器验证用户的领取资格
                alist = self.get_result(slist)
                blist = alist[:10]
                # print(blist)
                clist = []
                for i in blist:
                    begin_id = ''.join(re.findall(r'[A-Za-z]', str(i['r_id'])))  
                    if begin_id == 'UG':
                        # Dynamic,UserGraphic,Comment (1,'图文'),(2,'动态'),(3,'评论')
                        review_type = 1
                    if begin_id == 'UD':
                        review_type = 2
                    if begin_id == 'GCOM':
                        review_type = 3
                    aobj = models.AssignedUserReleaseRecordTask(task_id=task_id,task_object_number=i['r_id'],task_recipient_num=user.u_id,review_type=review_type)
                    clist.append(aobj)
                print(clist,'----------')
                n = len(clist)
                models.AssignedUserReleaseRecordTask.objects.bulk_create(clist,n)
                re_data['code'] = 1
                re_data['msg'] = "操作成功，已领取" + str(n) + "条任务，请在30分钟内完成任务"
        except Exception as e:
            print(e)
            re_data['code'] = -1
            re_data['msg'] = "任务领取失败，请重新操作或联系管理员"
        return JsonResponse(re_data)


# 人脸核身
def get_sign():
    api_key = "6n5LKRbuFzG8l9NZ-KUdx4CqXx464PgT"
    api_secret = "CK9vkhlCkZ7bHzuvEEVH0EnB_oB3fm4h"
    valid_durtion = 10000
    current_time = int(time.time())
    expire_time = current_time + valid_durtion
    rdm = ''.join(random.choice("0123456789") for i in range(10))
    raw1 = "a={}&b={}&c={}&d={}".format(api_key, expire_time, current_time, rdm)
    # raw = "a=ICVvC_xUs6177WEtyUNwIH8J6NfGu50t&b=1530762218&c=1530762118&d=0799687066"
    raw = bytes(raw1, encoding = "utf8")  
    api_secret = bytes(api_secret, encoding = "utf8")
    sign_tmp = hmac.new(api_secret, raw, hashlib.sha1).digest()
    sign = base64.b64encode(sign_tmp + raw)
    return sign


class PeopleFace(APIView):
    def get(self,request,*args,**kwargs):
        data = {'sign':get_sign(),'sign_version':'hmac_sha1','return_url':'http://94.191.125.82','notify_url':'http://94.191.125.82/wangtian_backend/api/v1/release_review/ph_face/',
            'comparison_type':1,'group':1,'liveness_type':'video_number'}
        mepost=requests.post("https://openapi.faceid.com/lite/v1/get_biz_token",json=data)
        url_join = mepost.json()
        url = 'https://openapi.faceid.com/lite/v1/do/' + str(url_join['biz_token'])
        print(url,'----------------')
        print(url_join,'-----------------------')
        # return render(request,'test1.html',{'url':url})
        return JsonResponse({'code':1,'url':url})


class IndesShowTest(APIView):
    def get(self,request,*args,**kwargs):
        return render(request,"a1.html")

        
class PhedFace(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data.get('data', None)
        gk_data = json.loads(data)
        print(gk_data,111111)
        return JsonResponse({'code':1,'msg':'migin','gk_data':gk_data})