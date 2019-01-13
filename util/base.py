import hashlib
from datetime import  datetime
from login.models import ConfirmString
from django.core.mail import EmailMultiAlternatives
from django.conf import settings  #导入settings配置文件
def hash_code(pwd,salt='mysite'):
    '''使用hash加密'''
    s = pwd + salt
    h = hashlib.sha256()
    h.update(s.encode()) # update方法只接收bytes类型
    return  h.hexdigest()

def make_confirm_string(user):
    '''创建确认码对象，并返回确认码'''
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(user.name,now)
    ConfirmString.objects.create(code=code,user=user) #生成并保存一个确认码对象
    return code

def send_email(to_email,code):
    '''注册的邮箱和前面生成的哈希值'''
    subject = '来自www.helailiang.com的注册确认邮件'
    text_content = '感谢注册www.helailiang.com，这里是何老的博客和教程站点，专注于Python和Django技术的分享！' \
                   '如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'
    html_content = '''
                    <p>感谢注册<a href="http://{}/login/confirm/?code={}" target=blank>www.helailiang.com</a>，\
                    这里是何老的博客和教程站点，专注于Python和Django技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[to_email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()
