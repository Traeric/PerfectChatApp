# Author : Mr King
# Date : 2018-03-17 14:57 

from urllib import request
from urllib import parse
""

url = 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard'
data = {
    "api_key": "2m7lT8laBkcVpnKR3zqUI2wqdvkjvKgi",
    "api_secret": "R5Syqnte_p7TaYoPiLuR7h19NUbOf2Vv",
    "image_url": "https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=e0450021f1246b607b0eb572d3c37d71/9345d688d43f8794fa8e165cd51b0ef41bd53a4a.jpg"
}


data = parse.urlencode(data).encode(encoding='utf-8')
html = request.urlopen(url, data=data).read()


print(html)

