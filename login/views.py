from django.shortcuts import render,redirect
from .models import User,ConfirmString
from .forms import UserForm,RegisterForm
# Create your views here.
from util.base import hash_code,make_confirm_string,send_email
from datetime import  datetime,timedelta
from django.conf import settings
def index(request): #首页
    pass
    return render(request, 'login/index.html')
# def login(request):#登录
#     if request.method == "POST":
#         name = request.POST.get('username',None)
#         pwd = request.POST.get('password',None)
#         print('后台收到的登录用户：',name,'密码为：',pwd)
#         message='请填写登录信息'
#         if name and pwd :  #最低的信任度对待发送过来的数据
#             name = name.strip()
#             try:
#                 user = User.objects.get(name=name)  #如果未匹配到用户，则执行except中的语句
#                 if user.password == pwd:
#                     return redirect('/login/index/')
#                 else:
#                     message='密码不正确'
#             except:
#                 message = '用户不存在'
#         return render(request, 'login/login.html', {'message': message}) #用于保存提示信息
#     return render(request, 'login/login.html') #重定向到index页

def login(request):#登录
    if request.session.get('is_login', None):  # 不允许重复登录,写在前面，不提交form表单的情况下，就可以重定向
        return redirect('/login/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message='请填写登录信息'
        if login_form.is_valid():
            name = login_form.cleaned_data['username'] #表单对象的cleaned_data数据字典中获取表单的具体值
            pwd =  login_form.cleaned_data['password']
            print('后台收到的登录用户：', name, '密码为：', pwd)
            if name and pwd :  #最低的信任度对待发送过来的数据
                name = name.strip()
            try:
                user = User.objects.get(name=name)  #如果未匹配到用户，则执行except中的语句
                if not user.has_confirmed:
                    message = '该用户还未通过邮件确认！'
                    return render(request, 'login/login.html',locals())
                if user.password == hash_code(pwd):  # 哈希值和数据库内的值进行比对
                    request.session['is_login']=True
                    request.session['uer_id']=user.id
                    request.session['user_name']=user.name
                    return redirect('/login/index/')
                else:
                    message='密码不正确'
            except:
                message = '用户不存在'
        print('locals::::',locals())
        return render(request, 'login/login.html', locals()) #用于保存提示信息 locals()函数，它返回当前所有的本地变量字典
    login_form = UserForm()
    return render(request, 'login/login.html',locals()) #重定向到index页

def register(request):#注册
    if request.session.get('is_login',None):
        redirect('/login/index')    #如果已经登陆了，则直接到首页
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        message = '请检查填写内容'
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            pwd1 = reg_form.cleaned_data['password1']
            pwd2 = reg_form.cleaned_data['password2']
            email = reg_form.cleaned_data['email']
            sex = reg_form.cleaned_data['sex']
            if pwd1 != pwd2:
                message='两次输入的密码不一致'
                return render(request,'login/register.html',locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:#用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request,'login/register.html',locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())
                new_user = User()
                new_user.name = username
                new_user.password = hash_code(pwd1)   ## 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()  #保存新用户

                code = make_confirm_string(new_user)
                send_email(new_user.email,code)
                message='请前往注册邮箱，进行邮件确认'

                return redirect('/login/login/')  #自动跳转到登录页面

    reg_form = RegisterForm() #第一次请求，返回空页面
    return render(request, 'login/register.html',locals())

def logout(request):#退出
    if request.session.get('is_login',None):
        request.session.flush()
    return redirect("/login/index/")  #页面重定向到‘index’首页

def confirm(request):
    code = request.GET.get('code',None)
    message =''
    try:
        confim = ConfirmString.objects.get(code=code)
    except:
        message='无效的确认请求!'
        return render(request,'login/confirm.html',locals())
    now = datetime.now()
    c_time = confim.c_time
    if now > c_time + timedelta(settings.CONFIRM_DAYS):
        message = '您的邮件已经过期！请重新注册!'
        confim.user.delete()  #如果时间已经超期，删除注册的用户，同时注册码也会一并删除
        return render(request,'login/confirm.html',locals())
    else:
        confim.user.has_confirmed = True
        confim.user.save()
        confim.delete()   #删除注册码，但不删除用户本身
        message = '恭喜注册成功，请使用账户登录！'
        return render(request,'login/confirm.html',locals())
