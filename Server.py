import pipeManage as pm
import time

def fun(data):
    if '5' in data.decode():
        print("fun: found 5")

p = pm.pipeManager(asServer=True, funServerRead=fun)

for i in range(10):
    print("print" + str(i+100))
    p.write(('server send:'+str(i+100)).encode('utf-8'))
    time.sleep(1)

p.threadRead.join()