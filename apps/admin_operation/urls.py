from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.admin_operation.views import (WROrderableGoodsView,ProductCategoryView,WROrderableGoodsInfoView,WROrderableGoodsGraphicView,
                                        WRDirectCommodView,WRDirectCommodInfoView,WRDirectCommodGraphicView,WRDirectCommodStockView)
from apps.admin_operation import views as ad_v

urlpatterns = [  
    # ��ӿɶ�����Ʒ
    url(r'^add_orderable_goods/$',WROrderableGoodsView.as_view()),
    # ���/�鿴��Ʒ����
    url(r'^product_category/$',ProductCategoryView.as_view()),
    # ��ӿɶ�����Ʒ����
    url(r'^add_orderable_good_info/$',WROrderableGoodsInfoView.as_view()),
    # ��ӿɶ�����Ʒͼ��
    url(r'^add_orderable_good_graphic/$',WROrderableGoodsGraphicView.as_view()),
    # ���ֱ����Ʒ
    url(r'^add_direct_commod/$',WRDirectCommodView.as_view()),
    # ���ֱ����Ʒ����
    url(r'^add_direct_commod_info/$',WRDirectCommodInfoView.as_view()),
    # ���ֱ����Ʒͼ��
    url(r'^add_direct_commod_graphic/$',WRDirectCommodGraphicView.as_view()),
    # ���ֱ����Ʒ���/��ȡֱ����Ʒ�б�
    url(r'^add_direct_commod_stock/$',WRDirectCommodStockView.as_view()),
    # �༭/�鿴ֱ����Ʒ���
    url(r'^edit_direct_commod_stock/$',ad_v.EditDirectCommodStockView.as_view()),
    # ��Ʒ�ϼ�/�¼�
    url(r'^good_shelf/$',ad_v.GoodsShelfView.as_view()),
    # ũҵ��˾¼��/��ȡũҵ��˾�б�
    url(r'^agricultural_enterprise_entry/$',ad_v.AgriculturalEnterpriseEntryView.as_view()),
    # ũҵ��˾���ϱ༭/��ȡ����ũҵ��˾����
    url(r'^agricultural_enterprise_edit/$',ad_v.AgriculturalEnterpriseEditView.as_view()),
    # ũҵ��˾��Ʒ�������/��ȡ����ũҵ��˾��Ʒ�б�
    url(r'^supplier_merchant_product_entry/$',ad_v.SupplierMerchantProductEntryView.as_view()),
    # ũҵ��˾��Ʒ���ϱ༭/��ȡ����ũҵ��˾������Ʒ����
    url(r'^supplier_merchant_product_edit/$',ad_v.SupplierMerchantProductEditView.as_view()),
    # �û���¼
    url(r'^login/$',ad_v.LoginView.as_view()),
    # ����/��֤������֤��
    url(r'^send_sms/$',ad_v.SendVerificationCode.as_view()),
]
