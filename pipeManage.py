import win32file
import win32pipe
import threading

PIPE_NAME = r'\\.\pipe\\'
PIPE_BUFFER_SIZE = 65535


class pipeManager():
    def serverWaitThread(self):
        if self.pipeRead:
            win32pipe.ConnectNamedPipe(self.pipeRead, None)
            self.isActive = True
            self.threadRead = threading.Thread(target=self.pipeReadThread)
            self.threadRead.start()
        else:
            self.isActive = False
            print("Pipe Init: Fail Creating Pipe")
            
        if self.pipeWrite:
            win32pipe.ConnectNamedPipe(self.pipeWrite, None)
            self.writeAllow = True
        else:
            self.writeAllow = False
            print("Pipe Init: Fail Creating Pipe")

    def pipeReadThread(self):
        if self.isServer:
            while self.isActive:
                data = win32file.ReadFile(self.pipeRead, PIPE_BUFFER_SIZE, None)
                if data is None or len(data) < 2:
                    continue
                print('ReadThread MSG_RECV:', data)
                
                # 额外的处理函数
                if self.funServerRead:
                    self.funServerRead(data[1])
            print("pipeReadThread Disconnect.")
            win32pipe.DisconnectNamedPipe(self.pipe)
        else:
            while self.isActive:
                # if win32pipe.WaitNamedPipe(self.pipe, win32pipe.NMPWAIT_WAIT_FOREVER):
                data = win32file.ReadFile(self.pipeRead, PIPE_BUFFER_SIZE, None)
                if data is None or len(data) < 2:
                    continue
                print('ReadThread MSG_RECV:', data)
                
                # 额外的处理函数
                if self.funClientRead:
                    self.funClientRead(data[1])
            print("pipeReadThread CloseHandle.")
            win32file.CloseHandle(file_handle)
                    
                
        
    def write(self, data):
        if self.isActive:
            # print('pipeWrite:' + str(data))
            ret = win32file.WriteFile(self.pipeWrite, data)
            return ret
        else:
            print("pipeWrite: pipe is not active!")
            return None
            
    
    def __init__(self, asServer=True, pipeName="default", funServerRead = None, funClientRead = None):
        self.isActive = False
        if asServer:
            self.pipeReadName = PIPE_NAME + pipeName + '_r'
            self.pipeWriteName = PIPE_NAME + pipeName + '_w'
            self.isServer = True
            self.funServerRead = funServerRead
            self.pipeRead = win32pipe.CreateNamedPipe(self.pipeReadName,
                                           win32pipe.PIPE_ACCESS_DUPLEX,
                                           win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_BYTE,
                                           win32pipe.PIPE_UNLIMITED_INSTANCES,
                                           PIPE_BUFFER_SIZE,
                                           PIPE_BUFFER_SIZE, 500, None)
                                           
            self.pipeWrite = win32pipe.CreateNamedPipe(self.pipeWriteName,
                                           win32pipe.PIPE_ACCESS_DUPLEX,
                                           win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_BYTE,
                                           win32pipe.PIPE_UNLIMITED_INSTANCES,
                                           PIPE_BUFFER_SIZE,
                                           PIPE_BUFFER_SIZE, 500, None)
            self.serverWaitThread = threading.Thread(target=self.serverWaitThread)
            self.serverWaitThread.start()
        else:
            self.pipeReadName = PIPE_NAME + pipeName + '_w'
            self.pipeWriteName = PIPE_NAME + pipeName + '_r'
            self.isServer = False
            self.funClientRead = funClientRead
            
            self.pipeWrite = win32file.CreateFile(self.pipeWriteName,
                                   win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                   win32file.FILE_SHARE_WRITE, None,
                                   win32file.OPEN_EXISTING, 0, None)
                                   
            self.pipeRead = win32file.CreateFile(self.pipeReadName,
                                   win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                   win32file.FILE_SHARE_WRITE, None,
                                   win32file.OPEN_EXISTING, 0, None)
            
            if self.pipeWrite and self.pipeRead:
                self.isActive = True
                self.threadRead = threading.Thread(target=self.pipeReadThread)
                self.threadRead.start()
            else:
                print("Pipe Init: Fail Creating Pipe")
            
            
    
            
            