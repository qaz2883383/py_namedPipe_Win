import win32file
import win32pipe
import threading

PIPE_NAME = r'\\.\pipe\\'
PIPE_BUFFER_SIZE = 65535


class pipeManager():
    def pipeReadThread(self):
        if self.isServer:
            while self.isActive:
                try:
                    print("pipeReadThread active.")
                    # 
                    print("pipeReadThread Connect.")
                    # 线程会block在这里
                    data = win32file.ReadFile(self.pipe, PIPE_BUFFER_SIZE, None)
                    print("pipeReadThread readfile.")
                    if data is None or len(data) < 2:
                        continue
                    print('ReadThread MSG_RECV:', data)
                    
                    # 额外的处理函数
                    if self.funServerRead:
                        self.funServerRead(data)
                except Exception as e:
                    print("exception:", e)
                    continue
            print("pipeReadThread Disconnect.")
            win32pipe.DisconnectNamedPipe(self.pipe)
        else:
            while self.isActive:
                try:
                    print("pipeReadThread active.")
                    # if win32pipe.WaitNamedPipe(self.pipe, win32pipe.NMPWAIT_WAIT_FOREVER):
                    data = win32file.ReadFile(self.pipe, PIPE_BUFFER_SIZE, None)
                    print("pipeReadThread readfile.")
                    if data is None or len(data) < 2:
                        continue
                    print('ReadThread MSG_RECV:', data)
                    
                    # 额外的处理函数
                    if self.funClientRead:
                        self.funClientRead(data)
                except Exception as e:
                    print("exception:", e)
                    continue
            print("pipeReadThread CloseHandle.")
            win32file.CloseHandle(file_handle)
                    
                
        
    def pipeWrite(self, data):
        if self.isActive:
            print('pipeWrite:' + str(data))
            ret = win32file.WriteFile(self.pipe, data)
            print('pipeWrite: Write Finish')
            return ret
        else:
            print("pipeWrite: pipe is not active!")
            return None
            
    
    def __init__(self, asServer=True, pipeName="default", funServerRead = None, funClientRead = None):
        self.isActive = False
        if asServer:
            self.pipeName = PIPE_NAME + pipeName
            self.isServer = True
            self.funServerRead = funServerRead
            self.pipe = win32pipe.CreateNamedPipe(self.pipeName,
                                           win32pipe.PIPE_ACCESS_DUPLEX | win32file.FILE_FLAG_OVERLAPPED,
                                           win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_BYTE,
                                           win32pipe.PIPE_UNLIMITED_INSTANCES,
                                           PIPE_BUFFER_SIZE,
                                           PIPE_BUFFER_SIZE, 500, None)
            
            if self.pipe:
                win32pipe.ConnectNamedPipe(self.pipe, None)
                self.isActive = True
                self.threadRead = threading.Thread(target=self.pipeReadThread)
                self.threadRead.start()
            else:
                print("Pipe Init: Fail Creating Pipe")
        else:
            self.pipeName = PIPE_NAME + pipeName
            self.isServer = False
            self.funClientRead = funClientRead
            self.pipe = win32file.CreateFile(self.pipeName,
                                   win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                   win32file.FILE_SHARE_WRITE, None,
                                   win32file.OPEN_EXISTING, win32file.FILE_FLAG_OVERLAPPED, None)
            
            if self.pipe:
                self.isActive = True
                self.threadRead = threading.Thread(target=self.pipeReadThread)
                self.threadRead.start()
            else:
                print("Pipe Init: Fail Creating Pipe")
            
            
    
            
            