# Author : Mr King
# Date : 2018-03-12 20:46 


import smtplib
from email.mime.text import MIMEText

# 发送方邮箱
msg_from = '2789519045@qq.com'

# 发送方邮箱的授权码
code = 'fjkmnzgjgwhwdfjc'

# 收件人邮箱
msg_to = '2968626690@qq.com'

# 主题
subject = '验证码'

# 正文
content = '这是我使用python email以及smtplib模块发送的邮件'

msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

try:
    # 邮件服务器及端口号
    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(msg_from, code)
    s.sendmail(msg_from, msg_to, msg.as_string())
    print('发送成功')
except Exception:
    print("发送失败")
finally:
    s.quit()



