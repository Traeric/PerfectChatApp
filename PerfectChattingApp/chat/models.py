from django.db import models

# Create your models here.


class UserInfo(models.Model):
    """ 用户信息表 """
    user_name = models.CharField(max_length=64)
    user_email = models.CharField(max_length=64)
    user_password = models.CharField(max_length=64)
    user_img = models.CharField(max_length=256)
    user_date = models.CharField(max_length=128)
    # 该用户的联系人
    contact = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        unique_together = (('user_name', 'user_email'), ('user_name', 'user_password'),)


class UserMsg(models.Model):
    """ 用户消息 """
    from_user = models.CharField(max_length=64, null=False, blank=False)
    to_user = models.CharField(max_length=64, null=False, blank=False)
    msg = models.CharField(max_length=8192, null=False, blank=False)

    class Meta:
        db_table = 'user_msg'



