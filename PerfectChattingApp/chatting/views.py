from django.shortcuts import render, HttpResponse
from django import views
from chat import models

# Create your views here.
# 添加联系人


class Contact(views.View):

    def get(self, req):
        return HttpResponse("ok")

    def post(self, req):
        contact = req.POST.get('contact', None).strip()
        user_name = req.POST.get("user_name", None).strip()
        import json
        dict_info = {
            "msg": 4000,
            "path": ''
        }
        # 从数据库取
        con = models.UserInfo.objects.filter(user_name=contact).count()
        if not con:
            # 如果没有该用户
            dict_info["msg"] = 4000
            return HttpResponse(json.dumps(dict_info))
        elif contact == user_name:
            # 如果是用户自己
            dict_info["msg"] = 4001
            return HttpResponse(json.dumps(dict_info))
        else:
            user = models.UserInfo.objects.filter(user_name=user_name)[0]
            # 将该用户的contact字段取出来
            contact_str = str(user.contact)
            contact_arr = contact_str.split("|")
            for i in contact_arr:
                if i == contact:
                    # 如果已经添加了该用户
                    dict_info["msg"] = 4002
                    return HttpResponse(json.dumps(dict_info))
            # 如果字段为空，赋值''
            if not contact_str:
                contact_str = ''
            # 将好友添加进去
            contact_str = contact_str + contact + "|"
            # 没问题，添加
            models.UserInfo.objects.filter(user_name=user_name).update(contact=contact_str)
            # 刷新session
            req.session["contact"] = contact_str
            # 将好友头像取出来
            path = models.UserInfo.objects.filter(user_name=contact)[0].user_img
            dict_info["msg"] = 4003
            dict_info["path"] = path
            return HttpResponse(json.dumps(dict_info))
# 处理聊天内容


class SendMsg(views.View):

    def get(self, req):
        from_user = req.GET.get("from", None).strip()
        to_user = req.GET.get("to", None).strip()
        # 从数据库里面拿取聊天记录
        me = models.UserMsg.objects.filter(from_user=from_user, to_user=to_user)
        # she = models.UserMsg.objects.filter(from_user=to_user, to_user=from_user)
        she = models.UserMsg.objects.filter(from_user=to_user, to_user=from_user)
        # 将所有消息的ID添加进列表
        id_count = []
        for i in me:
            id_count.append(i.id)
        for j in she:
            id_count.append(j.id)
        # 将消息的id进行排序
        id_count.sort(key=int)
        # 存放消息的列表
        all_msg = []
        for i in id_count:
            # 在me里面查找
            for j in me:
                if j.id == i:
                    all_msg.append(('me', j.msg))
            # 在she里面查找
            for j in she:
                if j.id == i:
                    all_msg.append(("she", j.msg))
        import json
        return HttpResponse(json.dumps(all_msg))

    def post(self, req):
        from_user = req.POST.get("from", None).strip()
        to_user = req.POST.get('to', None).strip()
        msg = req.POST.get('content', None)
        # 将消息存入数据库
        models.UserMsg.objects.create(from_user=from_user, to_user=to_user, msg=msg)
        return HttpResponse('ok')












