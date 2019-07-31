from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.admin_operation.views import (WROrderableGoodsView,ProductCategoryView,WROrderableGoodsInfoView,WROrderableGoodsGraphicView,
                                        WRDirectCommodView,WRDirectCommodInfoView,WRDirectCommodGraphicView,WRDirectCommodStockView)
from apps.admin_operation import views as ad_v

urlpatterns = [  
    # 添加可订购商品
    url(r'^add_orderable_goods/$',WROrderableGoodsView.as_view()),
    # 添加/查看商品种类
    url(r'^product_category/$',ProductCategoryView.as_view()),
    # 添加可订购商品详情
    url(r'^add_orderable_good_info/$',WROrderableGoodsInfoView.as_view()),
    # 添加可订购商品图文
    url(r'^add_orderable_good_graphic/$',WROrderableGoodsGraphicView.as_view()),
    # 添加直购商品
    url(r'^add_direct_commod/$',WRDirectCommodView.as_view()),
    # 添加直购商品详情
    url(r'^add_direct_commod_info/$',WRDirectCommodInfoView.as_view()),
    # 添加直购商品图文
    url(r'^add_direct_commod_graphic/$',WRDirectCommodGraphicView.as_view()),
    # 添加直购商品库存/获取直购商品列表
    url(r'^add_direct_commod_stock/$',WRDirectCommodStockView.as_view()),
    # 编辑/查看直购商品库存
    url(r'^edit_direct_commod_stock/$',ad_v.EditDirectCommodStockView.as_view()),
    # 商品上架/下架
    url(r'^good_shelf/$',ad_v.GoodsShelfView.as_view()),
    # 农业公司录入/获取农业公司列表
    url(r'^agricultural_enterprise_entry/$',ad_v.AgriculturalEnterpriseEntryView.as_view()),
    # 农业公司资料编辑/获取单个农业公司资料
    url(r'^agricultural_enterprise_edit/$',ad_v.AgriculturalEnterpriseEditView.as_view()),
    # 农业公司产品资料添加/获取单个农业公司产品列表
    url(r'^supplier_merchant_product_entry/$',ad_v.SupplierMerchantProductEntryView.as_view()),
    # 农业公司产品资料编辑/获取单个农业公司单个产品资料
    url(r'^supplier_merchant_product_edit/$',ad_v.SupplierMerchantProductEditView.as_view()),
    # 用户登录
    url(r'^login/$',ad_v.LoginView.as_view()),
    # 发送/验证短信验证码
    url(r'^send_sms/$',ad_v.SendVerificationCode.as_view()),
]
