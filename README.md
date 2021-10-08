### Using namedPipe in Python on Windows



#### Demo

run Server.py first and Then Client



#### Description

Try using namedpipe to transfer message for different processes.



#### 备注：

本来命名管道本身是支持异步IO操作的，但是使用起来过于复杂，特别是使用python情况下，要弄清楚怎么定义OVERLAP结构体就够麻烦，所以这里直接使用了两个命名管道来实现双工通讯。

如果不定义OVERLAP结构体，程序会无缘无故退出。附上有错误的版本 pipeManage - 副本.py

希望哪天能找到用OVERLAP实现的代码。