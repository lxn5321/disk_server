import hashlib
import os
import datetime

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

print(GetFileMd5('D:\\apythoncode\\disk_server\\www\\5'))

myhash = hashlib.md5()
myhash.update(b'a')
print(myhash.hexdigest())
