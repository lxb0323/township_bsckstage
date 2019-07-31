from django.http import JsonResponse,HttpResponse
from django.utils.deprecation import MiddlewareMixin
import json

class BlockedIpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.data)
        # print(request.user.id,55555555555555555555555555555555555555555555555555555555555)
        print(request.path_info,'--------------1--------------')
        print(type(request.path_info),'-------------111-------------')
        # if request.user.id is None and request.path_info == '/api/v1/admin/yanzhengma/' :
        #     return True

        # if request.user.id is None and request.path_info != '/api/v1/admin/yanzhengma/' and request.path_info != '/api/v1/login/':
        #     return JsonResponse({'code':4003,'msg':"请登录"})
        # if request.user.id is None:
        #     if request.path_info == '/api/v1/admin/yanzhengma/':
        #         return None
        #     if request.path_info == '/api/v1/login/':
        #         return None
        #     else:
        #         return JsonResponse({'code':4003,'msg':"请登录"})
        # if request.path_info == '/api/v1/login/':
        #     return None
        # if request.path_info == '/api/v1/admin/yanzhengma/':
        #     return None
        
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        如果有返回值，则不在继续执行，直接到最后一个中间件的response
        """
        print('m1.process_view:', callback)
    def process_exception(self, request, exception):
        print(str(exception),78878888888888888888888)
        if str(exception) == '110055':
            return JsonResponse({"code":110055,"msg":"操作成功！"})
    #     if str(exception) == '1001':
    #         return JsonResponse({"code":1001,"msg":"没有权限"})
    #     if str(exception) == '1002':
    #         return JsonResponse({"code":1002,"msg":"当前用户已禁用，无法进行操作"})  
    #     if str(exception) == '1003':
    #         return JsonResponse({"code":1003,"msg":"当前用户已删除，无法进行操作"})
    #     if str(exception) == '1004':
    #         return JsonResponse({"code":1004,"msg":"当前用户电话号码已存在"})
    #     if str(exception) == '1005':
    #         return JsonResponse({"code":1005,"msg":"非超级管理员没有此权限"})
    #     if str(exception) == '1006':
    #         return JsonResponse({"code":1006,"msg":"必填字段未填写"})
    #     if str(exception) == '1007':
    #         return JsonResponse({"code":1007,"msg":"此处不支持修改自己的密码"})
    #     if str(exception) == '1008':
    #         return JsonResponse({"code":1008,"msg":"作为商家管理员您只能添加自己商户的管理员"})
    #     if str(exception) == '1009':
    #         return JsonResponse({"code":1009,"msg":"作为渠道管理员您只能添加所管理商户的管理员"})
    #     if str(exception) == '1010':
    #         return JsonResponse({"code":1010,"msg":"该管理员已禁用或删除，无法进行密码修改"})

    #     # -------------------------------------------系统处理错误码
    #     if str(exception) == '4005':
    #         return JsonResponse({"code":4005,"msg":"查询商家不存在"})
    #     if str(exception) == '4006':
    #         return JsonResponse({"code":4006,"msg":"操作失败"})
    #     if str(exception) == '4007':
    #         return JsonResponse({"code":4007,"msg":"必填字段未填"})
        
    #     if str(exception) == '5000':
    #         return JsonResponse({"code":5000,"msg":"服务器故障，请联系维护人员"})
    #     if str(exception) == '5001':
    #         return JsonResponse({"code":5001,"msg":"查询数据不存在"})
    #     if str(exception) == '5002':
    #         return JsonResponse({"code":5002,"msg":"时间格式错误"})
    #     if str(exception) == '5003':
    #         return JsonResponse({"code":5003,"msg":"数据创建失败"})
    #     if str(exception) == '5004':
    #         return JsonResponse({"code":5004,"msg":"管理员个人信息不完善，请先完善个人信息"})

    #     # -------------------------------------------业务错误码
    #     if str(exception) == '110002':
    #         return JsonResponse({"code":110002,"msg":"手机号不能为空"})
    #     if str(exception) == '110003':
    #         return JsonResponse({"code":110003,"msg":"验证码错误"})
    #     if str(exception) == '110004':
    #         return JsonResponse({"code":110004,"msg":"注册失败"})
    #     if str(exception) == '110005':
    #         return JsonResponse({"code":110005,"msg":"管理员类型为必填"})
    #     if str(exception) == '110006':
    #         return JsonResponse({"code":110006,"msg":"银行管理员无法创建信条内部管理员"})
    #     if str(exception) == '110007':
    #         return JsonResponse({"code":110007,"msg":"创建银行管理员时需要填入所属银行"})
    #     if str(exception) == '110008':
    #         return JsonResponse({"code":110008,"msg":"渠道商管理员添加商家管理员时，商家编号和商家名不为空"})
    #     if str(exception) == '110009':
    #         return JsonResponse({"code":110009,"msg":"管理员创建失败"})
    #     if str(exception) == '110012':
    #         return JsonResponse({"code":110012,"msg":"请选择要操作的管理员"})
    #     if str(exception) == '110013':
    #         return JsonResponse({"code":110013,"msg":"所选管理员不存在"})
    #     if str(exception) == '110014':
    #         return JsonResponse({"code":110014,"msg":"两次输入密码不一致"})
    #     if str(exception) == '110015':
    #         return JsonResponse({"code":110015,"msg":"该商户已经进件，如需修改资料请点击修改"})
    #     if str(exception) == '110016':
    #         return JsonResponse({"code":110016,"msg":"商户资料注册人电话不为空"})
    #     if str(exception) == '110017':
    #         return JsonResponse({"code":110017,"msg":"该手机号未注册，无法进行进一步操作"})
        
    #     else:
    #         return None

    def process_response(self, request, response):
        print("中间件2返回：",json.loads(response.content))
        # print(request.user.u_id)
        print(type(response),'---------------------')
        return response
