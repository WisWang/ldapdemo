from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from ldap_tool import LdapTool
from django.contrib.auth.models import User


def index(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'home.html')


def django_python3_ldap_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print "username,password:%s %s" % (username, password)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                err_msg = 'username and password is wrong'
        else:
            err_msg = 'username and password can not be empty'
        return render(request, 'ldap_auth.html', {'err_msg':err_msg,})
    else:
        return render(request, 'ldap_auth.html')


def my_ldap_auth(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            ldaptool = LdapTool()
            res = ldaptool.check_pass(username,password)
            if res == 0:
                user = User.objects.filter(username=username)
                if not user:
                    u = User.objects.create_user(username=username, password="asdf1234")
                else:
                    u = user[0]
                    u.set_password("asdf1234")
                u.save()
                user = authenticate(username=username, password='asdf1234')
                login(request, user)
                return HttpResponseRedirect('/')
            elif res == 1:
                err_msg = "username not found"
            else:
                err_msg = "password wrong"
            return render(request, 'ldap_auth.html', {'err_msg': err_msg, })
        else:
            err_msg = 'username and password can not be empty'
            return render(request,'ldap_auth.html', {'err_msg':err_msg, })
    else:
        return render(request, 'ldap_auth.html')


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")