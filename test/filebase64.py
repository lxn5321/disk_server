import base64
import unicodedata

str = '喂喂喂，你是谁，你是美国的小美眉。'

b = base64.b64encode(str.encode('gbk'))
print(b)

n = base64.b64decode(b)
print(len(n))
print(n.decode('utf-8'))

bb =  'zrnOuc65o6zE48rHy62jrMTjysfDwLn6tcTQocPAw7yhowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='



nn = base64.b64decode(bb)
print(type(nn.decode('gbk')).__name__)
print(nn.decode('gbk'))
print(len(nn))

bbb = u'zrnOuc65o6zE48rHy62jrMTjysfDwLn6tcTQocPAw7yhowAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
print(type(bbb).__name__)
nnn = base64.b64decode(bbb)
print(nn.decode('gbk'))