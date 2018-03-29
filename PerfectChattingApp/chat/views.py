from django.shortcuts import render, HttpResponse, redirect
from django import views
from django.views.decorators.csrf import csrf_exempt

from . import models
import time
import random
import os

# Create your views here.

# 全局变量
CONFIRM_CODE = ''

# 主页面


class Home(views.View):

    def get(self, req):
        return render(req, 'Home/home.html')
# 登录页面


class Login(views.View):

    def get(self, req):
        response = render(req, 'Home/login.html', {'msg': ''})
        is_login = req.GET.get("is_login")
        # 如果用户点击退出登录，清除浏览器的cookie,并返回登录页面
        if is_login:
            response.delete_cookie("user_name")
            return response
        # 进行cookie验证
        user_name = req.COOKIES.get('user_name')
        # 如果用户浏览器存在cookie值，则免登录
        if user_name:
            user_name = req.session.get("username")
            img = req.session.get('img')
            last_date = req.session.get('last_date')
            contact = req.session.get("contact")
            contact_arr = str(contact).split("|")
            contact_arr.pop()
            return render(req, "Home/homelogin.html", {'user_name': user_name, 'img': img, 'last_date': last_date, 'contact': contact_arr})
        # 如果没有登录，显示登录页面
        return response

    def post(self, req):
        user_name = req.POST.get('username', None)
        user_password = req.POST.get('password', None)
        # 从数据库中找出该用户信息
        user = models.UserInfo.objects.filter(user_name=user_name, user_password=user_password)
        # 如果该用户存在
        if user.count():
            # 取出用户头像
            user = user[0]
            img = user.user_img
            if not img:
                # 如果用户没有设置头像
                img = 'no_img.jpg'

            # 计算距离上次登录的时间
            date = user.user_date
            login_date = time.time() - float(date)
            last_date = str(int(login_date//86400)) + '天' + str(int(login_date%86400//3600)) + '小时' + str(int(login_date%86400%3600//60)) + '分钟'
            # 刷新数据库登录时间
            models.UserInfo.objects.filter(user_name=user_name).update(user_date=str(time.time()))
            # 取出好友列表
            contact = user.contact
        else:
            # 如果用户不存在
            return render(req, 'Home/login.html', {"msg": "用户不存在"})
        # 将用户信息储存进session
        req.session['username'] = user_name
        req.session['img'] = img
        req.session['last_date'] = last_date
        req.session["contact"] = contact
        return redirect('/chat/homelogin/')
# 登录成功页面


class LoginHome(views.View):

    def get(self, req):
        img = req.GET.get('img', None)
        user_name = req.session.get('username', None)
        if user_name:
            if not img:
                # 如果没有获取到img，就是用session里面储存的img
                img = req.session.get('img', None)
            else:
                # 如果获取到了img，就用获取到的，并且刷新数据库里面的user_img以及session里面的
                models.UserInfo.objects.filter(user_name=user_name).update(user_img=img)
                req.session['img'] = img
            last_date = req.session.get('last_date', None)
            contact = req.session.get("contact")
            contact_arr = str(contact).split("|")
            contact_arr.pop()
            # 将用户数据跟密码储存进cookie
            rep = render(req, "Home/homelogin.html", {'user_name': user_name, 'img': img, 'last_date': last_date, 'contact': contact_arr})
            rep.set_cookie("user_name", user_name.encode("utf8"), 360)
            # 跳转到用户页面
            return rep
        else:
            # 如果没有登录，跳转到登录页面
            return redirect('/chat/login/')
# 注册页面


class Register(views.View):

    def get(self, req):
        return render(req, "Home/register.html", {"msg": ''})

    def post(self, req):
        user_name = req.POST.get("user_name", None)
        user_email = req.POST.get("user_email", None)
        user_password = req.POST.get("user_pwd", None)
        user_coding = req.POST.get("confirm_code", None)
        if user_coding != CONFIRM_CODE:
            return render(req, "Home/register.html", {"msg": "验证码错误！！！"})
        # 检测数据库中是否已经有注册过的邮箱、用户名
        user = models.UserInfo.objects.filter(user_name=user_name).count()
        # 如果用户名已经存在
        if user:
            return render(req, "Home/register.html", {"msg": "用户名已经存在！！！"})
        user = models.UserInfo.objects.filter(user_name=user_email).count()
        # 如果邮箱已经注册过
        if user:
            return render(req, "Home/register.html", {"msg": "该邮箱已经注册！！！"})

        # 如果没有问题，将数据保存进数据库
        models.UserInfo.objects.create(user_name=user_name, user_email=user_email, user_password=user_password, user_date=str(time.time()), user_img="no_img.jpg")
        # 为用户创建一个头像目录保存头像
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.mkdir('%s/statics/user_head/%s' % (base_dir, user_name.strip()))
        return render(req, "Home/registerSuccess.html")
# 利用邮箱发送验证码


class EmailCode(views.View):

    def post(self, req):
        email = req.POST.get('email', None)
        # 生成4位验证码
        import random
        global CONFIRM_CODE
        CONFIRM_CODE = str(random.randint(0, 9)) + random.choice("abcdefghijklmnopqrstuvwxyz") + \
                       str(random.randint(0, 9)) + random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # 发送邮件
        import smtplib
        from email.mime.text import MIMEText
        # 发送方邮箱
        msg_from = '2789519045@qq.com'
        # 发送方邮箱的授权码
        code = 'fjkmnzgjgwhwdfjc'
        msg_to = email
        # 主题
        subject = '完美聊天室验证码'
        # 正文
        content = '你的完美聊天室验证码是' + CONFIRM_CODE
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        try:
            # 邮件服务器及端口号
            s = smtplib.SMTP_SSL('smtp.qq.com', 465)
            s.login(msg_from, code)
            s.sendmail(msg_from, msg_to, msg.as_string())
        except Exception:
            return HttpResponse("发送失败，请重新点击发送。。。")
        finally:
            s.quit()
        return HttpResponse("请将邮箱接收到的验证码填入表单中。。。")
# 文件上传


class SendHeadImg(views.View):

    def post(self, req):
        # 拿取到上传文件的对象
        obj = req.FILES.get('img_file')
        # 拿到用户名
        user_name = req.POST.get('user_name', None).strip()
        if obj.name:
            # 文件存在
            # 创建随机文件，解决浏览器不能实时加载图片的问题
            ran = str(random.randint(1, 100000))
            # 将文件写入本地用户头像库中
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(r'%s/statics/user_head/%s/%s%s.jpg' % (base_path, user_name.strip(), user_name, ran), 'wb') as f:
                # 将内容写入本地
                for chunk in obj.chunks():
                    f.write(chunk)
            # 将文件路径写入数据库对应的用户列
            img_name = '%s%s.jpg' % (user_name, ran)
            models.UserInfo.objects.filter(user_name=user_name).update(user_img=img_name)
        return HttpResponse(img_name)
# 用户历史头像


class HistoryImg(views.View):

    def get(self, req):
        now_img = req.GET.get("now_img", None).strip()
        user = req.GET.get("user", None).strip()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, 'statics', 'user_head', user)
        history_img = os.listdir(path)
        return render(req, 'Home/history_img.html', {"now_img": now_img, "user": user, "history_img": history_img})

