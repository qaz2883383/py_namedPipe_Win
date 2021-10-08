import pipeManage as pm
import time

def fun(data):
    pass

p = pm.pipeManager(asServer=True)

for i in range(10):
    print("print" + str(i+100))
    p.write(('server send:'+str(i+100)).encode('utf-8'))
    time.sleep(1)

p.threadRead.join()