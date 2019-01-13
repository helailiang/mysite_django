from django import forms
from captcha.fields import CaptchaField

gender = (
    ('man', '男'),
    ('woman', '女'),
)
class UserForm(forms.Form): #登录form
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'请输入用户名'})) #label参数用于设置<label>标签
    password = forms.CharField(label='密码',max_length=100,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'请输入密码'})) #用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(\
        attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))  # label参数用于设置<label>标签
    password1 = forms.CharField(label='密码', max_length=100, widget=forms.PasswordInput(\
        attrs={'class': 'form-control','placeholder': '请输入密码'}))  # 用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框
    password2 = forms.CharField(label='确认密码', max_length=100, widget=forms.PasswordInput( \
        attrs={'class': 'form-control',
               'placeholder': '请输入密码'}))  # 用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框
    email = forms.EmailField(label='邮箱地址',widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别',choices=gender)  #是一个select下拉框
    captcha = CaptchaField(label='验证码')

