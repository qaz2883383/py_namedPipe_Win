import pipeManage as pm
import time

def fun(data):
    if '3' in data.decode():
        print("fun: found 3")

p = pm.pipeManager(asServer=False, funClientRead=fun)

for i in range(10):
    print("print" + str(i))
    p.write(('client send:'+str(i)).encode('utf-8'))
    time.sleep(1)

p.threadRead.join()