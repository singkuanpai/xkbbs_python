# coding=utf-8
from django.template import loader,Context
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response,RequestContext
import datetime
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from django import forms
from django.db import connection
from mybbs.models import threads,posts,threaduvs


from mybbs.models import threads,posts,members

def about(request):
    t=loader.get_template("about.html")
    c=Context({'':''})
    return HttpResponse(t.render(c))

def post_write(request):
    ip=request.META['REMOTE_ADDR']
    onlines=set_bbs_cookies(request,ip)
    youragent=request.META['HTTP_USER_AGENT']
    if youragent is None:
        youragent=request.META.get('HTTP_USER_AGENT','')
    t=loader.get_template("post_write.html")
    c=Context({'onlines':onlines,'yourip':ip,'youragent':youragent})
    return HttpResponse(t.render(c))

def post_view(request,tid):
    tid=int(tid)
    if tid< 1:
        return 0
    else:
        xvar=threads.objects.get(id=tid)
        ip=request.META['REMOTE_ADDR']
        onlines=set_bbs_cookies(request,ip)
        youragent=request.META['HTTP_USER_AGENT']
        if youragent is None:
            youragent=request.META.get('HTTP_USER_AGENT','')
        debuginfo=(updateuv(ip=ip,threads_id=tid))
        page=int(request.GET.get('page','1'))
        dvars=post_view_list(tid,page)
        vvars=dvars['v']
        page_range=dvars['p']
        #print('')
        #print(p for p in vvars)
        t=loader.get_template("post_view.html")
        c=Context({'xvar':xvar,'yourip':ip,'youragent':youragent,'vvars':vvars,"page_range":page_range,'onlines':onlines})
        return HttpResponse(t.render(c))

def updateuv(ip,threads_id):
    tid=int(threads_id)
    if tid>0:
        psc=threaduvs.objects.filter(threads_id=threads_id,ip=ip)[:1].count()
        pm=threads.objects.values_list('uv','pv').filter(id=tid)
        pms=threads.objects.get(id=tid) 
               
        if pm.exists():
            pms.pv=int(pm[0][1])+1
            pms.save()

            if psc>0:
                #'this is the same user'
                pass
            else:
                '''
                pss=threaduvs(
                   username='admin',
                   ip=ip,
                   uvnum=1,
                   threads_id=threads_id,
                   members_id=1
                   )
                pss.save
                pms1=threads.objects.get(id=tid)
                pms1.uv=int(pms1.uv)+1
                pms1.save
                '''
                sql="insert into mybbs_threaduvs(username,ip,uvnum,threads_id,members_id)values('','"+ip+"',1,"+str(tid)+",1)"
                cursor=connection.cursor()
                cursor.execute(sql)
                sqlu="update mybbs_threads set uv=uv+1 where id="+str(tid)
                cursor.execute(sqlu)                

def post_list(request):
    ip=request.META['REMOTE_ADDR']
    onlines=set_bbs_cookies(request,ip)
    ip=request.META['REMOTE_ADDR'] 
    youragent=request.META['HTTP_USER_AGENT']
    if youragent is None:
        youragent=request.META.get('HTTP_USER_AGENT','')
    xlist = threads.objects.all()
    paginator=Paginator(xlist,8)
   
    after_range_num=5
    befor_range_num=4

    try:
        page=int(request.GET.get('page','1'))
        if page<1:
            page=1
    except ValueError:
        page=1

    try:
        xvars=paginator.page(page)
    except(EmptyPage,InvalidPage):
        xvars=paginator.page(paginator.num_pages)
    
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]


    return render_to_response('post_list.html',{"xvars":xvars,"page_range":page_range,"onlines":onlines,'yourip':ip,'youragent':youragent})


#@csrf_protect
def post_writeok(request):
    c={}
    #req=(csrf(request))
    if request.method=='POST':
        #form=ContactForm((request.POST))
        title=request.POST.get('title','')
        message=title
    else:
        message='you are wrong.'
    
    if title:
        newthread=threads(
            title=request.POST.get('title',''),
            content=request.POST.get('content',''),
            username=request.POST.get('username',''),
            ip=request.META['REMOTE_ADDR'],
            uv=1,
            replytime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            members_id=1,
            )
        newthread.save()
    
    posttime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    t=loader.get_template("post_writeok.html")
    c=RequestContext(request,{'message':message,})
    return HttpResponse(t.render(c))
    #return render_to_response('post_writeok.html',{"message":message},context_instance=RequestContext(request))


def reply_writeok(request):
    if request.method=='POST':
        tid=int(request.POST.get('tid',''))
        if tid<1:
            raise forms.ValidationError( 'tid is error!')
        username=request.POST.get('username','')
        if len(username)<3:
            raise forms.ValidationError('the username  length must more than 3')
        content=request.POST.get('content','')
        if len(content)<3:
            raise forms.ValidationError('the content length must more than 3')

        newposts=posts(
            title='',
            content=request.POST.get('content',''),
            username=request.POST.get('username',''),
            ip=request.META['REMOTE_ADDR'],
            # replytime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            members_id=1,
            threads_id=tid,
            browsertype = request.META.get('HTTP_USER_AGENT',None),
            )
        newposts.save()
        replytimes=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql="update mybbs_threads set renum=renum+1, replytime='"+str(replytimes)+ "'  where id="+str(tid)
        cursor=connection.cursor()
        cursor.execute(sql)
        #threads.objects.filter(id=tid).update(replytime=replytime,renum=renums+1)
        return HttpResponseRedirect('/view/tid/'+str(tid))


def post_view_list(tid,page=1):
    if int(tid)<1:
        raise forms.ValidationError('valid thread!')
    vlist = posts.objects.filter(threads_id=tid)
    paginator=Paginator(vlist,8)
   
    after_range_num=5
    befor_range_num=4

    try:
        #page=int(request.GET.get('page','1'))
        if page<1:
            page=1
    except ValueError:
        page=1

    try:
        vvars=paginator.page(page)
    except(EmptyPage,InvalidPage):
        vvars=paginator.page(paginator.num_pages)
    
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]

	viewd={}
	viewd={'v':vvars,'p':page_range}
        return viewd
    
def set_bbs_cookies(request,ip):
    anow=datetime.datetime.now()
    strnow=anow.strftime("%Y-%m-%d %H:%M:%S")
    ages=datetime.datetime.now()+datetime.timedelta(minutes=5)
    response=HttpResponse()
    response.set_cookie(ip,ip,expires=ages)
    dt = datetime.datetime.now() + datetime.timedelta(days = 120)
    cookielist=[]
    try:
        cookielist=request.session['cookielist']
    except KeyError:
        pass
       
    for i in range(len(cookielist)):
        try:
            if request.COOKIES[cookielist[i]] is None:
                cookielist.pop(i)
            else:
                pass
        except KeyError:
            pass
    
    cookielist.append(ip)
    cookielist=list(set(cookielist))
    request.session['cookielist']=cookielist
    return len(cookielist)
    #return response

def get_bbs_cookies():
    pass
