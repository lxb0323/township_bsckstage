from django.db import models
import ast

# 自定义一个ListFiled,继承与TextField这个类
class ListFiled(models.TextField):
    description = "just a listfiled"

    # 继承TextField
    def __init__(self, *args, **kwargs):
        super(ListFiled, self).__init__(*args, **kwargs)
    # 读取数据库的时候调用这个方法
    def from_db_value(self, value, expression, conn, context):
        # print('from_db_value')
        if not value:
            value = []
        if isinstance(value, list):
            return value
        # print('value type ', type(value))
        # 直接将字符串转换成python内置的list
        return ast.literal_eval(value)

    # 保存数据库的时候调用这个方法
    def get_prep_value(self, value):
        # print("get_prep_value")
        if not value:
            return value
        # print('value type ', type(value))
        return str(value)
