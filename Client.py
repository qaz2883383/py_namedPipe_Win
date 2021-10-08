import pipeManage as pm
import time

def fun(data):
    pass

p = pm.pipeManager(asServer=False)

for i in range(10):
    print("print" + str(i))
    p.write(('client send:'+str(i)).encode('utf-8'))
    time.sleep(1)

p.threadRead.join()