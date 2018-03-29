# Author : Mr King
# Date : 2018-03-20 15:42 

from django import template
from chat import models
# import os
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)


register = template.Library()


@register.simple_tag
def contact(username):
    print(username)
    user = models.UserInfo.objects.filter(user_name=username)
    if user:
        user = user[0]
        return user.user_img
    else:
        return ''

