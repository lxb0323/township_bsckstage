from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from apps.release_review import views as re_v

urlpatterns = [  
    # 获取任务首页
    url(r'^task_index/$',re_v.ReviewOperateView.as_view()),
    # 领取任务
    url(r'^recieve_the_task/$',re_v.AuditTaskCollectionView.as_view()),
    url(r'^get_ak/$',re_v.PeopleFace.as_view()),
    url(r'^index/$', re_v.IndesShowTest.as_view()),
    url(r'^ph_face/$',re_v.PhedFace.as_view()),
]
