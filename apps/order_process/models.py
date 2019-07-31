from django.db import models

# Create your models here.
# '''
#     |-- 自动编号（order_id, 自增长主键）
#     |-- 订单单号（order_no, 唯一值，供客户查询）
#     |-- 商店编号（shop_id, 商店表自动编号）
#     |-- 订单状态 (order_status,未付款,已付款,已发货,已签收,退货申请,退货中,已退货,取消交易)
#     |-- 商品数量 (product_count, 商品项目数量，不是商品)
#     |-- 商品总价 (product_amount_total)
#     |-- 订单金额 (order_amount_total，实际付款金额)
#     |-- 运费金额 (logistics_fee)
#     |-- 是否开箱验货 (is_unpacking_inspection)
#     |-- 是否开票（是否开具发票）
#     |-- 发票编号 (订单发票表自动编号)
#     |-- 收货地址编号 (address_id, 收货地址表自动编号)
#     |-- 订单物流编号 (orderlogistics_id, 订单物流表自动编号)
#     |-- 订单支付渠道 (pay_channel)
#     |-- 订单支付单号 (out_trade_no/escrow_trade_no,第三方支付流水号)
#     |-- 创建时间 (下单时间)
#     |-- 付款时间
#     |-- 发货时间
#     |-- 客户编号 (user_id，用户表自动编号)
#     |-- 客户备注
#     |-- 订单结算状态 (order_settlement_status，货到付款、分期付款会用到)
#     |-- 订单结算时间 (order_settlement_time)
# '''

# class Order(models.Model):
#     order_no = models.CharField(max_length=64,unquire=True,verbose_name='订单单号')
#     shop_type_choice = ((1,'平台自营'),(2,'商户出售'),(3,'个人交易'))
#     shop_type = models.SmallIntegerField(choices=shop_type_choice,default=1)
#     order_type_choice = ((1,'直购订单'),(2,'求购订单'))
#     order_type = models.SmallIntegerField(choices=order_type,default=1)
#     shop_id = models.CharField(max_length=64,verbose_name='出售方id')
#     product_count = models.BigIntegerField(verbose_name='商品数量')
#     product_amount_total = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='商品总金额')
#     order_amount_total = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='实际付款金额')
#     logistics_fee = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='物流费')
#     orderlogistics_id = models.CharField(max_length=64,verbose_name='物流单号')
#     address_id = models.CharField(max_length=64,verbose_name='收货地址编号')
#     pay_channel_choice = ((0,'余额'),(1,'微信'),(2,'支付宝'),(3,'线下'))
#     pay_channel = models.SmallIntegerField(choices=pay_channel_choice,default=0,verbose_name='支付渠道')
#     out_trade_no = models.CharField(max_length=64,verbose_name='支付单号')
#     escrow_trade_no = models.CharField(max_length=64,verbose_name='流水号')
#     order_status_choice = ((0,'未付款'),(1,'已付款'),(2,'已发货'),(3,'已签收'),(-1,'退货申请'),(-2,'退货中'),(-3,'已退货'),(-4,'取消交易'))
#     order_status = models.SmallIntegerField(choices=order_status_choice,default=0,verbose_name='订单状态')
#     u_id = models.CharField(max_length=32,verbose_name='用户编号')
#     pay_time = models.DateTimeField(verbose_name='支付时间',auto_now_add=True)
#     delivery_time = models.DateTimeField(verbose_name='发货时间',auto_now_add=True)
#     created_at = models.DateTimeField(verbose_name='下单时间',auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name='修改时间',auto_now_add=True)
#     signing_at =models.DateTimeField(verbose_name='签收时间',auto_now_add=True)
#     waybill_number = models.CharField(max_length=64,verbose_name='运单号')



#     class Meta:
#         db_table = 'order'
#         managed = True
#         verbose_name = '订单表'
#         verbose_name_plural = '订单表'

# class OrderAppraise(models.Model):
#     order_no = models.CharField(max_length=64,unquire=True,verbose_name='订单单号')
#     u_id = models.CharField(max_length=32,verbose_name='用户编号')
#     shop_type_choice = ((1,'平台自营'),(2,'商户出售'),(3,'个人交易'))
#     shop_type = models.SmallIntegerField(choices=shop_type_choice,default=1)
#     shop_id = models.CharField(max_length=64,verbose_name='出售方id')
#     service_comment = models.TextField(verbose_name='服务评价')
#     remarks = models.TextField(default='',verbose_name='备注')
#     class Meta:
#         db_table = 'order_appraise'
#         managed = True
#         verbose_name = '订单评价'
# class ProductReview(models.Model):
#     pr_id = models.CharField(max_length=64,unquire=True,verbose_name='商品评价编号')
#     u_id = models.CharField(max_length=32,verbose_name='用户编号')
#     order_no = models.CharField(max_length=64,verbose_name='订单单号')
#     commodity_no = models.CharField(max_length=64, verbose_name='商品编号')
#     commodity_name = models.CharField(max_length=255,verbose_name='商品名')
#     unit_price = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='单价')
#     quantity = models.BigIntegerField(verbose_name='商品数量')
#     total_price = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='实际总价')
#     content = models.TextField(default='未评价',verbose_name='评价内容')
#     images = models.TextField(default='',verbose_name='图片')
#     video = models.TextField(default='',verbose_name='视频')
#     comment_count = models.BigIntegerField(default=0,verbose_name='评论总量')
#     like_count = models.BigIntegerField(default=0,verbose_name='点赞总量')
#     click_volume = models.BigIntegerField(default=0,verbose_name='点击量')
#     create_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'product_review'
#         managed = True
#         verbose_name = '商品评价'

# class OrderDetail(models.Model):
#     order_no = models.CharField(max_length=64,unquire=True,verbose_name='订单单号')
#     goods_detail = 
#     class Meta:
#         db_table = 'order_detail'
#         managed = True
#         verbose_name = '订单详情'

# class order_auditbiz(models.Model):
#     order_no = models.CharField(max_length=64,unquire=True,verbose_name='订单单号')
#     deal_with_user = models.CharField(max_length=32,verbose_name='处理人编号')

#     class Meta:
#         db_table = 'order_auditbiz'
#         managed = True
#         verbose_name = '订单处理'

# class order_commission(models.Model):
#     order_no = models.CharField(max_length=64,unquire=True,verbose_name='订单单号')
#     shop_type_choice = ((1,'平台自营'),(2,'商户出售'),(3,'个人交易'))
#     shop_type = models.SmallIntegerField(choices=shop_type_choice,default=1))
#     product_amount_total = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='商品总金额')
#     order_amount_total = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='实际收款金额')
#     seller_no = models.CharField(max_length=64,verbose_name='出售方编号')
#     seller_receipt = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='出售方收款金额')
#     seller_transfer_account = 
#     platform_collection = models.DecimalField(max_digits=12,decimal_places=4,verbose_name='平台方收款金额')
#     platform_transfer_account =
#     commission_amount = 
#     settlement_status = 
    
#     class Meta:
#         db_table = 'order_commission'
#         managed = True
#         verbose_name = '订单分润'