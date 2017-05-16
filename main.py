#coding=utf-8
#qpy:kivy
#qpy:2


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import socket
import threadpool
import os


class MyLayout(BoxLayout):
    address=ObjectProperty()
    portnum=ObjectProperty()
    output=ObjectProperty()
    result=ObjectProperty()
    tnum=ObjectProperty()
    timeout=ObjectProperty()
    
    
    
    def start(self):
        num=self.portnum.text.split(',')
        num=[int(i) for i in num]
        if len(num)!=1:
            num=xrange(num[0],num[1])
        self.ids.result.text=''
        self.ids.output.text=''
        thnum=self.tnum.text
        pool=threadpool.ThreadPool(int(thnum))
        
        requests=threadpool.makeRequests(self.check,num)
        [pool.putRequest(i) for i in requests]

        
        
        
    def check(self,port):
        addrs=self.address.text.strip().split(' ')
        for addr in addrs:
            if addr[-1]=='0':
                for i in range(1,256):
                    naddr=addr.split('.')
                    del naddr[-1]
                    naddr='.'.join(naddr)
                    naddr=naddr+'.'+str(i)
                    try:
                        s=socket.socket()
                        s.connect((naddr,port))
                        if port==22:
                            recv=s.recv(1024)
                            recv=recv.split(' ')[-1]
                            recv=recv.replace('\r\n','').replace('\n','')
                            self.ids.result.text += '%s:%s  %s\n'%(naddr,port,recv)
                        else:
                            self.ids.result.text += '%s:%s\n'%(naddr,port)
                    except Exception,e:
                        self.ids.output.text='正在扫描 %s:%s'%(naddr,port)
                    finally:
                        s.close()                             
            else:
                try:
                    s=socket.socket()
                    s.connect((addr,port))
                    if port==22:
                        recv=s.recv(1024)
                        recv=recv.split(' ')[-1]
                        recv=recv.replace('\r\n','').replace('\n','')
                        self.ids.result.text += '%s:%s  %s\n'%(addr,port,recv)
                    else:
                        self.ids.result.text += '%s:%s\n'%(addr,port)

                except Exception,e:
                    self.ids.output.text='正在扫描 %s:%s'%(addr,port)
                finally:
                    s.close()
        '''
        try:
            s=socket.socket()
            s.connect((addr,addrport))
            self.ids.result.text += '%s:%s\n'%(addr,addrport)
        except Exception,e:
            self.ids.output.text='正在扫描 %s:%s'%(addr,addrport)
        finally:
            s.close()
        '''
        
            

class MainApp(App):
    def build(self):
        return MyLayout()
    def on_start(self):
        socket.setdefaulttimeout(int(self.root.ids.timeout.text))

MainApp().run()