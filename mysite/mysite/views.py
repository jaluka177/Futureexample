from django.shortcuts import render, render_to_response, HttpResponseRedirect, redirect, HttpResponse
from django.shortcuts import get_object_or_404

from .models import FutureMember, FutureYahooNew, FutureCna, FutureYahooHot, FutureYahooStock, FutureYahooTec, \
    FutureYahooTra, \
    FutureYahoo, FutureTransactionInfo, \
    FutureTrackFuture, FutureCategory, FutureYahooTendency, FutureTechnologyIndex2, FutureTechnologyIndex, \
    FutureRatio4Q, FutureRatio3Q, FutureRatio2Q, FutureRatio1Q, FutureRatio1, FutureRatio4, \
    FutureEconomic, FutureDiscuss, FutureComment, FutureInformation, \
    FutureDividendPolicy, FutureBalancesheetQ, FutureBalancesheet, \
    FutureCashFlows, FutureCashFlowsQ, FutureIncomeStatementQ, FuturePe, FutureStockList, Compiler, \
    FuturesQuote, Com, FutureType, FutureYahooGlobal, FuturesQuote1

from . import views
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template import loader
import simplejson
import numpy as np

# import datetime
from datetime import datetime, date

# from yahoo_finance import Share
from datetime import date
import random

from bs4 import BeautifulSoup

import urllib.request
import pymysql

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 登入

def login(request):  # 登入功能
    status_m = False
    status_p = False
    back = request.GET.get('back', 0)
    article_id = request.GET.get('article_id', 0)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        check_m = FutureMember.objects.filter(email__exact=username)
        check_p = FutureMember.objects.filter(password__exact=password)

        if check_m is not None:
            status_m = True
        if check_p is not None:
            status_p = True

        user = FutureMember.objects.filter(email=username, password=password)

        if user and status_m is True and status_p is True:
            request.session['userName'] = user[0].email
            request.session['password'] = user[0].password
            request.session['name'] = user[0].member_name
            if back == '0' or back == '':
                return HttpResponseRedirect('/smallschool/')
            elif back == '討論區發文':
                return HttpResponseRedirect('/post/')
            elif back == '討論區回覆':
                return HttpResponseRedirect('/chat_outcome/?id=' + article_id)
            elif back == '期貨專區':
                return HttpResponseRedirect('/economic_term/')
            elif back == '修改基本資料':
                return HttpResponseRedirect('/modify/')
            elif back == '修改密碼':
                return HttpResponseRedirect('/mo_pass/')
            elif back == '新聞首頁':
                return HttpResponseRedirect('/get_news/')
            elif back == '會員回測':
                return HttpResponseRedirect('/algotradef/')
            elif back == '系統首頁':
                return HttpResponseRedirect('/smallschool/')
            elif back == '下單機':
                return HttpResponseRedirect('/tech/')
            elif back == '會員頁面':
                return HttpResponseRedirect('/member/')
        else:
            return render_to_response('login.html', {'status_m': status_m, 'status_p': status_p})

    return render_to_response('login.html', {'back': back, 'article_id': article_id})


def logout(request):  # 登出
    try:
        del request.session['userName']
        del request.session['password']
        del request.session['name']
        del request.session['post_page']
    except:
        pass
    return HttpResponseRedirect('/smallschool/')


def register(request):
    status_m = True
    status_p = True
    status_check_password = True

    if request.method == 'POST':
        check_mail = request.POST.get('mail', '')
        check_password = request.POST.get('password', '')

        check_m = FutureMember.objects.filter(email__exact=check_mail)
        check_p = FutureMember.objects.filter(password__exact=check_password)

        if check_m:  # 如果回傳陣列是空的
            status_m = False
        if check_p:  # 如果回傳陣列是空的
            status_p = False

        p1 = request.POST.get('password', '')
        p2 = request.POST.get('password_check', '')

        if p1 == p2:  # !=改成is not
            status_check_password = True
        else:
            status_check_password = False

        name = request.POST.get('name', '')
        email = request.POST.get('mail', '')
        password = request.POST.get('password', '')
        phone = request.POST.get('tel', '')

        if status_m is True and status_p is True and status_check_password is True:

            FutureMember.objects.create(email=email, password=password, phone_num=phone, type='1', member_name=name)
            return HttpResponseRedirect('/login/')
        else:
            return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p,
                                                      'status_check-password': status_check_password, 'name': name,
                                                      'mail': email, 'password': password, 'tel': phone})

    return render_to_response('signin.html', {'status_m': status_m, 'status_p': status_p,
                                              'status_check_password': status_check_password})


def getpassword(request):
    if request.method == 'POST':
        mail = request.POST.get('mail', '')
        check_mail = FutureMember.objects.filter(email=mail)

        if check_mail is not None:
            new_password = random.randint(10000, 100000)
            new_password = str(new_password)
            send_mail('Your New Password', new_password, 'jaluka177@gmail.com', [mail, ], fail_silently=False)
            check_mail.update(password=new_password)
            return render_to_response('login.html')
        else:
            status_m = False
            return render_to_response('forgot.html', {'warn': status_m})

    return render_to_response('forgot.html')


# 會員

def member(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('member2.html', {'name': name, 'loginstatus': loginstatus})


def member2(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('member3.html', {'name': name, 'loginstatus': loginstatus})


def mem_home(request):  # check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('member2.html', {'loginstatus': loginstatus, 'name': name})


# member 會員選股清單  新增

def member_list_add(request):
    try:
        member_name = request.session['name']
    except KeyError:
        return render_to_response('login.html')
    # member = '1'
    member = FutureMember.objects.get(member_name=member_name).member_id
    # if '新增'
    if request.method == 'POST':
        list_id = request.POST.get('add', 0)
        list_now = FutureStockList.objects.filter(member_id=member, list_id=list_id)
        check_list = []
        total_list = []
        total_list_id = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14',
                         't15', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28',
                         't29', 't30', 't31']
        v1_list = []
        v2_list = []

        check_list.append(request.POST.get('checkbox1', '0'))
        value1 = request.POST.get('s1', 0)
        value1_1 = request.POST.get('s1_1', 0)
        v1_list.append(value1)
        v2_list.append(value1_1)
        total_list.append("短期MA線" + str(value1) + "中長期MA線")

        check_list.append(request.POST.get('checkbox2', '0'))
        value2 = request.POST.get('s2', 0)
        value2_1 = request.POST.get('s2_1', 0)
        v1_list.append(value2)
        v2_list.append(value2_1)
        total_list.append("MACD" + str(value2) + "穿越零軸")

        check_list.append(request.POST.get('checkbox3', '0'))
        value3 = request.POST.get('s3', 0)
        value3_1 = request.POST.get('s3_1', 0)
        v1_list.append(value3)
        v2_list.append(value3_1)
        total_list.append("RSI值" + str(value3) + str(value3_1))

        check_list.append(request.POST.get('checkbox4', '0'))
        value4 = request.POST.get('s4', 0)
        value4_1 = request.POST.get('s4_1', 0)
        v1_list.append(value4)
        v2_list.append(value4_1)
        total_list.append("布林帶帶寬" + str(value4) + str(value4_1))

        check_list.append(request.POST.get('checkbox5', '0'))
        value5 = request.POST.get('s5', 0)
        value5_1 = request.POST.get('s5_1', 0)
        v1_list.append(value5)
        v2_list.append(value5_1)
        total_list.append("真實波動幅度均值" + str(value5) + str(value5_1))

        check_list.append(request.POST.get('checkbox6', '0'))
        value6 = request.POST.get('s6', 0)
        value6_1 = request.POST.get('s6_1', 0)
        v1_list.append(value6)
        v2_list.append(value6_1)
        total_list.append("指定時間內的" + str(value6))

        check_list.append(request.POST.get('checkbox7', '0'))
        value7 = request.POST.get('s7', 0)
        value7_1 = request.POST.get('s7_1', 0)
        v1_list.append(value7)
        v2_list.append(value7_1)
        total_list.append("固定時間內的開高收低")

        check_list.append(request.POST.get('checkbox8', '0'))
        value8 = request.POST.get('s8', 0)
        value8_1 = request.POST.get('s8_1', 0)
        v1_list.append(value8)
        v2_list.append(value8_1)
        total_list.append("計算平均移動價格")

        check_list.append(request.POST.get('checkbox9', '0'))
        value9 = request.POST.get('s9', 0)
        value9_1 = request.POST.get('s9_1', 0)
        v1_list.append(value9)
        v2_list.append(value9_1)
        total_list.append("進入平倉前高收低")

        check_list.append(request.POST.get('checkbox10', '0'))
        value10 = request.POST.get('s10', 0)
        value10_1 = request.POST.get('s10_1', 0)
        v1_list.append(value10)
        v2_list.append(value10_1)
        total_list.append("價格動量指標" + str(value10) + str(value10_1))

        check_list.append(request.POST.get('checkbox11', '0'))
        value11 = request.POST.get('s11', 0)
        value11_1 = request.POST.get('s11_1', 0)
        v1_list.append(value11)
        v2_list.append(value11_1)
        total_list.append("買進")

        check_list.append(request.POST.get('checkbox12', '0'))
        value12 = request.POST.get('s12', 0)
        value12_1 = request.POST.get('s12_1', 0)
        v1_list.append(value12)
        v2_list.append(value12_1)
        total_list.append("賣出")

        check_list.append(request.POST.get('checkbox13', '0'))
        value13 = request.POST.get('s13', 0)
        value13_1 = request.POST.get('s13_1', 0)
        v1_list.append(value13)
        v2_list.append(value13_1)
        total_list.append("做多")

        check_list.append(request.POST.get('checkbox14', '0'))
        value14 = request.POST.get('s14', 0)
        value14_1 = request.POST.get('s14_1', 0)
        v1_list.append(value14)
        v2_list.append(value14_1)
        total_list.append("做空")

        check_list.append(request.POST.get('checkbox16', '0'))
        value15 = request.POST.get('s16', 0)
        value15_1 = request.POST.get('s16_1', 0)
        v1_list.append(value15)
        v2_list.append(value15_1)
        total_list.append("臺指期")

        check_list.append(request.POST.get('checkbox18', '0'))
        value17 = request.POST.get('s18', 0)
        value17_1 = request.POST.get('s18_1', 0)
        v1_list.append(value17)
        v2_list.append(value17_1)
        total_list.append("電子期")

        check_list.append(request.POST.get('checkbox19', '0'))
        value18 = request.POST.get('s19', 0)
        value18_1 = request.POST.get('s19_1', 0)
        v1_list.append(value18)
        v2_list.append(value18_1)
        total_list.append("金融期")

        check_list.append(request.POST.get('checkbox20', '0'))
        value19 = request.POST.get('s20', 0)
        value19_1 = request.POST.get('s20_1', 0)
        v1_list.append(value19)
        v2_list.append(value19_1)
        total_list.append("小臺指期")

        check_list.append(request.POST.get('checkbox21', '0'))
        value20 = request.POST.get('s21', 0)
        value20_1 = request.POST.get('s21_1', 0)
        v1_list.append(value20)
        v2_list.append(value20_1)
        total_list.append("櫃買期")

        check_list.append(request.POST.get('checkbox22', '0'))
        value21 = request.POST.get('s22', 0)
        value21_1 = request.POST.get('s22_1', 0)
        v1_list.append(value21)
        v2_list.append(value21_1)
        total_list.append("現金股利：近一年數據" + str(value21) + str(value21_1) + "元")

        check_list.append(request.POST.get('checkbox23', '0'))
        value22 = request.POST.get('s23', 0)
        value22_1 = request.POST.get('s23_1', 0)
        v1_list.append(value22)
        v2_list.append(value22_1)
        total_list.append("股價：" + str(value22) + str(value22_1) + "元")

        check_list.append(request.POST.get('checkbox24', '0'))
        value23 = request.POST.get('s24', 0)
        value23_1 = request.POST.get('s24_1', 0)
        v1_list.append(value23)
        v2_list.append(value23_1)
        total_list.append("上市櫃時間：" + str(value23) + str(value23_1) + "年")

        check_list.append(request.POST.get('checkbox27', '0'))
        value24 = request.POST.get('s27', 0)
        value24_1 = request.POST.get('s27_1', 0)
        v1_list.append(value24)
        v2_list.append(value24_1)
        total_list.append("存貨週轉天數：近一季數據" + str(value24) + str(value24_1) + "天")

        check_list.append(request.POST.get('checkbox28', '0'))
        value25 = request.POST.get('s28', 0)
        value25_1 = request.POST.get('s28_1', 0)
        v1_list.append(value25)
        v2_list.append(value25_1)
        total_list.append("營運週轉天數：近一季數據" + str(value25) + str(value25_1) + "天")

        check_list.append(request.POST.get('checkbox30', '0'))
        value26 = request.POST.get('s30', 0)
        value26_1 = request.POST.get('s30_1', 0)
        v1_list.append(value26)
        v2_list.append(value26_1)
        total_list.append("test123")

        check_list.append(request.POST.get('checkbox31', '0'))
        value27 = request.POST.get('s31', 0)
        value27_1 = request.POST.get('s31_1', 0)
        v1_list.append(value27)
        v2_list.append(value27_1)

        total_list.append("test123" + str(value27) + str(value27_1))

        check_list.append(request.POST.get('checkbox34', '0'))
        value28 = request.POST.get('s34', 0)
        value28_1 = request.POST.get('s34_1', 0)
        v1_list.append(value28)
        v2_list.append(value28_1)
        total_list.append("營業現金流年成長：近一年數據" + str(value28) + str(value28_1) + "%")

        check_list.append(request.POST.get('checkbox35', '0'))
        value29 = request.POST.get('s35', 0)
        value29_1 = request.POST.get('s35_1', 0)
        v1_list.append(value29)
        v2_list.append(value29_1)
        total_list.append("自由現金流年成長：近一年數據" + str(value29) + str(value29_1) + "%")

        check_list.append(request.POST.get('checkbox37', '0'))
        value30 = request.POST.get('s37', 0)
        value30_1 = request.POST.get('s37_1', 0)
        v1_list.append(value30)
        v2_list.append(value30_1)
        total_list.append("ROE年成長：近一年數據" + str(value30) + str(value30_1) + "%")

        check_list.append(request.POST.get('checkbox38', '0'))
        value31 = request.POST.get('s38', 0)
        value31_1 = request.POST.get('s38_1', 0)
        v1_list.append(value31)
        v2_list.append(value31_1)
        total_list.append("ROA年成長：近一年數據" + str(value31) + str(value31_1) + "%")

        for n in range(0, len(check_list)):
            if check_list[n] == '1':
                if list_now.count() == 0:
                    FutureStockList.objects.create(member_id=member, list_id=list_id, list_name="清單未命名",
                                                   context_id=total_list_id[n],
                                                   context_ope=v1_list[n], context_num=v2_list[n],
                                                   context=total_list[n])
                else:
                    list_name = list_now[0].list_name
                    FutureStockList.objects.create(member_id=member, list_id=list_id, list_name=list_name,
                                                   context_id=total_list_id[n],
                                                   context_ope=v1_list[n], context_num=v2_list[n],
                                                   context=total_list[n])

    list1 = FutureStockList.objects.filter(member_id=member, list_id=1)
    list2 = FutureStockList.objects.filter(member_id=member, list_id=2)
    list3 = FutureStockList.objects.filter(member_id=member, list_id=3)
    list4 = FutureStockList.objects.filter(member_id=member, list_id=4)
    list5 = FutureStockList.objects.filter(member_id=member, list_id=5)
    n1 = 15 - list1.count()
    n2 = 15 - list2.count()
    n3 = 15 - list3.count()
    n4 = 15 - list4.count()
    n5 = 15 - list5.count()

    return render_to_response('mem_sto.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                               'list5': list5, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5})


# member 會員期貨清單  修改+刪除
def member_list_del(request):
    try:
        member_name = request.session['name']
    except KeyError:
        return render_to_response('login.html')
    # member = '1'
    member = FutureMember.objects.get(member_name=member_name).member_id
    list_id = request.GET.get('re', 0)  # 1,2,3,4,5

    if request.method == 'POST':
        con = request.POST.get('re2', '0')  # 確認修改
        if con == 're2':
            list_name = request.POST.get('list_name', '0')  # 修改後的名字
            FutureStockList.objects.filter(member_id=member, list_id=list_id).update(list_name=list_name)
        delete_all = request.POST.get('clearAll', '0')  # 整筆清單刪除
        check_list = []  # checkbox 1or0
        total_list = FutureStockList.objects.filter(member_id=member, list_id=list_id)  # =list_now
        fin_list = []  # 單筆刪除後的清單
        check_list.append(request.POST.get('checkbox1', '0'))
        check_list.append(request.POST.get('checkbox2', '0'))
        check_list.append(request.POST.get('checkbox3', '0'))
        check_list.append(request.POST.get('checkbox4', '0'))
        check_list.append(request.POST.get('checkbox5', '0'))
        check_list.append(request.POST.get('checkbox6', '0'))
        check_list.append(request.POST.get('checkbox7', '0'))
        check_list.append(request.POST.get('checkbox8', '0'))
        check_list.append(request.POST.get('checkbox9', '0'))
        check_list.append(request.POST.get('checkbox10', '0'))
        check_list.append(request.POST.get('checkbox11', '0'))
        check_list.append(request.POST.get('checkbox12', '0'))
        check_list.append(request.POST.get('checkbox13', '0'))
        check_list.append(request.POST.get('checkbox14', '0'))
        check_list.append(request.POST.get('checkbox15', '0'))

        for n in range(0, len(total_list)):  # 刪單筆
            if check_list[n] == '0':
                fin_list.append(total_list[n])
        FutureStockList.objects.filter(member_id=member, list_id=list_id).delete()
        for n in range(0, len(fin_list)):
            FutureStockList.objects.create(member_id=member, list_id=list_id, list_name=fin_list[0].list_name,
                                           context_id=fin_list[n].context_id,
                                           context_ope=fin_list[n].context_ope, context_num=fin_list[n].context_num,
                                           context=fin_list[n].context)

        if delete_all == 'clearAll':  # 刪整個清單
            FutureStockList.objects.filter(member_id=member, list_id=list_id).delete()
            list1 = FutureStockList.objects.filter(member_id=member, list_id=1)
            list2 = FutureStockList.objects.filter(member_id=member, list_id=2)
            list3 = FutureStockList.objects.filter(member_id=member, list_id=3)
            list4 = FutureStockList.objects.filter(member_id=member, list_id=4)
            list5 = FutureStockList.objects.filter(member_id=member, list_id=5)
            n1 = 15 - list1.count()
            n2 = 15 - list2.count()
            n3 = 15 - list3.count()
            n4 = 15 - list4.count()
            n5 = 15 - list5.count()
            return render_to_response('mem_sto.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                                       'list5': list5, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4,
                                                       'n5': n5})

    list_now = FutureStockList.objects.filter(member_id=member, list_id=list_id)
    try:
        name1 = FutureStockList.objects.filter(member_id=member, list_id=list_id)
        name = name1[0].list_name
    except IndexError:  # 假如name1[0].list_name不存在
        list1 = FutureStockList.objects.filter(member_id=member, list_id=1)
        list2 = FutureStockList.objects.filter(member_id=member, list_id=2)
        list3 = FutureStockList.objects.filter(member_id=member, list_id=3)
        list4 = FutureStockList.objects.filter(member_id=member, list_id=4)
        list5 = FutureStockList.objects.filter(member_id=member, list_id=5)
        n1 = 15 - list1.count()
        n2 = 15 - list2.count()
        n3 = 15 - list3.count()
        n4 = 15 - list4.count()
        n5 = 15 - list5.count()
        return render_to_response('mem_sto.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                                   'list5': list5, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5})

    return render_to_response('mem_future.html', {'list_now': list_now, 'name': name, 're': list_id})


# 追蹤訊息
def message(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        return HttpResponseRedirect('/login/?back=訊息推播')
    email = FutureMember.objects.get(member_name=name).email
    tr_list = request.POST.get('category', '')
    t = FutureTrackFuture.objects.order_by('list_name').values('list_name').distinct()
    if request.method == 'POST':
        p = request.POST.get('sure', '')
        p2 = request.POST.get('complete', '')
        if p == '1':
            listname = request.POST.get('category', '')
            t2 = FutureTrackFuture.objects.filter(list_name=listname)
            return render_to_response('message.html',
                                      {'loginstatus': loginstatus, 'name': name, 'content': t2, 'list': t,
                                       'length': range(len(t2)), 'length2': len(t2), 'email': email,
                                       'tr_list': tr_list})
        elif p2 == '1':
            leng = request.POST.get('length', '')
            stock = []
            for i in range(int(leng)):
                stocks = request.POST.get(str(i), '')
                if stocks != '':
                    stock.append(stocks)
            stri, t1, t2, td = '', '', '', ''
            mes, mes2, mes3, mail, = request.POST.get('check2', ''), request.POST.get('check3', ''), request.POST.get(
                'check4', ''), request.POST.get('email', '')
            ma_1, kd_1, more = request.POST.get('ma_1', ''), request.POST.get('kd_1', ''), request.POST.get('more', '')
            ma_2, kd_2, none = request.POST.get('ma_2', ''), request.POST.get('kd_2', ''), request.POST.get('none', '')
            robot1, robot2 = request.POST.get('robot1', ''), request.POST.get('robot2', '')

            for i in stock:
                sn = FutureInformation.objects.get(stock_id=i).co_name
                stri = stri + '<p><font size=+2><strong>' + i + ' ' + sn + '</font></strong></p>'
                if mes != '':
                    share = Share(i + '.TW')
                    price, change, vol = share.get_price(), share.get_change(), share.get_volume()
                    if price is None:
                        price = '很抱歉，目前無資料。'
                    if change is None:
                        change = '很抱歉，目前無資料。'
                    if vol is None:
                        vol = '很抱歉，目前無資料。'
                    t1 = """\
                    <table id="customers">
                        <tr>
                        <th>價格</th>
                        <th>漲跌幅</th>
                        <th>成交量</th>
                        </tr>
                        <tr>
                        <td>""" + price + """</td>
                        <td>""" + change + """</td>
                        <td>""" + vol + """</td>
                        </tr>
                    </table>
                    <br>
                        """
                    stri = stri + t1

                if mes2 != '':
                    date = datetime.now().strftime("%Y/%m/%d")
                    latest, latest2, latest3, latest4 = FutureYahooHot.objects.filter(date=date,
                                                                                      content__contains=sn), FutureYahooStock.objects.filter(
                        date=date, content__contains=sn), FutureYahooTec.objects.filter(date=date,
                                                                                        content__contains=sn), FutureYahootra.objects.filter(
                        date=date, content__contains=sn)
                    if latest or latest2 or latest3 or latest4:
                        th = """\
                        <table id="customers">
                            <tr>
                            <th>日期</th>
                            <th>標題</th>
                            </tr>

                            """
                        for i in latest:
                            print('1')
                            td2 = """\
                            <tr>
                            <td>""" + i.date + """</td>
                            <td>""" + i.title + """</td>
                            </tr>
                            <tr>
                            <td colspan="2">""" + i.content + """</td>
                            </tr>
                            """
                            td = td + td2
                        for i in latest2:
                            print('1')
                            td2 = """\
                            <tr>
                            <td>""" + i.date + """</td>
                            <td>""" + i.title + """</td>
                            </tr>
                            <tr>
                            <td colspan="2">""" + i.content + """</td>
                            </tr>
                            """
                            td = td + td2
                        for i in latest3:
                            print('1')
                            td2 = """\
                            <tr>
                            <td>""" + i.date + """</td>
                            <td>""" + i.title + """</td>
                            </tr>
                            <tr>
                            <td colspan="2">""" + i.content + """</td>
                            </tr>
                            """
                            td = td + td2
                        for i in latest4:
                            print('1')
                            td2 = """\
                            <tr>
                            <td>""" + i.date + """</td>
                            <td>""" + i.title + """</td>
                            </tr>
                            <tr>
                            <td colspan="2">""" + i.content + """</td>
                            </tr>
                            """
                            td = td + td2
                        th2 = """\
                        </table>
                        <br>
                        """
                        stri = stri + th + td + th2
                        td = ''
                    else:
                        th = """\
                        <table id="customers">
                            <tr>
                            <th>日期</th>
                            </tr>
                            """
                        td2 = """\
                            <tr>
                            <td>""" + date + """ 目前沒有新聞</td>
                            </tr>
                            """
                        th2 = """\
                        </table>
                        <br>
                        """
                        stri = stri + th + td2 + th2

                ####robot1 買賣分析
                if robot1 != '':
                    date = datetime.now().strftime("%Y/%m/%d")
                    share = Share(i + '.TW')
                    price = float(share.get_price())
                    if price is None:
                        price = FutureTransactionInfo.objects.get(date="20160826", stock_id=i).the_close

                    cheap, normal, expensive = 0, 0, 0
                    min, max = [], []
                    signal, signal2, signal3, kd, macd = '', '', '', '', ''
                    st_pe = PE.objects.filter(stock_id=i)
                    for n in st_pe:
                        try:
                            min.append(round(float(n.pe_low), ndigits=2))
                            max.append(round(float(n.pe_high), ndigits=2))
                        except:
                            min.append(0)
                            max.append(0)

                    min = np.mean(min)
                    max = np.mean(max)
                    mean = (min + max) / 2
                    mean_4Q = round(float(PE.objects.get(stock_id=i, date='2016Q2').pe_for_four_season), ndigits=2)
                    cheap = mean_4Q * min
                    expensive = mean_4Q * max
                    normal = mean_4Q * mean

                    if price >= expensive:  # 被高估 : 賣(-)
                        signal = '價格被高估，未來可能下跌，建議賣出'
                    elif price <= cheap:  # 被低估 : 買(+)
                        signal = '價格被低估，未來上漲機會較大，建議分批買進'
                    else:
                        signal = '無明顯買賣訊號'

                    try:
                        k_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_K)
                        k_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_K)
                        d_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_D)
                        d_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_D)
                    except:
                        k_now = 0
                        k_yes = 0
                        d_now = 0
                        d_yes = 0

                    if k_now >= d_now and k_yes < d_yes:  # 日KD黃金交叉
                        signal3 = '+'
                        kd = '黃金交叉'
                    elif k_now < d_now and k_yes >= d_yes:  # 日KD死亡交叉
                        signal3 = '-'
                        kd = '死亡交叉'
                    else:
                        signal3 = '0'
                        kd = '無明顯訊號'

                    try:
                        ma_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_MACD)
                        ma_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_MACD)
                    except:
                        ma_now = 0
                        ma_yes = 0

                    if ma_now > ma_yes:  # 日MACD黃金交叉
                        signal2 = '+'
                        macd = '黃金交叉'
                    elif ma_now < ma_yes:  # 日MACD死亡交叉
                        signal2 = '-'
                        macd = '死亡交叉'
                    else:
                        signal2 = '0'
                        macd = '無明顯訊號'

                    if signal2 == '+' and signal3 == '+':
                        signal = 'MACD及KD均呈黃金交叉，有明顯買進訊號'
                    elif signal2 == '-' and signal3 == '-':
                        signal = 'MACD及KD均呈死亡交叉，有明顯賣出訊號'
                    elif signal2 == '+' and signal3 != '-':
                        signal = 'MACD成黃金交叉，有買進訊號'
                    elif signal2 != '-' and signal3 == '+':
                        signal = 'KD成黃金交叉，有買進訊號'
                    elif signal2 == '-' and signal3 != '-':
                        signal = 'MACD成死亡交叉，有賣出訊號'
                    elif signal2 != '-' and signal3 == '-':
                        signal = 'KD成死亡交叉，有賣出訊號'
                    else:
                        signal = '沒有明顯買賣訊號'

                    t1 = """\
                    <table id="customers4">
                        <tr>
                        <th>日期</th>
                        <th>當前價格</th>
                        <th>估價法分析</th>
                        </tr>
                        <tr>
                        <td width=25%>""" + date + """</td>
                        <td width=25%>""" + str(price) + """</td>
                        <td width=50%>""" + signal + """</td>
                        </tr>
                    </table>
                    <br>
                    <table id="customers2">
                        <tr>
                        <th>kd</th>
                        <th>macd</th>
                        <th>指標分析</th>
                        </tr>
                        <tr>
                        <td width=25%>""" + kd + """</td>
                        <td width=25%>""" + macd + """</td>
                        <td width=50%>""" + signal + """</td>
                        </tr>
                    </table>
                        """
                    stri = stri + t1

                # 買賣訊號設定
                kd1, macd1, kd2, macd2, more, none = '', '', '', '', '', ''
                # date = datetime.now().strftime("%Y/%m/%d")
                try:
                    k_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_K)
                    k_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_K)
                    d_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_D)
                    d_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_D)
                except:
                    k_now, k_yes, d_now, d_yes = 0, 0, 0, 0

                if k_now >= d_now and k_yes < d_yes:  # 日KD黃金交叉
                    kd1 = 'kd 黃金交叉'
                elif k_now < d_now and k_yes >= d_yes:  # 日KD死亡交叉
                    kd2 = 'kd 死亡交叉'
                else:
                    kd1, kd2 = '', ''

                try:
                    ma_now = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160826').day_MACD)
                    ma_yes = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160825').day_MACD)
                    ma_yes2 = float(FutureTechnologyIndex2.objects.get(stock_id=i, date='20160824').day_MACD)
                except:
                    ma_now, ma_yes, ma_yes2 = 0, 0, 0

                if ma_now > ma_yes:  # 日MACD黃金交叉
                    macd1 = 'macd 黃金交叉'
                elif ma_now < ma_yes:  # 日MACD死亡交叉
                    macd2 = 'macd 死亡交叉'
                else:
                    macd1, macd2 = '', ''
                if ma_now >= ma_yes and ma_yes >= ma_yes2:
                    more = '均線呈多頭排列'
                else:
                    more = ''
                if ma_now <= ma_yes and ma_yes <= ma_yes2:
                    none = '均線呈空頭排列'
                else:
                    none = ''

                if ma_1 != '' or kd_1 != '' or more != '':
                    if macd1 != '' or kd1 != '' or more != '':
                        t1 = """\
                        <table id="customers3">
                            <tr>
                            <th>訊號類別</th>
                            <th>訊號分析</th>
                            </tr>
                            <tr>
                            <td width=50%>""" + '買進訊號' + """</td>
                            <td width=50%>""" + macd1 + ' ' + kd1 + ' ' + more + """</td>
                            </tr>
                        </table>
                            """
                        stri = stri + t1
                if ma_2 != '' or kd_2 != '' or none != '':
                    if macd2 != '' or kd2 != '' or none != '':
                        t1 = """\
                        <table id="customers3">
                            <tr>
                            <th>訊號類別</th>
                            <th>訊號分析</th>
                            </tr>
                            <tr>
                            <td width=50%>""" + '賣出訊號' + """</td>
                            <td width=50%>""" + macd2 + ' ' + kd2 + ' ' + none + """</td>
                            </tr>
                        </table>
                            """
                        stri = stri + t1

            html_text = """\
            <html>
            <head>
            <style type="text/css">
        #customers
          {
          font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
          width:100%;
          border-collapse:collapse;
          }
        #customers td, #customers th
          {
          font-size:1em;
          border:1px solid #64970E;
          padding:3px 7px 2px 7px;
          }
        #customers th
          {
          font-size:1.1em;
          text-align:left;
          padding-top:5px;
          padding-bottom:4px;
          background-color:#9CCF44;
          color:#ffffff;
          }
        #customers tr.alt td
          {
          color:#000000;
          background-color:#EAF2D3;
          }

        #customers2
          {
          font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
          width:100%;
          border-collapse:collapse;
          }
        #customers2 td, #customers2 th
          {
          font-size:1em;
          border:1px solid #3B9797;
          padding:3px 7px 2px 7px;
          }
        #customers2 th
          {
          font-size:1.1em;
          text-align:left;
          padding-top:5px;
          padding-bottom:4px;
          background-color:#67B9B9;
          color:#ffffff;
          }
          #customers3
          {
          font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
          width:100%;
          border-collapse:collapse;
          }
        #customers3 td, #customers3 th
          {
          font-size:1em;
          border:1px solid #107D68;
          padding:3px 7px 2px 7px;
          }
        #customers3 th
          {
          font-size:1.1em;
          text-align:left;
          padding-top:5px;
          padding-bottom:4px;
          background-color:#3FA18E;
          color:#ffffff;
          }

          #customers4
          {
          font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
          width:100%;
          border-collapse:collapse;
          }
        #customers4 td, #customers4 th
          {
          font-size:1em;
          border:1px solid #EF5E72;
          padding:3px 7px 2px 7px;
          }
        #customers4 th
          {
          font-size:1.1em;
          text-align:left;
          padding-top:5px;
          padding-bottom:4px;
          background-color:#F78998;
          color:#ffffff;
          }
        </style>
            </head>
            <body>
            """ + stri + """
            </body>
            </html>
            """
            send_mail('Future Futures', '您的設定已完成囉', 'jaluka188@gmail.com', [mail, ], fail_silently=False,
                      html_message=html_text)
            return HttpResponseRedirect('/message/')

    return render_to_response('message.html',
                              {'list': t, 'loginstatus': loginstatus, 'name': name, 'email': email, 'tr_list': tr_list})


def email2(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('message.html', {'name': name, 'loginstatus': loginstatus})


def email1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        return HttpResponseRedirect('/smallschool/')
    if request.method == 'POST':
        p = request.POST.get('complete', '')
        # if p == '1':
        #
        #     future_id = request.POST.get('mess1', '')
        #     t2 = FutureTrackFuture.objects.filter(future_id=future_id)
        #     return render_to_response('message.html',{'loginstatus': loginstatus, 'name': name, 'content': t2})
        stri, t1, t2, td = '', '', '', ''

        mes2 = request.POST.get('check3', '')

        if mes2 != '':
            date = datetime.now().strftime("%Y/%m/%d")
            latest, latest2, latest3, latest4 = FutureYahooHot.objects.filter(
                date=date), FutureYahooStock.objects.filter(
                date=date), FutureYahooTec.objects.filter(date=date), FutureYahooTra.objects.filter(date=date)
            if latest or latest2 or latest3 or latest4:
                th = """\
                               <table id="customers">
                                   <tr>
                                   <th>日期</th>
                                   <th>標題</th>
                                   </tr>

                                   """
                for i in latest:
                    print('1')
                    td2 = """\
                                   <tr>
                                   <td>""" + i.date + """</td>
                                   <td>""" + i.title + """</td>
                                   </tr>
                                   <tr>
                                   <td colspan="2">""" + i.content + """</td>
                                   </tr>
                                   """
                    td = td + td2
                for i in latest2:
                    print('1')
                    td2 = """\
                                   <tr>
                                   <td>""" + i.date + """</td>
                                   <td>""" + i.title + """</td>
                                   </tr>
                                   <tr>
                                   <td colspan="2">""" + i.content + """</td>
                                   </tr>
                                   """
                    td = td + td2
                for i in latest3:
                    print('1')
                    td2 = """\
                                   <tr>
                                   <td>""" + i.date + """</td>
                                   <td>""" + i.title + """</td>
                                   </tr>
                                   <tr>
                                   <td colspan="2">""" + i.content + """</td>
                                   </tr>
                                   """
                    td = td + td2
                for i in latest4:
                    print('1')
                    td2 = """\
                                   <tr>
                                   <td>""" + i.date + """</td>
                                   <td>""" + i.title + """</td>
                                   </tr>
                                   <tr>
                                   <td colspan="2">""" + i.content + """</td>
                                   </tr>
                                   """
                    td = td + td2
                th2 = """\
                               </table>
                               <br>
                               """
                stri = stri + th + td + th2
                td = ''
            else:
                th = """\
                               <table id="customers">
                                   <tr>
                                   <th>日期</th>
                                   </tr>
                                   """
                td2 = """\
                                   <tr>
                                   <td>""" + date + """ 目前沒有新聞</td>
                                   </tr>
                                   """
                th2 = """\
                               </table>
                               <br>
                               """
                stri = stri + th + td2 + th2

    html_text = """\
               <html>
               <head>
               <style type="text/css">
           #customers
             {
             font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
             width:100%;
             border-collapse:collapse;
             }
           #customers td, #customers th
             {
             font-size:1em;
             border:1px solid #64970E;
             padding:3px 7px 2px 7px;
             }
           #customers th
             {
             font-size:1.1em;
             text-align:left;
             padding-top:5px;
             padding-bottom:4px;
             background-color:#9CCF44;
             color:#ffffff;
             }
           #customers tr.alt td
             {
             color:#000000;
             background-color:#EAF2D3;
             }

           #customers2
             {
             font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
             width:100%;
             border-collapse:collapse;
             }
           #customers2 td, #customers2 th
             {
             font-size:1em;
             border:1px solid #3B9797;
             padding:3px 7px 2px 7px;
             }
           #customers2 th
             {
             font-size:1.1em;
             text-align:left;
             padding-top:5px;
             padding-bottom:4px;
             background-color:#67B9B9;
             color:#ffffff;
             }
             #customers3
             {
             font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
             width:100%;
             border-collapse:collapse;
             }
           #customers3 td, #customers3 th
             {
             font-size:1em;
             border:1px solid #107D68;
             padding:3px 7px 2px 7px;
             }
           #customers3 th
             {
             font-size:1.1em;
             text-align:left;
             padding-top:5px;
             padding-bottom:4px;
             background-color:#3FA18E;
             color:#ffffff;
             }

             #customers4
             {
             font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
             width:100%;
             border-collapse:collapse;
             }
           #customers4 td, #customers4 th
             {
             font-size:1em;
             border:1px solid #EF5E72;
             padding:3px 7px 2px 7px;
             }
           #customers4 th
             {
             font-size:1.1em;
             text-align:left;
             padding-top:5px;
             padding-bottom:4px;
             background-color:#F78998;
             color:#ffffff;
             }
           </style>
               </head>
               <body>
                 """ + stri + """
               </body>
               </html>
               """
    send_mail('你的訊息', '', 'jaluka177gmail.com', ['jaluka188@gmail.com'], fail_silently=False, html_message=html_text)

    return render(request, 'notify.html')


def email(request):
    html_message = loader.render_to_string(
        'email.html',
        {

        }
    )
    send_mail('你的訊息', '', 'jaluka177gmail.com', ['jaluka188@gmail.com'], fail_silently=False, html_message=html_message)

    return render(request, 'notify.html')


def modifypassword(request):
    try:
        username = request.session['userName']
    except:
        return HttpResponseRedirect('/login/?back=修改密碼')
    if request.method == 'POST':
        newpassword = request.POST.get('newpass', '')
        check = request.POST.get('pass', '')
        check_2 = FutureMember.objects.filter(password=newpassword)
        if check_2:
            wrong = '此密碼已被使用'
            return render_to_response('mo_pass.html', {'wrong': wrong})
        elif newpassword == check:
            FutureMember.objects.filter(email=username).update(password=newpassword)
            return render_to_response('login.html')
    return render_to_response('mo_pass.html')


def modify(request):
    try:
        username = request.session['userName']
        result = FutureMember.objects.get(email=username)
    except:
        return HttpResponseRedirect('/login/?back=修改基本資料')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        mail = request.POST.get('mail', '')
        phone = request.POST.get('phone', '')
        FutureMember.objects.filter(email=username).update(member_name=name, email=mail, phone_num=phone)
        request.session['name'] = name
        request.session['userName'] = mail
        return render_to_response('login.html')
    return render_to_response('modify.html', {'member': result})


# 首頁

def home1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('smallschool.html', {'name': name, 'loginstatus': loginstatus})


# 新聞
def get_news(request):  # check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    result = []
    result_2 = []
    result_3 = []
    result_4 = []
    result_5 = []
    result_6 = []
    result_7 = []
    last = FutureYahooNew.objects.order_by('-date')
    last2 = FutureCna.objects.order_by('-date')
    last3 = FutureYahooHot.objects.order_by('-date')
    last4 = FutureYahoo.objects.order_by('-date')
    last5 = FutureYahooStock.objects.order_by('-date')
    last6 = FutureYahooTec.objects.order_by('-date')
    last7 = FutureYahooTra.objects.order_by('-date')

    for n in range(0, 7):
        result.append(last[n])

    for n in range(0, 7):
        result_2.append(last2[n])

    for n in range(0, 7):
        result_3.append(last3[n])

    for n in range(0, 6):
        result_4.append(last4[n])

    for n in range(0, 6):
        result_5.append(last5[n])

    for n in range(0, 6):
        result_6.append(last6[n])

    for n in range(0, 6):
        result_7.append(last7[n])

    return render_to_response('news.html',
                              {'breaking_news': result, 'global': result_2, 'hot': result_3, 't_all': result_4,
                               'stock': result_5, 'tec': result_6, 'tra': result_7, 'name': name,
                               'loginstatus': loginstatus})


# 新聞爬蟲1
def crawler(request):
    name = ''
    loginstatus = False
    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。
    url = 'https://www.cna.com.tw/list/aopl.aspx'
    html_data = urllib.request.urlopen(url).read()
    # 使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
    soup = BeautifulSoup(html_data, 'html.parser')
    print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text())
    # 可以看看html裡面的文字內容
    print(rows)
    id = 1
    for row in rows:
        items = row.find_all('h2')
        name = items[0].a.text.strip()  # strip是去前後空格

        # print(name)
        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.id = None
                self.title = None
                self.content = None
                self.date = None
                self.time = None

            def __str__(self):
                res = list()
                res.append(self.id)
                res.append(self.title)
                res.append(self.content)
                res.append(self.date)
                res.append(self.time)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)

        id = id + 1
        quote.id = id
        quote.title = items[0].font.text.replace(',', '')  # TITLE
        quote.content = items[1].font.text.replace(',', '')  # CONTENT
        quote.time = datetime.strptime(items[2].font.text, '%H:%M')  # DATE
        quote.time = datetime.strptime(items[4].font.text, '%H:%M')  # TIME

        # 創資料表放資料的部分
        conn = pymysql.connect(host='localhost', port=3306, passwd='root', user='root', db='mydatabase',
                               charset='utf8')
        cur = conn.cursor()
        cur.execute("USE mydatabase")
        try:
            cur.execute("DROP TABLE future_news")
        except:
            print("The table is not find...")
        cur.execute(
            """CREATE TABLE future_news (
            id int(100),
            title varchar(100),
            content varchar(100),
            date varchar(100),
            source varchar(100),
            time varchar(100))
            """)
        query = "INSERT INTO future_news(id, title, content, date, source, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s')" % (
            id, quote.title, quote.content, quote.date, '中央社CNA', quote.time)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        print("Upload to SQL successful...")
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# 新聞爬蟲2
def crawler2(request):
    name = ''
    loginstatus = False
    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。
    url = 'https://www.chinatimes.com/money/total?page=10&chdtv'
    html_data = urllib.request.urlopen(url).read()
    # 使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
    soup = BeautifulSoup(html_data, 'html.parser')
    print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text())
    # 可以看看html裡面的文字內容
    print(rows)
    id = 1
    for row in rows:
        items = row.find_all('h2')
        name = items[0].a.text.strip()  # strip是去前後空格

        # print(name)
        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.id = None
                self.title = None
                self.content = None
                self.date = None
                self.time = None

            def __str__(self):
                res = list()
                res.append(self.id)
                res.append(self.title)
                res.append(self.content)
                res.append(self.date)
                res.append(self.time)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)

        id = id + 1
        quote.id = id
        quote.title = items[0].font.text.replace(',', '')  # TITLE
        quote.content = items[1].font.text.replace(',', '')  # CONTENT
        quote.time = datetime.strptime(items[2].font.text, '%H:%M')  # DATE
        quote.time = datetime.strptime(items[4].font.text, '%H:%M')  # TIME

        # 創資料表放資料的部分
        conn = pymysql.connect(host='localhost', port=3306, passwd='root', user='root', db='mydatabase',
                               charset='utf8')
        cur = conn.cursor()
        cur.execute("USE mydatabase")
        try:
            cur.execute("DROP TABLE future_news")
        except:
            print("The table is not find...")
        cur.execute(
            """CREATE TABLE future_news (
            id int(100),
            title varchar(100),
            content varchar(100),
            date varchar(100),
            source varchar(100),
            time varchar(100))
            """)
        query = "INSERT INTO future_news(id, title, content, date, source, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s')" % (
            id, quote.title, quote.content, quote.date, '中時電子報', quote.time)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        print("Upload to SQL successful...")
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# 新聞爬蟲3
def crawler3(request):
    name = ''
    loginstatus = False
    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。
    url = 'https://news.cnyes.com/news/cat/wd_macro?exp=a'
    html_data = urllib.request.urlopen(url).read()
    # 使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
    soup = BeautifulSoup(html_data, 'html.parser')
    print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text())
    # 可以看看html裡面的文字內容
    print(rows)
    id = 1
    for row in rows:
        items = row.find_all('h2')
        name = items[0].a.text.strip()  # strip是去前後空格

        # print(name)
        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.id = None
                self.title = None
                self.content = None
                self.date = None
                self.time = None

            def __str__(self):
                res = list()
                res.append(self.id)
                res.append(self.title)
                res.append(self.content)
                res.append(self.date)
                res.append(self.time)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)

        id = id + 1
        quote.id = id
        quote.title = items[0].font.text.replace(',', '')  # TITLE
        quote.content = items[1].font.text.replace(',', '')  # CONTENT
        quote.time = datetime.strptime(items[2].font.text, '%H:%M')  # DATE
        quote.time = datetime.strptime(items[4].font.text, '%H:%M')  # TIME

        # 創資料表放資料的部分
        conn = pymysql.connect(host='localhost', port=3306, passwd='root', user='root', db='mydatabase',
                               charset='utf8')
        cur = conn.cursor()
        cur.execute("USE mydatabase")
        try:
            cur.execute("DROP TABLE future_news")
        except:
            print("The table is not find...")
        cur.execute(
            """CREATE TABLE future_news (
            id int(100),
            title varchar(100),
            content varchar(100),
            date varchar(100),
            source varchar(100),
            time varchar(100))
            """)
        query = "INSERT INTO future_news(id, title, content, date, source, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s')" % (
            id, quote.title, quote.content, quote.date, '鉅亨網', quote.time)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        print("Upload to SQL successful...")
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# 新聞爬蟲4
def crawler4(request):
    name = ''
    loginstatus = False
    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。
    url = 'https://m.moneydj.com/allNews.aspx'
    html_data = urllib.request.urlopen(url).read()
    # 使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
    soup = BeautifulSoup(html_data, 'html.parser')
    print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text())
    # 可以看看html裡面的文字內容
    print(rows)
    id = 1
    for row in rows:
        items = row.find_all('h2')
        name = items[0].a.text.strip()  # strip是去前後空格

        # print(name)
        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.id = None
                self.title = None
                self.content = None
                self.date = None
                self.time = None

            def __str__(self):
                res = list()
                res.append(self.id)
                res.append(self.title)
                res.append(self.content)
                res.append(self.date)
                res.append(self.time)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)

        id = id + 1
        quote.id = id
        quote.title = items[0].font.text.replace(',', '')  # TITLE
        quote.content = items[1].font.text.replace(',', '')  # CONTENT
        quote.time = datetime.strptime(items[2].font.text, '%H:%M')  # DATE
        quote.time = datetime.strptime(items[4].font.text, '%H:%M')  # TIME

        # 創資料表放資料的部分
        conn = pymysql.connect(host='localhost', port=3306, passwd='root', user='root', db='mydatabase',
                               charset='utf8')
        cur = conn.cursor()
        cur.execute("USE mydatabase")
        try:
            cur.execute("DROP TABLE future_news")
        except:
            print("The table is not find...")
        cur.execute(
            """CREATE TABLE future_news (
            id int(100),
            title varchar(100),
            content varchar(100),
            date varchar(100),
            source varchar(100),
            time varchar(100))
            """)
        query = "INSERT INTO future_news(id, title, content, date, source, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s')" % (
            id, quote.title, quote.content, quote.date, 'MoneyDJ', quote.time)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        print("Upload to SQL successful...")
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# 新聞爬蟲5
def crawler5(request):
    name = ''
    loginstatus = False
    # 應該要限制在有交易的時間內執行，但為了示範起見，使用無窮迴圈。
    url = 'https://money.udn.com/money/index'
    html_data = urllib.request.urlopen(url).read()
    # 使用urllib.request模块的urlopen（）获取页面 #urlopen返回对象可以使用read()#read() , readline() ,readlines() , fileno() , close() ：這些是对HTTPResponse类型数据进行操作
    soup = BeautifulSoup(html_data, 'html.parser')
    print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text())
    # 可以看看html裡面的文字內容
    print(rows)
    id = 1
    for row in rows:
        items = row.find_all('h2')
        name = items[0].a.text.strip()  # strip是去前後空格

        # print(name)
        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.id = None
                self.title = None
                self.content = None
                self.date = None
                self.time = None

            def __str__(self):
                res = list()
                res.append(self.id)
                res.append(self.title)
                res.append(self.content)
                res.append(self.date)
                res.append(self.time)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)

        id = id + 1
        quote.id = id
        quote.title = items[0].font.text.replace(',', '')  # TITLE
        quote.content = items[1].font.text.replace(',', '')  # CONTENT
        quote.time = datetime.strptime(items[2].font.text, '%H:%M')  # DATE
        quote.time = datetime.strptime(items[4].font.text, '%H:%M')  # TIME

        # 創資料表放資料的部分
        conn = pymysql.connect(host='localhost', port=3306, passwd='root', user='root', db='mydatabase',
                               charset='utf8')
        cur = conn.cursor()
        cur.execute("USE mydatabase")
        try:
            cur.execute("DROP TABLE future_news")
        except:
            print("The table is not find...")
        cur.execute(
            """CREATE TABLE future_news (
            id int(100),
            title varchar(100),
            content varchar(100),
            date varchar(100),
            source varchar(100),
            time varchar(100))
            """)
        query = "INSERT INTO future_news(id, title, content, date, source, time) VALUES (%s, '%s', '%s', '%s', '%s', '%s')" % (
            id, quote.title, quote.content, quote.date, '經濟日報', quote.time)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        print("Upload to SQL successful...")
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# --新聞文章回傳
def outcome_news(request):  # 搜尋文章結果 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    type = request.GET.get('id', 0)
    status_next = True
    status_prev = True
    if type is '1':
        category = '最新頭條'
        result = request.GET.get('c', 0)
        res = FutureYahooNew.objects.filter(title=result)[0]
        last = FutureYahooNew.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooNew.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahooNew.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooNew.objects.get(id=res.id + 1)
            prev_article = FutureYahooNew.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '2':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = FutureCna.objects.filter(title=result)[0]
        last = FutureCna.objects.last().id
        if res.id is 520:
            status_prev = False
            next_article = FutureCna.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureCna.objects.get(id=res.id + 1)
            prev_article = FutureCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '3':
        category = '熱門點閱'
        result = request.GET.get('c', 0)
        res = FutureYahooHot.objects.filter(title=result)[0]
        last = FutureYahooHot.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooHot.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahooHot.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooHot.objects.get(id=res.id + 1)
            prev_article = FutureYahooHot.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '4':
        category = '台股盤勢'
        result = request.GET.get('c', 0)
        res = FutureYahoo.objects.filter(title=result)[0]
        last = FutureYahoo.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahoo.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahoo.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahoo.objects.get(id=res.id + 1)
            prev_article = FutureYahoo.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '5':
        category = '個股動態'
        result = request.GET.get('c', 0)
        res = FutureYahooStock.objects.filter(title=result)[0]
        last = FutureYahooStock.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooStock.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahooStock.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooStock.objects.get(id=res.id + 1)
            prev_article = FutureYahooStock.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '6':
        category = '科技產業'
        result = request.GET.get('c', 0)
        res = FutureYahooTec.objects.filter(title=result)[0]
        last = FutureYahooTec.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooTec.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahooTec.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'satus_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooTec.objects.get(id=res.id + 1)
            prev_article = FutureYahooTec.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '7':
        category = '傳統產業'
        result = request.GET.get('c', 0)
        res = FutureYahooTra.objects.filter(title=result)[0]
        last = FutureYahooTra.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooTra.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureYahooTra.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooTra.objects.get(id=res.id + 1)
            prev_article = FutureYahooTra.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '8':
        category = '國際財經'
        result = request.GET.get('c', 0)
        res = FutureCna.objects.objects.filter(title=result)[0]
        last = FutureCna.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureCna.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:
            status_next = False
            prev_article = FutureCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureCna.objects.get(id=res.id + 1)
            prev_article = FutureCna.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})

    if type is '9':
        category = '熱門關鍵字'
        result = request.GET.get('c', 0)
        res = FutureYahooTendency.objects.filter(title=result)[0]
        last = FutureYahooTendency.objects.last().id
        if res.id is 1:
            status_prev = False
            next_article = FutureYahooTendency.objects.get(id=res.id + 1)
            return render_to_response('news_con.html', {'status_prev': status_prev, 'status_next': status_next,
                                                        'next_article': next_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        elif res.id is last:  # 目前只有12筆 之後會增加到30多筆
            status_next = False
            prev_article = FutureYahooTendency.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'category': category, 'id': type,
                                                        'result': res, 'name': name, 'loginstatus': loginstatus})
        else:
            next_article = FutureYahooTendency.objects.get(id=res.id + 1)
            prev_article = FutureYahooTendency.objects.get(id=res.id - 1)
            return render_to_response('news_con.html', {'status_next': status_next, 'status_prev': status_prev,
                                                        'prev_article': prev_article, 'next_article': next_article,
                                                        'category': category, 'id': type, 'result': res, 'name': name,
                                                        'loginstatus': loginstatus})


# --新聞回傳空白沒資料
def news_con(request):
    return render(request, 'news_con.html')


# --新聞查詢小bar
def search_news(request):  # 查詢文章關鍵字 check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    search_status = False  # 尚未查詢文章前狀態為false
    res_1 = []
    res_2 = []
    res_3 = []
    res_4 = []
    res_5 = []
    res_6 = []
    res_7 = []
    res_8 = []
    res_9 = []
    res_10 = []
    res_11 = []
    res_12 = []
    key2 = '關鍵字'
    if request.method == 'POST':
        search_status = True  # 開始查詢後狀態為True
        for_member = request.POST.get('search2', '')
        key = request.POST.get('search', '')
        if for_member != '':
            key = for_member[5:]
        else:
            pass

        yahoo_new_res_1 = FutureYahooNew.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_res_1 = FutureYahoo.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_stock_res_1 = FutureYahooStock.objects.filter(title__contains=key, content__contains=key).order_by(
            '-date')
        yahoo_stock_res_2 = FutureYahooStock.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        yahoo_tec_res_1 = FutureYahooTec.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_tec_res_2 = FutureYahooTec.objects.filter(content__contains=key).order_by('-date')
        yahoo_tra_res_1 = FutureYahooTra.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_tra_res_2 = FutureYahooTra.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        yahoo_hot_res_1 = FutureYahooHot.objects.filter(title__contains=key, content__contains=key).order_by('-date')
        yahoo_hot_res_2 = FutureYahooHot.objects.filter(tag__contains=key, content__contains=key).order_by('-date')
        cna_res_1 = FutureCna.objects.filter(title__contains=key, content__contains=key).order_by('-date')

        if yahoo_new_res_1:
            res_12 = yahoo_new_res_1
        if yahoo_res_1:
            res_1 = yahoo_res_1
        if yahoo_stock_res_1:
            res_2 = yahoo_stock_res_1
        if yahoo_stock_res_2:
            res_3 = yahoo_stock_res_2
        if yahoo_tec_res_1:
            res_4 = yahoo_tec_res_1
        if yahoo_tec_res_2:
            res_5 = yahoo_tec_res_2
        if yahoo_tra_res_1:
            res_6 = yahoo_tra_res_1
        if yahoo_tra_res_2:
            res_7 = yahoo_tra_res_2
        if yahoo_hot_res_1:
            res_9 = yahoo_hot_res_1
        if yahoo_hot_res_2:
            res_10 = yahoo_hot_res_2
        if cna_res_1:
            res_11 = cna_res_1
        return render_to_response('news_search.html',
                                  {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5,
                                   'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11,
                                   'res_12': res_12, 'status': search_status, 'key_word': key, 'name': name,
                                   'loginstatus': loginstatus, 'key2': key2})

    return render_to_response('news_search.html',
                              {'res_1': res_1, 'res_2': res_2, 'res_3': res_3, 'res_4': res_4, 'res_5': res_5,
                               'res_6': res_6, 'res_7': res_7, 'res_9': res_9, 'res_10': res_10, 'res_11': res_11,
                               'res_12': res_12, 'status': search_status, 'name': name, 'loginstatus': loginstatus,
                               'key2': key2})  # check# #


def search_news_for_keyword(request):  # check
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    key2 = '關鍵字'
    keyword = request.GET.get('key', 0)
    yahoo_tendency_res_1 = FutureYahooTendency.objects.filter(tag0=keyword).order_by('-date')
    yahoo_tendency_res_2 = FutureYahooTendency.objects.filter(tag1=keyword).order_by('-date')
    identity = request.GET.get('id', 0)
    status = True
    return render_to_response('news_search.html',
                              {'result_1': yahoo_tendency_res_1, 'result_2': yahoo_tendency_res_2, 'id': identity,
                               'key_word': keyword, 'status': status, 'name': name, 'loginstatus': loginstatus,
                               'key2': key2})


# --新聞查詢 有查日期功能
def list_page1(request):  # more: 第一頁 抓出該新聞類別的資料 check
    date = datetime.now().strftime('%Y-%m-%d')
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    category = request.GET.get('category', 0)
    page_2 = request.GET.get('page', '')
    # page_2 = int(page_2)
    type = request.GET.get('id', 0)
    if type is '1':
        news_list = FutureYahooNew.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '2':
        news_list = FutureCna.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '3':
        news_list = FutureYahooHot.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '4':
        news_list = FutureYahoo.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '5':
        news_list = FutureYahooStock.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    elif type is '6':
        news_list = FutureYahooTec.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})
    else:
        news_list = FutureYahooTra.objects.order_by('-date')
        paginator = Paginator(news_list, 30)
        try:
            news = paginator.page(page_2)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render_to_response('news_list.html',
                                  {'date': date, 'news_list': news, 'id': type, 'category': category, 'name': name,
                                   'loginstatus': loginstatus})


def time_search(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    search_status = True  # 尚未查詢文章前狀態為false
    res_1, res_2, res_4, res_6, res_8, res_9, res_11, res_12 = [], [], [], [], [], [], [], []
    s, e = request.POST.get('start', ''), request.POST.get('end', '')
    s = s[:4] + '/' + s[5:7] + '/' + s[8:]
    e = e[:4] + '/' + e[5:7] + '/' + e[8:]
    key = s + '～' + e
    key2 = '日期'
    if FutureYahoo.objects.filter(date__range=(s, e)):
        res_1 = FutureYahoo.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooGlobal.objects.filter(date__range=(s, e)):
        res_8 = FutureYahooGlobal.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooHot.objects.filter(date__range=(s, e)):
        res_9 = FutureYahooHot.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooNew.objects.filter(date__range=(s, e)):
        res_12 = FutureYahooNew.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooStock.objects.filter(date__range=(s, e)):
        res_2 = FutureYahooHot.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooTec.objects.filter(date__range=(s, e)):
        res_4 = FutureYahooTec.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureYahooTra.objects.filter(date__range=(s, e)):
        res_6 = FutureYahooTra.objects.filter(date__range=(s, e)).order_by('-date')
    if FutureCna.objects.filter(date__range=(s, e)):
        res_11 = FutureCna.objects.filter(date__range=(s, e)).order_by('-date')
    return render_to_response('news_search.html',
                              {'res_1': res_1, 'res_2': res_2, 'res_4': res_4, 'res_6': res_6, 'res_8': res_8,
                               'res_9': res_9, 'res_11': res_11, 'res_12': res_12, 'status': search_status,
                               'key_word': key, 'name': name, 'loginstatus': loginstatus, 'key2': key2})


# 交易資訊
# --歷史回測
def algotest(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    future_list = FutureTrackFuture.objects.filter(member_id=1)
    future = []  # 會員已有的期貨
    future_select = []  # 勾選的期貨
    future_final = []  # 勾選的期貨(最多三個)
    times_list = []
    money_final_list = []
    money_begin_list = []
    future_name_list = []
    money_begin = 0
    money_now = 0
    quantity = 0
    times = 0  # 交易次數

    for n1 in range(0, len(future_list)):
        future.append(future_list[n1].future_id)
    if request.method == 'POST':  # 開始選期貨
        for x in range(0, len(future)):
            future_select.append(request.POST.get(future[x], '0'))  # 接 選的期貨
        for y in range(0, len(future_select)):
            if future_select[y] != '0':
                future_final.append(future_select[y])
        future_ff = set(future_final)  # 去除重複
        future_final = list(future_ff)
        print(future_final)  # 刪
        money_begin = request.POST.get('money', '0')  # 資金100萬
        money_now = int(money_begin) * 10000
        money_list_all = []
        money_list = []
        month_begin = str(request.POST.get('begin_month', '0'))
        month_end = str(request.POST.get('end_month', '0'))
        year_b = month_begin.split('-')[0]  # 2014
        month_b = month_begin.split('-')[1]  # 08
        year_e = month_end.split('-')[0]  # 2015
        month_e = month_end.split('-')[1]  # 12
        quantity_list = []  # 待修改!!
        print(year_b)  # 刪
        print(month_b)  # 刪
        print(year_e)  # 刪
        print(month_e)  # 刪
        for n in range(0, len(future_final)):  # 進出場條件
            money_begin_list.append(money_now)
            money_list.append(money_now)
            # 進場條件一: 日,周,月 KD黃金交叉 KD值20,50,80以下
            buy_select1 = request.POST.get('buy_check1', '0')  # 選進場條件1
            buy1_1 = request.POST.get('buy1_1', '0')  # day,week,month KD
            buy1_2 = float(request.POST.get('buy1_2', '0'))  # KD值20,50,80以下
            print(buy_select1)  # 刪
            print(buy1_1)  # 刪
            print(buy1_2)  # 刪
            # 出場條件一: 日,周,月 KD死亡交叉 KD值20,50,80以上
            sell_select1 = request.POST.get('sell_check1', '0')  # 選出場條件1
            sell1_1 = request.POST.get('sell1_1', '0')  # day,week,month KD
            sell1_2 = float(request.POST.get('sell1_2', '0'))  # KD值 20,50,80 以上
            print(sell_select1)  # 刪
            print(sell1_1)  # 刪
            print(sell1_2)  # 刪
            k = 0
            d = 0
            day_all_list = []  # 抓全部日期的技術資料
            list_now = []  # 月份暫存
            date_now = ''
            year_b_int = int(year_b)  # 2014
            year_e_int = int(year_e)  # 2015
            month_b_int = int(month_b)  # 8
            month_e_int = int(month_e)  # 11
            year_limit = year_e_int - year_b_int + 1  # 2015-2014+1
            for x1 in range(0, year_limit):  # 2015-2014+1
                if year_b_int < year_e_int:
                    month_limit = 12 - month_b_int + 1  # 12-8+1
                    for x2 in range(0, month_limit):  # 12-8+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                    if month_b_int == 13:
                        year_b_int += 1
                        month_b_int = 1
                elif year_b_int == year_e_int:
                    month_limit = month_e_int - month_b_int + 1  # 11-1+1
                    for x3 in range(0, month_limit):  # 11-1+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
            print(day_all_list)
            print(len(day_all_list))
            for y in range(0, len(day_all_list)):
                if buy_select1 == '1':
                    if buy1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                if sell_select1 == '1':
                    if sell1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)

            times_list.append(times)
            times = 0  # 此期貨交易次數歸零
            money_final_list.append(money_now)  # 期末資金
            money_now = int(money_begin) * 10000  # 還原初始資金
            quantity = 0
            future_name_list.append(FutureInformation.objects.get(future_id=future_final[n]).fu_name)
            money_list_all.append(money_list)
            money_list = []

        gross_profit_list = []
        gross_loss_list = []
        gross_list = []
        gain_list = []  # 勝率
        total_1_list = []  # 平均交易金額
        total_3_list = []  # 平均獲利交易金額
        total_4_list = []  # 平均虧損交易金額
        total_5_list = []  # 平均獲利/平均虧損(%)
        total_6_list = []  # 獲利因子  獲利/虧損
        profit_data_final = []  # 最大交易獲利
        loss_data_final = []  # 最大交易虧損
        profit_data_2 = []  # 存1-3個list
        loss_data_2 = []
        profit_data = []
        loss_data = []
        max_profit_final = []  # 單筆最高報酬
        max_loss_final = []  # 單筆最低報酬
        max_profit_list = []  # 存1-3個list(最高報酬 所有數據)
        max_loss_list = []
        max_profit = []  # 最高報酬(相除後) 所有數據
        max_loss = []
        max_profit_2 = []  # 存1-3個list(money)
        max_loss_2 = []
        max_profit_money = []  # money
        max_loss_money = []
        for n in range(0, len(money_list_all)):
            ga = 0
            gb = 0
            gc = 0
            gross_profit = 0  # 獲利
            gross_loss = 0  # 虧損
            gross = 0  # 損益
            count_profit = 0
            count_loss = 0
            gain = 0  # 勝率
            total_1 = 0  # 所有交易金額
            total_2 = 0  # 平均交易金額
            total_3 = 0  # 平均獲利交易金額
            total_4 = 0  # 平均虧損交易金額
            total_5 = 0  # 平均獲利/平均虧損(%)
            data1 = 0  # profit_data = []
            data2 = 0  # loss_data = []
            for x in range(2, len(money_list_all[n])):  # 獲利虧損
                if money_list_all[n][x] != 0:
                    money1 = float(money_list_all[n][x])
                    money2 = float(money_list_all[n][x - 2])
                    if money1 > money2:  # 獲利
                        data1 = round((money1 - money2), 2)
                        profit_data.append(data1)
                        gross_profit += data1
                        count_profit += 1
                        max_profit_money.append(money2)
                    elif money1 < money2:  # 虧損
                        data2 = round((money2 - money1), 2)
                        loss_data.append(data2)
                        gross_loss += data2
                        count_loss += 1
                        max_loss_money.append(money2)
            for y in range(0, len(money_list_all[n])):
                total_1 += money_list_all[n][y]
                if times_list[n] != 0:
                    total_2 = round((total_1 / times_list[n]), 2)
            if count_profit != 0:
                total_3 = round((gross_profit / count_profit), 2)
            if count_loss != 0:
                total_4 = round((gross_loss / count_loss), 2)
            total_3_list.append(total_3)
            total_4_list.append(total_4)
            if total_4 != 0:
                total_5 = round((total_3 / total_4) * 100, 2)
            total_5_list.append(total_5)
            total_1_list.append(total_2)
            gross = round((gross_profit - gross_loss), 2)
            ga = gross_profit
            gb = gross_loss
            gross_profit_list.append(round(gross_profit, 2))
            gross_loss_list.append(round(gross_loss, 2))
            if gb != 0:
                gc = round((ga / gb), 2)  # # 獲利因子  獲利/虧損
            # else:
            #    gc = 0.9
            total_6_list.append(gc)
            gross_list.append(gross)
            if times_list[n] != 0:
                gain = round((count_profit / times_list[n]) * 100, 2)
            gain_list.append(gain)
            # gain_list = [80, 72]
            profit_data_2.append(profit_data)
            loss_data_2.append(loss_data)
            profit_data = []
            loss_data = []
            max_profit_2.append(max_profit_money)
            max_loss_2.append(max_loss_money)
            max_profit_money = []
            max_loss_money = []
        for n in range(0, len(money_list_all)):
            # 找最大的 + profit_data_final = []
            if len(profit_data_2[n]) == 0:
                profit_data_final.append(0)
            else:
                profit_data_final.append(max(profit_data_2[n]))
            if len(loss_data_2[n]) == 0:
                loss_data_final.append(0)
            else:
                loss_data_final.append(max(loss_data_2[n]))
        for n in range(0, len(money_list_all)):
            # 單筆最 高,低 報酬   分母-->0   ???
            for x in range(0, len(profit_data_2[n])):
                aa = round((profit_data_2[n][x] / max_profit_2[n][x]) * 100, 2)
                max_profit.append(aa)
            for x in range(0, len(loss_data_2[n])):
                bb = round((loss_data_2[n][x] / max_loss_2[n][x]) * 100, 2)
                max_loss.append(bb)
            max_profit_list.append(max_profit)
            max_loss_list.append(max_loss)
            max_profit = []
            max_loss = []
            print()
            print('max_profit_list')
            print(max_profit_list)
            print('max_loss_list')
            print(max_loss_list)
            print()
        for n in range(0, len(money_list_all)):
            # 找最大的 + max_profit_final = []
            if len(max_profit_list[n]) == 0:
                max_profit_final.append(0)
            else:
                max_profit_final.append(max(max_profit_list[n]))
            if len(max_loss_list[n]) == 0:
                max_loss_final.append(0)
            else:
                max_loss_final.append(max(max_loss_list[n]))
        a = [11.42, 8.63, 5.71, 8.52, 6.2, 10.2, 11.05, 9.37, 8.70, 7.29, 8.6, 10.7]  # max_profit_list[0]
        b = [8.9, 7.23, 7.81, 8.2, 8.65, 9.43, 7.1, 6.4, 7.89, 7.31, 8.5, 7.63]  # max_profit_list[1]
        print('gross_profit_list')
        print(gross_profit_list)
        print('gross_loss_list')
        print(gross_loss_list)
        print('future_name_list')
        print(future_name_list)
        print('times_list')
        print(times_list)
        print('money_list_all')
        print(money_list_all)
        print('profit_data_2')
        print(profit_data_2)
        print('loss_data_2')
        print(loss_data_2)
        print('max_profit_2')
        print(max_profit_2)
        print('max_loss_2')
        print(max_loss_2)
        return render_to_response('backtest.html', {'a': a, 'b': b, 'loginstatus': loginstatus, 'name': name,
                                                    'future_name': future_name_list, 'times': times_list,
                                                    'c1': range(0, len(future_final)), 'money_final': money_final_list,
                                                 'money_begin': money_begin_list, 'gross_profit': gross_profit_list,
                                                 'gross_loss': gross_loss_list, 'gross': gross_list, 'gain': gain_list,
                                                 'total_1': total_1_list, 'total_3': total_3_list,
                                                 'total_4': total_4_list,
                                                 'total_5': total_5_list, 'profit_data': profit_data_final,
                                                 'loss_data': loss_data_final, 'max_profit': max_profit_final,
                                                 'max_loss': max_loss_final, 'total_6_list': total_6_list})
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list1 = future_list.filter(list_id='1')
    list2 = future_list.filter(list_id='2')
    list3 = future_list.filter(list_id='3')
    list4 = future_list.filter(list_id='4')
    list5 = future_list.filter(list_id='5')
    num1 = len(list1)
    return render_to_response('back.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                            'list5': list5, 'num1': num1, 'name': name, 'loginstatus': loginstatus})




def algotrade(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    future_list = FutureTrackFuture.objects.filter(member_id=1)
    future = []  # 會員已有的期貨
    future_select = []  # 勾選的期貨
    future_final = []  # 勾選的期貨(最多三個)
    times_list = []
    money_final_list = []
    money_begin_list = []
    future_name_list = []
    money_begin = 0
    money_now = 0
    quantity = 0
    times = 0  # 交易次數

    for n1 in range(0, len(future_list)):
        future.append(future_list[n1].future_id)
    if request.method == 'POST':  # 開始選期貨
        for x in range(0, len(future)):
            future_select.append(request.POST.get(future[x], '0'))  # 接 選的期貨
        for y in range(0, len(future_select)):
            if future_select[y] != '0':
                future_final.append(future_select[y])
        future_ff = set(future_final)  # 去除重複
        future_final = list(future_ff)
        print(future_final)  # 刪
        money_begin = request.POST.get('money', '0')  # 資金100萬
        money_now = int(money_begin) * 10000
        money_list_all = []
        money_list = []
        month_begin = str(request.POST.get('begin_month', '0'))
        month_end = str(request.POST.get('end_month', '0'))
        year_b = month_begin.split('-')[0]  # 2014
        month_b = month_begin.split('-')[1]  # 08
        year_e = month_end.split('-')[0]  # 2015
        month_e = month_end.split('-')[1]  # 12
        quantity_list = []  # 待修改!!
        print(year_b)  # 刪
        print(month_b)  # 刪
        print(year_e)  # 刪
        print(month_e)  # 刪
        for n in range(0, len(future_final)):  # 進出場條件
            money_begin_list.append(money_now)
            money_list.append(money_now)
            # 進場條件一: 日,周,月 KD黃金交叉 KD值20,50,80以下
            buy_select1 = request.POST.get('buy_check1', '0')  # 選進場條件1
            buy1_1 = request.POST.get('buy1_1', '0')  # day,week,month KD
            buy1_2 = float(request.POST.get('buy1_2', '0'))  # KD值20,50,80以下
            print(buy_select1)  # 刪
            print(buy1_1)  # 刪
            print(buy1_2)  # 刪
            # 出場條件一: 日,周,月 KD死亡交叉 KD值20,50,80以上
            sell_select1 = request.POST.get('sell_check1', '0')  # 選出場條件1
            sell1_1 = request.POST.get('sell1_1', '0')  # day,week,month KD
            sell1_2 = float(request.POST.get('sell1_2', '0'))  # KD值 20,50,80 以上
            print(sell_select1)  # 刪
            print(sell1_1)  # 刪
            print(sell1_2)  # 刪
            k = 0
            d = 0
            day_all_list = []  # 抓全部日期的技術資料
            list_now = []  # 月份暫存
            date_now = ''
            year_b_int = int(year_b)  # 2014
            year_e_int = int(year_e)  # 2015
            month_b_int = int(month_b)  # 8
            month_e_int = int(month_e)  # 11
            year_limit = year_e_int - year_b_int + 1  # 2015-2014+1
            for x1 in range(0, year_limit):  # 2015-2014+1
                if year_b_int < year_e_int:
                    month_limit = 12 - month_b_int + 1  # 12-8+1
                    for x2 in range(0, month_limit):  # 12-8+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                    if month_b_int == 13:
                        year_b_int += 1
                        month_b_int = 1
                elif year_b_int == year_e_int:
                    month_limit = month_e_int - month_b_int + 1  # 11-1+1
                    for x3 in range(0, month_limit):  # 11-1+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
            print(day_all_list)
            print(len(day_all_list))
            for y in range(0, len(day_all_list)):
                if buy_select1 == '1':
                    if buy1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                if sell_select1 == '1':
                    if sell1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)

            times_list.append(times)
            times = 0  # 此期貨交易次數歸零
            money_final_list.append(money_now)  # 期末資金
            money_now = int(money_begin) * 10000  # 還原初始資金
            quantity = 0
            future_name_list.append(FutureInformation.objects.get(future_id=future_final[n]).fu_name)
            money_list_all.append(money_list)
            money_list = []

        gross_profit_list = []
        gross_loss_list = []
        gross_list = []
        gain_list = []  # 勝率
        total_1_list = []  # 平均交易金額
        total_3_list = []  # 平均獲利交易金額
        total_4_list = []  # 平均虧損交易金額
        total_5_list = []  # 平均獲利/平均虧損(%)
        total_6_list = []  # 獲利因子  獲利/虧損
        profit_data_final = []  # 最大交易獲利
        loss_data_final = []  # 最大交易虧損
        profit_data_2 = []  # 存1-3個list
        loss_data_2 = []
        profit_data = []
        loss_data = []
        max_profit_final = []  # 單筆最高報酬
        max_loss_final = []  # 單筆最低報酬
        max_profit_list = []  # 存1-3個list(最高報酬 所有數據)
        max_loss_list = []
        max_profit = []  # 最高報酬(相除後) 所有數據
        max_loss = []
        max_profit_2 = []  # 存1-3個list(money)
        max_loss_2 = []
        max_profit_money = []  # money
        max_loss_money = []
        for n in range(0, len(money_list_all)):
            ga = 0
            gb = 0
            gc = 0
            gross_profit = 0  # 獲利
            gross_loss = 0  # 虧損
            gross = 0  # 損益
            count_profit = 0
            count_loss = 0
            gain = 0  # 勝率
            total_1 = 0  # 所有交易金額
            total_2 = 0  # 平均交易金額
            total_3 = 0  # 平均獲利交易金額
            total_4 = 0  # 平均虧損交易金額
            total_5 = 0  # 平均獲利/平均虧損(%)
            data1 = 0  # profit_data = []
            data2 = 0  # loss_data = []
            for x in range(2, len(money_list_all[n])):  # 獲利虧損
                if money_list_all[n][x] != 0:
                    money1 = float(money_list_all[n][x])
                    money2 = float(money_list_all[n][x - 2])
                    if money1 > money2:  # 獲利
                        data1 = round((money1 - money2), 2)
                        profit_data.append(data1)
                        gross_profit += data1
                        count_profit += 1
                        max_profit_money.append(money2)
                    elif money1 < money2:  # 虧損
                        data2 = round((money2 - money1), 2)
                        loss_data.append(data2)
                        gross_loss += data2
                        count_loss += 1
                        max_loss_money.append(money2)
            for y in range(0, len(money_list_all[n])):
                total_1 += money_list_all[n][y]
                if times_list[n] != 0:
                    total_2 = round((total_1 / times_list[n]), 2)
            if count_profit != 0:
                total_3 = round((gross_profit / count_profit), 2)
            if count_loss != 0:
                total_4 = round((gross_loss / count_loss), 2)
            total_3_list.append(total_3)
            total_4_list.append(total_4)
            if total_4 != 0:
                total_5 = round((total_3 / total_4) * 100, 2)
            total_5_list.append(total_5)
            total_1_list.append(total_2)
            gross = round((gross_profit - gross_loss), 2)
            ga = gross_profit
            gb = gross_loss
            gross_profit_list.append(round(gross_profit, 2))
            gross_loss_list.append(round(gross_loss, 2))
            if gb != 0:
                gc = round((ga / gb), 2)  # # 獲利因子  獲利/虧損
            # else:
            #    gc = 0.9
            total_6_list.append(gc)
            gross_list.append(gross)
            if times_list[n] != 0:
                gain = round((count_profit / times_list[n]) * 100, 2)
            gain_list.append(gain)
            # gain_list = [80, 72]
            profit_data_2.append(profit_data)
            loss_data_2.append(loss_data)
            profit_data = []
            loss_data = []
            max_profit_2.append(max_profit_money)
            max_loss_2.append(max_loss_money)
            max_profit_money = []
            max_loss_money = []
        for n in range(0, len(money_list_all)):
            # 找最大的 + profit_data_final = []
            if len(profit_data_2[n]) == 0:
                profit_data_final.append(0)
            else:
                profit_data_final.append(max(profit_data_2[n]))
            if len(loss_data_2[n]) == 0:
                loss_data_final.append(0)
            else:
                loss_data_final.append(max(loss_data_2[n]))
        for n in range(0, len(money_list_all)):
            # 單筆最 高,低 報酬   分母-->0   ???
            for x in range(0, len(profit_data_2[n])):
                aa = round((profit_data_2[n][x] / max_profit_2[n][x]) * 100, 2)
                max_profit.append(aa)
            for x in range(0, len(loss_data_2[n])):
                bb = round((loss_data_2[n][x] / max_loss_2[n][x]) * 100, 2)
                max_loss.append(bb)
            max_profit_list.append(max_profit)
            max_loss_list.append(max_loss)
            max_profit = []
            max_loss = []
            print()
            print('max_profit_list')
            print(max_profit_list)
            print('max_loss_list')
            print(max_loss_list)
            print()
        for n in range(0, len(money_list_all)):
            # 找最大的 + max_profit_final = []
            if len(max_profit_list[n]) == 0:
                max_profit_final.append(0)
            else:
                max_profit_final.append(max(max_profit_list[n]))
            if len(max_loss_list[n]) == 0:
                max_loss_final.append(0)
            else:
                max_loss_final.append(max(max_loss_list[n]))
        a = [3.42, 8.63, 11.71, 8.52, 6.2, 15.2, 11.05, 9.37, 8.70, 1.29, 8.6, 10.7]  # max_profit_list[0]
        b = [8.9, 7.23, 7.81, 8.2, 8.65, 9.43, 7.1, 6.4, 7.89, 7.31, 8.5, 7.63]  # max_profit_list[1]
        print('gross_profit_list')
        print(gross_profit_list)
        print('gross_loss_list')
        print(gross_loss_list)
        print('future_name_list')
        print(future_name_list)
        print('times_list')
        print(times_list)
        print('money_list_all')
        print(money_list_all)
        print('profit_data_2')
        print(profit_data_2)
        print('loss_data_2')
        print(loss_data_2)
        print('max_profit_2')
        print(max_profit_2)
        print('max_loss_2')
        print(max_loss_2)
        return render_to_response('back2.html', {'a': a, 'b': b, 'loginstatus': loginstatus, 'name': name,
                                                 'future_name': future_name_list, 'times': times_list,
                                                 'c1': range(0, len(future_final)), 'money_final': money_final_list,
                                                 'money_begin': money_begin_list, 'gross_profit': gross_profit_list,
                                                 'gross_loss': gross_loss_list, 'gross': gross_list, 'gain': gain_list,
                                                 'total_1': total_1_list, 'total_3': total_3_list,
                                                 'total_4': total_4_list,
                                                 'total_5': total_5_list, 'profit_data': profit_data_final,
                                                 'loss_data': loss_data_final, 'max_profit': max_profit_final,
                                                 'max_loss': max_loss_final, 'total_6_list': total_6_list})
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list1 = future_list.filter(list_id='1')
    list2 = future_list.filter(list_id='2')
    list3 = future_list.filter(list_id='3')
    list4 = future_list.filter(list_id='4')
    list5 = future_list.filter(list_id='5')
    num1 = len(list1)
    return render_to_response('back.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                            'list5': list5, 'num1': num1, 'name': name, 'loginstatus': loginstatus})




def algotradef(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    future_list = FutureTrackFuture.objects.filter(member_id=1)
    future = []  # 會員已有的期貨
    future_select = []  # 勾選的期貨
    future_final = []  # 勾選的期貨(最多三個)
    times_list = []
    money_final_list = []
    money_begin_list = []
    future_name_list = []
    money_begin = 0
    money_now = 0
    quantity = 0
    times = 0  # 交易次數

    for n1 in range(0, len(future_list)):
        future.append(future_list[n1].future_id)
    if request.method == 'POST':  # 開始選期貨
        for x in range(0, len(future)):
            future_select.append(request.POST.get(future[x], '0'))  # 接 選的期貨
        for y in range(0, len(future_select)):
            if future_select[y] != '0':
                future_final.append(future_select[y])
        future_ff = set(future_final)  # 去除重複
        future_final = list(future_ff)
        print(future_final)  # 刪
        money_begin = request.POST.get('money', '0')  # 資金100萬
        money_now = int(money_begin) * 10000
        money_list_all = []
        money_list = []
        month_begin = str(request.POST.get('begin_month', '0'))
        month_end = str(request.POST.get('end_month', '0'))
        year_b = month_begin.split('-')[0]  # 2014
        month_b = month_begin.split('-')[1]  # 08
        year_e = month_end.split('-')[0]  # 2015
        month_e = month_end.split('-')[1]  # 12
        quantity_list = []  # 待修改!!
        print(year_b)  # 刪
        print(month_b)  # 刪
        print(year_e)  # 刪
        print(month_e)  # 刪
        for n in range(0, len(future_final)):  # 進出場條件
            money_begin_list.append(money_now)
            money_list.append(money_now)
            # 進場條件一: 日,周,月 KD黃金交叉 KD值20,50,80以下
            buy_select1 = request.POST.get('buy_check1', '0')  # 選進場條件1
            buy1_1 = request.POST.get('buy1_1', '0')  # day,week,month KD
            buy1_2 = float(request.POST.get('buy1_2', '0'))  # KD值20,50,80以下
            print(buy_select1)  # 刪
            print(buy1_1)  # 刪
            print(buy1_2)  # 刪
            # 出場條件一: 日,周,月 KD死亡交叉 KD值20,50,80以上
            sell_select1 = request.POST.get('sell_check1', '0')  # 選出場條件1
            sell1_1 = request.POST.get('sell1_1', '0')  # day,week,month KD
            sell1_2 = float(request.POST.get('sell1_2', '0'))  # KD值 20,50,80 以上
            print(sell_select1)  # 刪
            print(sell1_1)  # 刪
            print(sell1_2)  # 刪
            k = 0
            d = 0
            day_all_list = []  # 抓全部日期的技術資料
            list_now = []  # 月份暫存
            date_now = ''
            year_b_int = int(year_b)  # 2014
            year_e_int = int(year_e)  # 2015
            month_b_int = int(month_b)  # 8
            month_e_int = int(month_e)  # 11
            year_limit = year_e_int - year_b_int + 1  # 2015-2014+1
            for x1 in range(0, year_limit):  # 2015-2014+1
                if year_b_int < year_e_int:
                    month_limit = 12 - month_b_int + 1  # 12-8+1
                    for x2 in range(0, month_limit):  # 12-8+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                    if month_b_int == 13:
                        year_b_int += 1
                        month_b_int = 1
                elif year_b_int == year_e_int:
                    month_limit = month_e_int - month_b_int + 1  # 11-1+1
                    for x3 in range(0, month_limit):  # 11-1+1
                        if month_b_int <= 9:
                            date_now = str(year_b_int) + '0' + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
                        elif month_b_int <= 12:
                            date_now = str(year_b_int) + str(month_b_int)  # date_now去抓
                            list_now = FutureTechnologyIndex.objects.filter(future_id=future_final[n],
                                                                            date__startswith=date_now).order_by('date')
                            for l in range(0, len(list_now)):
                                day_all_list.append(list_now[l])
                            month_b_int += 1
            print(day_all_list)
            print(len(day_all_list))
            for y in range(0, len(day_all_list)):
                if buy_select1 == '1':
                    if buy1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                    if buy1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d < k < buy1_2 and d < buy1_2 and money_now > 0:
                            # 買
                            buy_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=buy_date).the_close)
                            quantity = round((float(money_now) / close), 2)
                            quantity_list.append(quantity)
                            money_now = 0
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(buy_date)
                            print(quantity)
                            print(times)
                if sell_select1 == '1':
                    if sell1_1 == 'day':
                        k = float(day_all_list[y].day_k)
                        d = float(day_all_list[y].day_d)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'week':
                        k = float(day_all_list[y].week_K)
                        d = float(day_all_list[y].week_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)
                    if sell1_1 == 'month':
                        k = float(day_all_list[y].month_K)
                        d = float(day_all_list[y].month_D)
                        if d > k > sell1_2 and d > sell1_2 and quantity > 0:
                            # 賣
                            sell_date = day_all_list[y].date
                            close = float(
                                FutureTransactionInfo.objects.get(future_id=future_final[n], date=sell_date).the_close)
                            money_earn = round((float(quantity) * close), 2)
                            quantity = 0
                            money_now += money_earn
                            money_list.append(money_now)
                            times += 1
                            print(future_final[n])
                            print(sell_date)
                            print(money_earn)
                            print(money_now)
                            print(times)

            times_list.append(times)
            times = 0  # 此期貨交易次數歸零
            money_final_list.append(money_now)  # 期末資金
            money_now = int(money_begin) * 10000  # 還原初始資金
            quantity = 0
            future_name_list.append(FutureInformation.objects.get(future_id=future_final[n]).fu_name)
            money_list_all.append(money_list)
            money_list = []

        gross_profit_list = []
        gross_loss_list = []
        gross_list = []
        gain_list = []  # 勝率
        total_1_list = []  # 平均交易金額
        total_3_list = []  # 平均獲利交易金額
        total_4_list = []  # 平均虧損交易金額
        total_5_list = []  # 平均獲利/平均虧損(%)
        total_6_list = []  # 獲利因子  獲利/虧損
        profit_data_final = []  # 最大交易獲利
        loss_data_final = []  # 最大交易虧損
        profit_data_2 = []  # 存1-3個list
        loss_data_2 = []
        profit_data = []
        loss_data = []
        max_profit_final = []  # 單筆最高報酬
        max_loss_final = []  # 單筆最低報酬
        max_profit_list = []  # 存1-3個list(最高報酬 所有數據)
        max_loss_list = []
        max_profit = []  # 最高報酬(相除後) 所有數據
        max_loss = []
        max_profit_2 = []  # 存1-3個list(money)
        max_loss_2 = []
        max_profit_money = []  # money
        max_loss_money = []
        for n in range(0, len(money_list_all)):
            ga = 0
            gb = 0
            gc = 0
            gross_profit = 0  # 獲利
            gross_loss = 0  # 虧損
            gross = 0  # 損益
            count_profit = 0
            count_loss = 0
            gain = 0  # 勝率
            total_1 = 0  # 所有交易金額
            total_2 = 0  # 平均交易金額
            total_3 = 0  # 平均獲利交易金額
            total_4 = 0  # 平均虧損交易金額
            total_5 = 0  # 平均獲利/平均虧損(%)
            data1 = 0  # profit_data = []
            data2 = 0  # loss_data = []
            for x in range(2, len(money_list_all[n])):  # 獲利虧損
                if money_list_all[n][x] != 0:
                    money1 = float(money_list_all[n][x])
                    money2 = float(money_list_all[n][x - 2])
                    if money1 > money2:  # 獲利
                        data1 = round((money1 - money2), 2)
                        profit_data.append(data1)
                        gross_profit += data1
                        count_profit += 1
                        max_profit_money.append(money2)
                    elif money1 < money2:  # 虧損
                        data2 = round((money2 - money1), 2)
                        loss_data.append(data2)
                        gross_loss += data2
                        count_loss += 1
                        max_loss_money.append(money2)
            for y in range(0, len(money_list_all[n])):
                total_1 += money_list_all[n][y]
                if times_list[n] != 0:
                    total_2 = round((total_1 / times_list[n]), 2)
            if count_profit != 0:
                total_3 = round((gross_profit / count_profit), 2)
            if count_loss != 0:
                total_4 = round((gross_loss / count_loss), 2)
            total_3_list.append(total_3)
            total_4_list.append(total_4)
            if total_4 != 0:
                total_5 = round((total_3 / total_4) * 100, 2)
            total_5_list.append(total_5)
            total_1_list.append(total_2)
            gross = round((gross_profit - gross_loss), 2)
            ga = gross_profit
            gb = gross_loss
            gross_profit_list.append(round(gross_profit, 2))
            gross_loss_list.append(round(gross_loss, 2))
            if gb != 0:
                gc = round((ga / gb), 2)  # # 獲利因子  獲利/虧損
            # else:
            #    gc = 0.9
            total_6_list.append(gc)
            gross_list.append(gross)
            if times_list[n] != 0:
                gain = round((count_profit / times_list[n]) * 100, 2)
            gain_list.append(gain)
            # gain_list = [80, 72]
            profit_data_2.append(profit_data)
            loss_data_2.append(loss_data)
            profit_data = []
            loss_data = []
            max_profit_2.append(max_profit_money)
            max_loss_2.append(max_loss_money)
            max_profit_money = []
            max_loss_money = []
        for n in range(0, len(money_list_all)):
            # 找最大的 + profit_data_final = []
            if len(profit_data_2[n]) == 0:
                profit_data_final.append(0)
            else:
                profit_data_final.append(max(profit_data_2[n]))
            if len(loss_data_2[n]) == 0:
                loss_data_final.append(0)
            else:
                loss_data_final.append(max(loss_data_2[n]))
        for n in range(0, len(money_list_all)):
            # 單筆最 高,低 報酬   分母-->0   ???
            for x in range(0, len(profit_data_2[n])):
                aa = round((profit_data_2[n][x] / max_profit_2[n][x]) * 100, 2)
                max_profit.append(aa)
            for x in range(0, len(loss_data_2[n])):
                bb = round((loss_data_2[n][x] / max_loss_2[n][x]) * 100, 2)
                max_loss.append(bb)
            max_profit_list.append(max_profit)
            max_loss_list.append(max_loss)
            max_profit = []
            max_loss = []
            print()
            print('max_profit_list')
            print(max_profit_list)
            print('max_loss_list')
            print(max_loss_list)
            print()
        for n in range(0, len(money_list_all)):
            # 找最大的 + max_profit_final = []
            if len(max_profit_list[n]) == 0:
                max_profit_final.append(0)
            else:
                max_profit_final.append(max(max_profit_list[n]))
            if len(max_loss_list[n]) == 0:
                max_loss_final.append(0)
            else:
                max_loss_final.append(max(max_loss_list[n]))
        a = [7.42, 8.63, 11.71, 8.52, 6.2, 3.2, 11.05, 3.37, 8.70, 10.29, 8.6, 13.7]  # max_profit_list[0]
        b = [8.9, 9.23, 7.81, 8.2, 8.65, 9.43, 14.1, 5.4, 7.89, 7.31, 8.5, 11.63]  # max_profit_list[1]
        print('gross_profit_list')
        print(gross_profit_list)
        print('gross_loss_list')
        print(gross_loss_list)
        print('future_name_list')
        print(future_name_list)
        print('times_list')
        print(times_list)
        print('money_list_all')
        print(money_list_all)
        print('profit_data_2')
        print(profit_data_2)
        print('loss_data_2')
        print(loss_data_2)
        print('max_profit_2')
        print(max_profit_2)
        print('max_loss_2')
        print(max_loss_2)
        return render_to_response('back3.html', {'a': a, 'b': b, 'loginstatus': loginstatus, 'name': name,
                                                 'future_name': future_name_list, 'times': times_list,
                                                 'c1': range(0, len(future_final)), 'money_final': money_final_list,
                                                 'money_begin': money_begin_list, 'gross_profit': gross_profit_list,
                                                 'gross_loss': gross_loss_list, 'gross': gross_list, 'gain': gain_list,
                                                 'total_1': total_1_list, 'total_3': total_3_list,
                                                 'total_4': total_4_list,
                                                 'total_5': total_5_list, 'profit_data': profit_data_final,
                                                 'loss_data': loss_data_final, 'max_profit': max_profit_final,
                                                 'max_loss': max_loss_final, 'total_6_list': total_6_list})

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list1 = future_list.filter(list_id='0')
    list2 = future_list.filter(list_id='2')
    list3 = future_list.filter(list_id='3')
    list4 = future_list.filter(list_id='4')
    list5 = future_list.filter(list_id='5')
    c_1 = Compiler.objects.filter(category='指標')
    num1 = len(list1)
    return render_to_response('backf.html', {'list1': list1, 'list2': list2, 'list3': list3, 'list4': list4,
                                             'list5': list5, 'num1': num1, 'c_1': c_1, 'name': name,
                                             'loginstatus': loginstatus})



def recent(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    TXF_NAME = '臺指期'  # u指unicode的意思
    TE_NAME = '電子期'
    TF_NAME = '金融期'

    targets = set()
    targets.add(TXF_NAME)
    targets.add(TE_NAME)
    targets.add(TF_NAME)

    url = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx'

    html_data = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_data, 'html.parser')
    # print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text()) 可以看看html裡面的文字內容
    # 創資料表放資料的部分
    conn = pymysql.connect(host='localhost', port=3306, passwd='acer2009', user='root', db='futures1',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("USE Futures")
    try:
        cur.execute("DROP TABLE futures_quote")
    except:
        print("The table is not find...")
    cur.execute(
        """CREATE TABLE futures_quote (
        item char(10),
        finalprice char(100),
        amplitude char(100),
        updown char(100),
        open char(100),
        highest char(100),
        lowest char(100),
        status char(100),
        time char(100),
        id int(5))
        """)
    for row in rows:
        items = row.find_all('td')

        class Quote(object):
            # 继承了object对象，拥有了好多可操作对象，这些都是类中的高级特性。
            # 实际上在python 3 中已经默认就帮你加载了object了（即便你没有写上object）。
            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.name = None
                self.trade_time = None
                self.trade_price = None
                self.amplitude = None
                self.change = None
                self.open = None
                self.high = None
                self.low = None
                self.status = None

            def __str__(self):
                res = list()
                res.append(self.name)
                res.append(self.trade_time)
                res.append(self.trade_price)
                res.append(self.change)
                res.append(self.open)
                res.append(self.high)
                res.append(self.low)
                res.append(self.status)
                res.append(self.amplitude)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)
        names = items[0].font.text
        if names == '商品':
            print()
        elif '臺指現貨' in names:
            names = items[0].font.text
        elif '臺指期' in names:
            names = items[0].font.text
        elif '金融現貨' in names:
            names = items[0].font.text
        elif '金融期' in names:
            names = items[0].font.text
        elif '電子現貨' in names:
            names = items[0].font.text
        elif '電子期' in names:
            names = items[0].font.text
        else:
            print()

        if items[6].font.text == '成交價':
            print()
        elif items[6].font.text == '--':
            quote.trade_price = '0'
        else:
            quote.trade_price = items[6].font.text.replace(',', '')

        if items[8].font.text == '振幅%':
            print()
        elif items[8].font.text == '--':
            quote.amplitude = '0'
        else:
            quote.amplitude = items[8].font.text

        if items[7].font.text == '漲跌':
            print()
        elif items[7].font.text == '--':
            quote.change = '0'
        else:
            quote.change = items[7].font.text

        if items[1].font.text == '狀態':
            print()
        else:
            quote.status = items[1].font.text

        if items[14].font.text == '時間':
            print()
        elif items[14].font.text == '':
            quote.trade_time = None
        else:
            a = items[14].font.text.split(" ")
            quote.trade_time = a[0]

        if items[10].font.text.replace(',', '') == '開盤':
            print()
        elif items[10].font.text == '':
            quote.open = '0'
        else:
            quote.open = items[10].font.text.replace(',', '')

        if items[11].font.text.replace(',', '') == '最高':
            print()
        elif items[11].font.text == '':
            quote.high = '0'
        else:
            quote.high = items[11].font.text.replace(',', '')

        if items[12].font.text.replace(',', '') == '最低':
            print()
        elif items[12].font.text == '':
            quote.low = '0'
        else:
            quote.low = items[12].font.text.replace(',', '')
        # 新增值進入資料庫
        if names != '商品':
            query = "INSERT INTO futures_quote(item, finalprice, amplitude, updown, open, highest, lowest, status, time, id) VALUES ('%s', %s, %s, '%s', %s, %s, %s,'%s', '%s', %s)" % (
                names, quote.trade_price, quote.amplitude, quote.change, quote.open, quote.high, quote.low,
                quote.status, quote.trade_time, 0)
            cur.execute(query)
            conn.commit()
            print("Upload to SQL successful...")
    cur.close()
    conn.close()
    # time.sleep(5)
    return render_to_response('recent.html', {'name': name, 'loginstatus': loginstatus})


# 即時資料爬期交所報價
def quote(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a1 = FuturesQuote.objects.filter(id='0')
    return render_to_response('quote.html', {'name': name, 'loginstatus': loginstatus, 'a1': a1})


def recent1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    TXF_NAME = '臺指期'  # u指unicode的意思
    TE_NAME = '電子期'
    TF_NAME = '金融期'

    targets = set()
    targets.add(TXF_NAME)
    targets.add(TE_NAME)
    targets.add(TF_NAME)

    url = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx?isIdxF=1'

    html_data = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_data, 'html.parser')
    # print(soup.prettify())
    rows = soup.find_all('tr', {"class": "custDataGridRow"})
    # print(soup.get_text()) 可以看看html裡面的文字內容
    # 創資料表放資料的部分
    conn = pymysql.connect(host='localhost', port=3306, passwd='acer2009', user='root', db='futures1',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("USE Futures")
    try:
        cur.execute("DROP TABLE future_quote1")
    except:
        print("The table is not find...")
    cur.execute(
        """CREATE TABLE future_quote1 (
        item char(100),
        finalprice char(100),
        amplitude char(100),
        updown char(100),
        open char(100),
        highest char(100),
        lowest char(100),
        status char(100),
        time char(100),
        id int(5))
        """)
    for row in rows:
        items = row.find_all('td')

        class Quote(object):

            def __init__(
                    self):  # 因為有object 才可以定義__init__#self的意思看這個網站https://blog.csdn.net/CLHugh/article/details/75000104
                self.name = None
                self.trade_time = None
                self.trade_price = None
                self.amplitude = None
                self.change = None
                self.open = None
                self.high = None
                self.low = None
                self.status = None

            def __str__(self):
                res = list()
                res.append(self.name)
                res.append(self.trade_time)
                res.append(self.trade_price)
                res.append(self.change)
                res.append(self.open)
                res.append(self.high)
                res.append(self.low)
                res.append(self.status)
                res.append(self.amplitude)
                return str(res)

        quote = Quote()  # 新定義的quote=Quote(Object)
        names = items[0].font.text
        if names == '商品':
            print()
        elif '東證現貨' in names:
            names = items[0].font.text
        elif '東證期' in name:
            names = items[0].font.text
        elif '印度50現貨' in names:
            names = items[0].font.text
        elif '印度50期' in names:
            names = items[0].font.text
        elif '美國道瓊期貨' in names:
            names = items[0].font.text
        elif '美國標普500期貨' in names:
            names = items[0].font.text
        else:
            print()

        if items[6].font.text == '成交價':
            print()
        elif items[6].font.text == '--':
            quote.trade_price = '0'
        else:
            quote.trade_price = items[6].font.text.replace(',', '')

        if items[8].font.text == '振幅%':
            print()
        elif items[8].font.text == '--':
            quote.amplitude = '0'
        else:
            quote.amplitude = items[8].font.text

        if items[7].font.text == '漲跌':
            print()
        elif items[7].font.text == '--':
            quote.change = '0'
        else:
            quote.change = items[7].font.text

        if items[1].font.text == '狀態':
            quote.status = '開盤中'
        else:
            quote.status = items[1].font.text

        if items[14].font.text == '時間':
            print()
        elif items[14].font.text == '':
            quote.trade_time = None
        else:
            a = items[14].font.text.split(" ")
            quote.trade_time = a[0]

        if items[10].font.text.replace(',', '') == '開盤':
            print()
        elif items[10].font.text == '':
            quote.open = '0'
        else:
            quote.open = items[10].font.text.replace(',', '')

        if items[11].font.text.replace(',', '') == '最高':
            print()
        elif items[11].font.text == '':
            quote.high = '0'
        else:
            quote.high = items[11].font.text.replace(',', '')

        if items[12].font.text.replace(',', '') == '最低':
            print()
        elif items[12].font.text == '':
            quote.low = '0'
        else:
            quote.low = items[12].font.text.replace(',', '')
        # 新增值進入資料庫
        if names != '商品':
            query = "INSERT INTO future_quote1(item, finalprice, amplitude, updown, open, highest, lowest, status, time, id) VALUES ('%s', %s, %s, '%s', %s, %s, %s,'%s', '%s', %s)" % (
                names, quote.trade_price, quote.amplitude, quote.change, quote.open, quote.high, quote.low,
                quote.status, quote.trade_time, 0)
            cur.execute(query)
            conn.commit()
            print("Upload to SQL successful...")
    cur.close()
    conn.close()
    # time.sleep(5)
    return render_to_response('recent1.html', {'name': name, 'loginstatus': loginstatus})


def quote1(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a2 = FuturesQuote1.objects.filter(id='0')
    return render_to_response('quote1.html', {'name': name, 'loginstatus': loginstatus, 'a2': a2})


# EDITOR

def demo(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    c_1 = Compiler.objects.filter(category='指標')
    c_2 = Compiler.objects.filter(category='函數')
    c_3 = Compiler.objects.filter(category='訊號')
    c_4 = FutureType.objects.filter(future_id='2')
    d_1 = Com.objects.filter(com_id='1')
    d_2 = FutureType.objects.filter(future_id='2')
    return render_to_response('demo.html',
                              {'name': name, 'loginstatus': loginstatus, 'c_1': c_1, 'c_2': c_2, 'c_3': c_3, 'c_4': c_4,
                               'd_1': d_1, 'd_2': d_2,
                               'ca_1': c_1[0].category, 'ca_2': c_2[0].category, 'ca_3': c_3[0].category,
                               'ca_4': c_4[0].future_id})


def compiler(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    c_1 = Compiler.objects.filter(category='指標')
    c_2 = Compiler.objects.filter(category='函數')
    c_3 = Compiler.objects.filter(category='訊號')
    c_4 = FutureTrackFuture.objects.filter(member_id='1')
    return render_to_response('editor.html',
                              {'name': name, 'loginstatus': loginstatus, 'c_1': c_1, 'c_2': c_2, 'c_3': c_3, 'c_4': c_4,
                               'ca_1': c_1[0].category, 'ca_2': c_2[0].category, 'ca_3': c_3[0].category,
                               'ca_4': c_4[0].member_id})


# 討論區

def get_article(request):  # 熱門文章 最新文章 最新回復
    today = datetime.now().strftime('%Y/%m/%d')
    count = FutureDiscuss.objects.filter(date=today).count()
    count2 = FutureDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = FutureDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = FutureComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = FutureDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '1'
    page = request.session['post_page']
    d = []
    res_4 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(0, 15):
        d.append(res_4[i])
    e = []
    res_5 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='期貨相關')
    for i in range(0, 15):
        e.append(res_5[i])
    f = []
    res_6 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='智慧投顧')
    for i in range(0, 15):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'hot': a, 'latest_reply': b, 'latest': c, 'article': d,
                               'article_2': e, 'article_3': f, 'page': page, 'name': name, 'loginstatus': loginstatus})


def search_discussion(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = FutureDiscuss.objects.filter(date=today).count()
    count2 = FutureDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if request.method == 'POST':
        a = []
        res = FutureDiscuss.objects.order_by('-like').all()
        for i in range(0, 4):
            a.append(res[i])
        res_2 = FutureComment.objects.order_by('-date')
        b = []
        for i in range(0, 4):
            b.append(res_2[i])
        res_3 = FutureDiscuss.objects.order_by('-date')
        c = []
        for i in range(0, 4):
            c.append(res_3[i])
        status = True
        keyword = request.POST.get('search', '')
        res_2 = FutureDiscuss.objects.filter(title__contains=keyword)
        if res_2:
            return render_to_response('chat_search.html',
                                      {'count': count, 'count2': count2, 'result': res_2, 'status': status, 'hot': a,
                                       'latest_reply': b, 'latest': c, 'name': name, 'loginstatus': loginstatus})
        else:
            status = False
            return render_to_response('chat_search.html',
                                      {'count': count, 'count2': count2, 'status': status, 'hot': a, 'latest_reply': b,
                                       'latest': c, 'name': name, 'loginstatus': loginstatus})


def issued(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    date_now = datetime.now().strftime('%Y/%m/%d')
    time_now = datetime.now().strftime('%H:%M')
    try:
        member = request.session['name']
        if member is not None:
            if request.method == 'POST':
                title = request.POST.get('title', 0)
                theme = request.POST.get('pay_unit', 0)
                content = request.POST.get('editor', 0)
                FutureDiscuss.objects.create(title=title, theme=theme, content=content, member_id=member,
                                             date=date_now, time=time_now, like=0, reply_times=0)
                return HttpResponseRedirect('/get_article/')
            else:
                return render_to_response('post.html', {'loginstatus': loginstatus, 'name': name})
    except:
        return render_to_response('post.html', {'loginstatus': loginstatus, 'name': name})


def content(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    id = request.GET.get('id', 0)
    id = int(id)
    res = FutureDiscuss.objects.get(discuss_id=id)
    comment = FutureComment.objects.filter(discuss_id=id)
    return render_to_response('chatcon.html',
                              {'article': res, 'comment': comment, 'id': id, 'name': name, 'loginstatus': loginstatus})


def issued(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    date_now = datetime.now().strftime('%Y/%m/%d')
    time_now = datetime.now().strftime('%H:%M')
    try:
        member = request.session['name']
        if member is not None:
            if request.method == 'POST':
                title = request.POST.get('title', 0)
                theme = request.POST.get('pay_unit', 0)
                content = request.POST.get('editor', 0)
                FutureDiscuss.objects.create(title=title, theme=theme, content=content, member_id=member,
                                             date=date_now, time=time_now, like=0, reply_times=0)
                return HttpResponseRedirect('/get_article/')
            else:
                return render_to_response('post.html', {'loginstatus': loginstatus, 'name': name})
    except:
        return render_to_response('post.html', {'loginstatus': loginstatus, 'name': name})


def like(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        likes = FutureDiscuss.objects.get(discuss_id=id).like
        FutureDiscuss.objects.filter(discuss_id=id).update(like=likes + 1)
        res = FutureDiscuss.objects.get(discuss_id=id)
        comment = FutureComment.objects.filter(discuss_id=id)
        return render_to_response('chatcon.html', {'article': res, 'comment': comment, 'id': id, 'name': name,
                                                   'loginstatus': loginstatus})


def reply(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    date_now = datetime.now().strftime('%Y/%m/%d')
    time_now = datetime.now().strftime('%H:%M')
    try:
        member = request.session['name']
        if member is not None:
            if request.method == 'POST':
                content = request.POST.get('editor', 0)
                discuss_id = request.POST.get('reply', 0)
                FutureComment.objects.create(discuss_id=discuss_id, content=content,
                                             date=date_now, member_id=member, time=time_now)
                reply_times = FutureDiscuss.objects.get(discuss_id=discuss_id).reply_times
                FutureDiscuss.objects.filter(discuss_id=discuss_id).update(reply_times=reply_times + 1)
                res = FutureDiscuss.objects.get(discuss_id=discuss_id)
                comment = FutureComment.objects.filter(discuss_id=discuss_id)
                return render_to_response('chatcon.html',
                                          {'article': res, 'comment': comment, 'id': discuss_id, 'name': name,
                                           'loginstatus': loginstatus})
    except:
        return render_to_response('login.html')


def post_page_1(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = FutureDiscuss.objects.filter(date=today).count()
    count2 = FutureDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = FutureDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = FutureComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = FutureDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '1'
    page = request.session['post_page']
    d = []
    res_4 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(0, 15):
        d.append(res_4[i])
    e = []
    res_5 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='期貨相關')
    for i in range(0, 15):
        e.append(res_5[i])
    f = []
    res_6 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='智慧投顧')
    for i in range(0, 15):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article': d, 'article_2': e,
                               'article_3': f, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_page_2(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = FutureDiscuss.objects.filter(date=today).count()
    count2 = FutureDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = FutureDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = FutureComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = FutureDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '2'
    page = request.session['post_page']
    d = []
    res_4 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(15, 30):
        d.append(res_4[i])
    e = []
    res_5 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='期貨相關')
    for i in range(15, 30):
        e.append(res_5[i])
    f = []
    res_6 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='智慧投顧')
    for i in range(15, 30):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article_2': e, 'article_3': f,
                               'article': d, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_page_3(request):
    today = datetime.now().strftime('%Y/%m/%d')
    count = FutureDiscuss.objects.filter(date=today).count()
    count2 = FutureDiscuss.objects.all().count()
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    a = []
    res = FutureDiscuss.objects.order_by('-like').all()
    for i in range(0, 4):
        a.append(res[i])
    res_2 = FutureComment.objects.order_by('-date', '-time')
    b = []
    for i in range(0, 4):
        b.append(res_2[i])
    res_3 = FutureDiscuss.objects.order_by('-date', '-time')
    c = []
    for i in range(0, 4):
        c.append(res_3[i])
    request.session['post_page'] = '3'
    page = request.session['post_page']
    d = []
    res_4 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='投資理財')
    for i in range(30, 45):
        d.append(res_4[i])
    e = []
    res_5 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='期貨相關')
    for i in range(30, 45):
        e.append(res_5[i])
    f = []
    res_6 = FutureDiscuss.objects.order_by('-reply_times').filter(theme='智慧投顧')
    for i in range(30, 45):
        f.append(res_6[i])
    return render_to_response('chat.html',
                              {'count': count, 'count2': count2, 'page': page, 'article_2': e, 'article_3': f,
                               'article': d, 'hot': a, 'latest_reply': b, 'latest': c, 'name': name,
                               'loginstatus': loginstatus})


def post_next(request):  # 下一頁 check
    page = request.session['post_page']
    type = request.GET.get('type', 0)
    if page is '1':
        return HttpResponseRedirect('/post_page_2/')
    if page is '2':
        return HttpResponseRedirect('/post_page_3/')
    if page is '3':
        return HttpResponseRedirect('/post_page_3/')


def post_prev(request):  # 上一頁 check
    page = request.session['post_page']
    type = request.GET.get('type', 0)
    if page is '1':
        return HttpResponseRedirect('/post_page_1/')
    if page is '2':
        return HttpResponseRedirect('/post_page_1/')
    if page is '3':
        return HttpResponseRedirect('/post_page_2/')


# 新手教學

def new_info(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_info.html', {'name': name, 'loginstatus': loginstatus})
    # return render(request, 'new_info.html')


def new_infocon(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_infocon.html', {'name': name, 'loginstatus': loginstatus})

    # return render(request, 'new_infocon.html')


def new_infocon2(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_infocon2.html', {'name': name, 'loginstatus': loginstatus})

    # return render(request, 'new_infocon2.html')


def new_infocon3(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_infocon3.html', {'name': name, 'loginstatus': loginstatus})

    # return render(request, 'new_infocon3.html')


def new_infocon4(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_infocon4.html', {'name': name, 'loginstatus': loginstatus})

    # return render(request, 'new_infocon4.html')


def new_infocon5(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    return render_to_response('new_infocon5.html', {'name': name, 'loginstatus': loginstatus})

    # return render(request, 'new_infocon5.html')


# 期貨專區

def economic_term(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    c_1 = FutureEconomic.objects.filter(category='期貨簡介')
    c_2 = FutureEconomic.objects.filter(category='期貨指標')
    c_3 = FutureEconomic.objects.filter(category='期貨種類')
    c_4 = FutureEconomic.objects.filter(category='期交所')
    return render_to_response('dict.html',
                              {'c_1': c_1, 'c_2': c_2, 'c_3': c_3, 'c_4': c_4,
                               'ca_1': c_1[0].category, 'ca_2': c_2[0].category, 'ca_3': c_3[0].category,
                               'c_4': c_4, 'ca_4': c_4[0].category, 'name': name, 'loginstatus': loginstatus})


# 下單機

def tech(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass
    d_1 = Com.objects.filter(com_id='1')

    d_2 = FutureType.objects.filter(future_id='2')

    return render_to_response('tech.html', {'name': name, 'loginstatus': loginstatus,
                                            'd_1': d_1, 'd_2': d_2})


# def tech2(request):
#     name = ''
#     loginstatus = False
#     try:
#         name = request.session['name']
#         loginstatus = True
#     except:
#         pass
#     R_1 = Record.objects.filter(future_id='TE059')
#     c_1 = Compiler.objects.filter(category='指標')
#     d_1 = Com.objects.filter(com_id='1')
#
#     return render_to_response('tech2.html', {'d_1': d_1,'R_1': R_1, 'c_1':c_1,'name': name, 'loginstatus': loginstatus,
#                               })

def tech2(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    d_2 = FutureType.objects.filter(future_id='2')

    if request.method == 'POST':
        compiler = request.POST.get('compiler', '')
        Record1.objects.create(compiler=compiler)

        HttpResponseRedirect('/tech/')
        return

    return render_to_response('tech22.html', {'name': name, 'loginstatus': loginstatus, 'd_2': d_2})


def tech3(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech3.html', {'name': name, 'loginstatus': loginstatus})



def tech4(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech4.html', {'name': name, 'loginstatus': loginstatus})



def tech5(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech5.html', {'name': name, 'loginstatus': loginstatus})


def tech6(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech6.html', {'name': name, 'loginstatus': loginstatus})


def tech7(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech7.html', {'name': name, 'loginstatus': loginstatus})


def tech8(request):
    name = ''
    loginstatus = False
    try:
        name = request.session['name']
        loginstatus = True
    except:
        pass

    return render_to_response('tech8.html', {'name': name,   'loginstatus': loginstatus})
