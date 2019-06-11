"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from . import views
from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 登入
    url(r'^login/', views.login),
    url(r'^signin/', views.register),
    url(r'^logout/', views.logout),
    url(r'^forgot/', views.getpassword),

    # 首頁
    url(r'^smallschool/', views.home1),

    # 新聞
    # --新聞首頁
    url(r'^get_news/', views.get_news),
    # --新聞文章回傳
    url(r'^outcome/', views.outcome_news),
    # --新聞回傳空白沒資料
    url(r'^news_con/', views.news_con),
    # --新聞查詢小bar
    url(r'^search/', views.search_news),
    url(r'^search_for_keyword/', views.search_news_for_keyword),
    # --新聞查詢 有查日期功能
    url(r'^list/', views.list_page1),
    url(r'^time_search/', views.time_search),

    # 交易資訊
    # --歷史回測
    url(r'^algotrade/', views.algotrade),
    url(r'^algotradef/', views.algotradef),

    # --期貨專區

    # 即時資料
    url(r'^quote/', views.quote),
    url(r'^recent/', views.recent),
    url(r'^quote1/', views.quote1),
    url(r'^recent1/', views.recent1),




    # EDITOR
    url(r'^editor/', views.compiler),
    url(r'^demo/', views.demo),

    # 期貨專區
    url(r'^economic_term/', views.economic_term),

    # 下單機
    url(r'^tech/', views.tech),
    url(r'^tech2/', views.tech2),
    url(r'^tech3/', views.tech3),
    url(r'^tech4/', views.tech4),
    url(r'^tech5/', views.tech5),
    url(r'^tech6/', views.tech6),
    url(r'^tech7/', views.tech7),
    url(r'^tech8/', views.tech8),



    # --討論區
    url(r'^get_article/', views.get_article),
    url(r'^search_discussion/', views.search_discussion),
    url(r'^post/', views.issued),
    url(r'^chat_outcome/', views.content),
    url(r'^reply/', views.reply),
    url(r'^like/', views.like),

    url(r'^post_page_1/', views.post_page_1),
    url(r'^post_page_2/', views.post_page_2),
    url(r'^post_page_3/', views.post_page_3),
    url(r'^post_next/', views.post_next),
    url(r'^post_prev/', views.post_prev),

    # # -- 發文（簡單回傳

    # --討論區搜尋(開不了

    # --新手投資小常識
    url(r'^new_info/', views.new_info),
    url(r'^new_infocon2/', views.new_infocon2),
    url(r'^new_infocon3/', views.new_infocon3),
    url(r'^new_infocon4/', views.new_infocon4),
    url(r'^new_infocon5/', views.new_infocon5),
    url(r'^new_infocon/', views.new_infocon),

    # 會員
    # --會員首頁
    url(r'^member/', views.member),
    url(r'^member2/', views.member2),

    url(r'^mem_home/', views.mem_home),

    # --忘記密碼
    url(r'^mo_pass/', views.modifypassword),
    # --修改基本資料
    url(r'^modify/', views.modify),

    url(r'^mem_future/', views.member_list_del),

    url(r'^mem_sto/', views.member_list_add),
    url(r'^member', views.member),

    url(r'^message/', views.message),
    # url(r'^message1/', views.message1),
    url(r'^email/', views.email),
    url(r'^email2/', views.email2),
    # url(r'^email1/', views.email1),



]
urlpatterns += staticfiles_urlpatterns()