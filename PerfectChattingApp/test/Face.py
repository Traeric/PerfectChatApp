# Author : Mr King
# Date : 2018-03-17 14:10

from urllib import request
from urllib import parse
""

url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
data = {
    "api_key": "2m7lT8laBkcVpnKR3zqUI2wqdvkjvKgi",
    "api_secret": "R5Syqnte_p7TaYoPiLuR7h19NUbOf2Vv",
    "image_url1": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1256664899,3113985651&fm=27&gp=0.jpg",
    "image_url2": "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=111982302,2037773538&fm=27&gp=0.jpg"
}


data = parse.urlencode(data).encode(encoding='utf-8')
html = request.urlopen(url, data=data).read()


print(html)

