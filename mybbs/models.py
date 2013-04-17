from django.db import models
from django.contrib import admin


class members(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    regtime=models.DateTimeField(blank=True)
    lastlogintime=models.DateTimeField(blank=True)
    replytime=models.DateTimeField(blank=True)
    sex=models.IntegerField(default=0)
    ip=models.IPAddressField()

class threads(models.Model): 
    title = models.CharField(max_length=100) 
    content = models.TextField()    
    username = models.CharField(max_length=30)
    posttime=models.DateTimeField(auto_now_add=True)
    modifytime=models.DateTimeField(auto_now=True)
    replytime=models.DateTimeField()
    uv=models.IntegerField(default=0)
    pv=models.IntegerField(default=0)
    renum=models.IntegerField(default=0)
    istop=models.BooleanField(default=0)
    ip=models.IPAddressField()
    members=models.ForeignKey(members)
    browsertype=models.CharField(max_length=200,blank=True)

class posts(models.Model): 
    title = models.CharField(max_length=100) 
    content = models.TextField()    
    username = models.CharField(max_length=30)
    posttime=models.DateTimeField(auto_now_add=True)
    modifytime=models.DateTimeField(auto_now=True)
    threads=models.ForeignKey(threads)
    browsertype=models.CharField(max_length=200)
    members=models.ForeignKey(members)
    ip=models.IPAddressField()
     
class threaduvs(models.Model):
    username=models.CharField(max_length=30,blank=True)
    ip=models.IPAddressField()
    uvnum=models.IntegerField(default=0)
    threads=models.ForeignKey(threads)
    members=models.ForeignKey(members,blank=True,null=True,on_delete=models.SET_NULL)

class threadsAdmin(admin.ModelAdmin): 
    list_display = ("title", "username","posttime")

class postsAdmin(admin.ModelAdmin): 
    list_display = ("title", "username")

class membersAdmin(admin.ModelAdmin): 
    list_display = ("username","email")


admin.site.register(threads,threadsAdmin)
admin.site.register(posts,postsAdmin)
admin.site.register(members,membersAdmin)
