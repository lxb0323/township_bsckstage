from django.http import JsonResponse,HttpResponse
import functools
import jwt
from apps.admin_operation.models import Users
import json
 
 
def authenticated(method):
    # print("开始获取jwt_token")
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        
        # jwt_token = self.request.headers.get('jwt_token', None)
        jwt_token = self.request.META.get('HTTP_AUTHORIZATION') 
        print(jwt_token,222222222222222222222222)
        # url = self.get_login_url()
        if jwt_token is not None:
            try:
                print(1)
                token = jwt.decode(jwt_token, "12345", algorithm='HS256')
                print(2)
                print(token)
                #取出用户
                try:
                    user = Users.objects.get(mobile=token["mobile"])
                    print("验证user")
                    print(user)
                    # 一定要设置_current_user = user ,并且注意前面有下划线
                    self.request.user = user
                    print(1212)
                    return method(self, *args, **kwargs)
                except Exception as e:
                    print(e,233)
                    # self.write(json.dumps({"msg":"跳转"},ensure_ascii=False))
                    return method(self, *args, **kwargs)
                    # return JsonResponse({"msg":"跳转2"})
                    # return wrapper
 
            except Exception as e: # jwt.ExpiredSignatureError
                # self.set_status(401)
                # self.redirect(url)
                print(str(e),23232311111111111111111111111111111111111)
                if str(e) == 'Signature verification failed':
                    return JsonResponse({"code":1105,"msg":"签名验证失败"})  
                # self.write(json.dumps({"msg":"验证失败"},ensure_ascii=False))
                if str(e) == 'Signature has expired':
                    return JsonResponse({"code":1104,"msg":"签名已过期，请重新登录！"})   
                # return JsonResponse({"code":1106,"msg":"签名验证错误，请检查"})    
                return method(self, *args, **kwargs)
        else:
            # self.set_status(401)
            # print("验证不成功")
            # self.redirect(url)
            # self.write(json.dumps({"msg":"跳转"},ensure_ascii=False))
            return JsonResponse({"msg":"跳转1"})
        # self.finsh()
            # raise HTTPError(403)
    return wrapper

# def debug1(method):
#     @functools.wraps(method)
#     def wrapper(self, *args, **kwargs):
#         print("[DEBUG]: enter {}()".format(self.request.user.mobile))
#         return method(self, *args, **kwargs)
#     return wrapper
def debug1(func):
    def wrapper(self, *args, **kwargs):
        print("[DEBUG]: enter {}()".format(self.request))
        print("你说的是些个什么？？")
        configfile = self.request.user
        # f = open(configfile, 'r')
        # configstr = f.read().replace('\\', '\\\\')
        # configtmp = json.loads(configstr)
        # config = {k: v.replace('\\\\', '\\') for k, v in configtmp.items()}
        print(configfile.u_id)
        return func(self, *args, **kwargs)
    return wrapper

def authenticated_two(method):
    # print("开始获取jwt_token")
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        
        # jwt_token = self.request.headers.get('jwt_token', None)
        jwt_token = self.request.META.get('HTTP_AUTHORIZATION') 
        # print(jwt_token,222222222222222222222222)
        # url = self.get_login_url()
        if jwt_token is not None:
            try:
                token = jwt.decode(jwt_token, "12345", algorithm='HS256')
                print(token)
                #取出用户
                try:
                    user = Users.objects.get(mobile=token["mobile"])
                    # print("验证user")
                    print(user)
                    # 一定要设置_current_user = user ,并且注意前面有下划线
                    self.request.user = user
                    print(1212)
                    return method(self, *args, **kwargs)
                except Exception as e:
                    print(e,233)
                    # self.write(json.dumps({"msg":"跳转"},ensure_ascii=False))
                    return JsonResponse({"msg":"跳转2"})
 
            except Exception as e: # jwt.ExpiredSignatureError
                # self.set_status(401)
                # self.redirect(url)
                print(str(e),23232311111111111111111111111111111111111)
                if str(e) == 'Signature verification failed':
                    return JsonResponse({"code":1105,"msg":"签名验证失败"})  
                # self.write(json.dumps({"msg":"验证失败"},ensure_ascii=False))
                if str(e) == 'Signature has expired':
                    return JsonResponse({"code":1104,"msg":"签名已过期，请重新登录！"})   
                return JsonResponse({"code":1106,"msg":"签名验证错误，请检查"})      
        else:
            # self.set_status(401)
            # print("验证不成功")
            # self.redirect(url)
            # self.write(json.dumps({"msg":"跳转"},ensure_ascii=False))
            # return JsonResponse({"msg":"跳转1"})
            try:
                # print("验证user")
                user = 'visitor'
                # 一定要设置_current_user = user ,并且注意前面有下划线
                self.request.user = user
                return method(self, *args, **kwargs)
            except Exception as e:
                print(e,233)
                # self.write(json.dumps({"msg":"跳转"},ensure_ascii=False))
                return JsonResponse({"msg":"跳转2"})
        # self.finsh()
            # raise HTTPError(403)
    return wrapper