
# -*- coding=utf8 -*-

import re,time,urllib,requests,os,sys,json,random,pygame,eyed3

from tkinter import  *
from tkinter import ttk
import  tkinter.messagebox  as tkMessageBox
from PIL import Image,ImageTk
import threading
global musicdic,Page
musicdic={}
Page=[]
pygame.mixer.init()

def ClickMusic(event):
    try :
      selectname=Lb.get(Lb.curselection())
          
      var2.set(selectname)
      addoldMusic()
      #download(musicdic[selectname],str(Lb.curselection()))
      #download(musicdic[selectname])
      playmp3(selectname,musicdic[selectname])
    except :
      selectname=Lb2.get(Lb2.curselection())

      var2.set(selectname)
      addoldMusic()
      #download(musicdic[selectname],str(Lb.curselection()))
      #download(musicdic[selectname])
      playmp3(selectname,musicdic[selectname])
def playmp3(name,dis):
    Lb3.delete(0,END)
    url=dis[0]
    picurl=dis[1]
    songurl=dis[2]
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        second=0
    try:
        path=os.path.join('./temp/'+'1.mp3')
        picpath=os.path.join('./temp/'+'1.jpg')
        urllib.request.urlretrieve(url,path)
        urllib.request.urlretrieve(picurl,picpath) 
    except:
        path=os.path.join('./temp/'+'2.mp3')
        picpath=os.path.join('./temp/'+'2.jpg')
        urllib.request.urlretrieve(url,path)
        urllib.request.urlretrieve(picurl,picpath)
    html=requests.get(songurl).text
    song_dic=json.loads(html)
    var3.set(name)
    
    try :
        lrc=song_dic['lrc']['lyric']
    except:
        lrc='暂无歌词'
    for word in lrc.split('\n'):
        word=re.sub('\[.*?\]','',word)
        Lb3.insert(END,word)
    mp3=pygame.mixer.music.load(path)
    xx= eyed3.load(path)
    second=xx.info.time_secs
    im=Image.open(picpath)
    im=im.resize((300, 480),Image.ANTIALIAS)  
    bm2 = ImageTk.PhotoImage(im)
    piclabel.configure(image=bm2)
    piclabel.bm2=bm2
    pygame.mixer.music.play()
    return second
    
    

    
def listOpenMusic():
       if  pygame.mixer.music.get_busy():
           pygame.mixer.music.stop()
           second=0
       count=Lb2.size()
       ct=Lb.size()
       if count==0:
           tkMessageBox.showinfo('提示','历史播放列表为空,请先添加播放列表')
       else:
           #tkinter.messagebox.showinfo('列表播放','开始列表播放')
           for i in range(count):
               print(i)
               name=Lb2.get(i)
         
               var2.set(name)
               if not pygame.mixer.music.get_busy():
                  second=playmp3(name,musicdic[name])
               else:
                   break
               time.sleep(second)
       global List
       LIST = threading.Timer(1, listOpenMusic)
       LIST.start()
                  
                
def randOpenMusic():
       if  pygame.mixer.music.get_busy():
           pygame.mixer.music.stop()
       count=Lb2.size()
       if count==0:
           tkMessageBox.showinfo('提示','历史播放列表为空,请先添加播放列表')
       else:
           #tkinter.messagebox.showinfo('列表播放','开始列表播放')
               if not pygame.mixer.music.get_busy():
                   
                   i=random.randint(1,count)-1

                   name=Lb2.get(i)

                   var2.set(name)
                       
                   #download(musicdic[name])
                   second=playmp3(name,musicdic[name])
       global rand
       rand = threading.Timer(second, randOpenMusic)
       rand.start()
                   
def randplay():
       rand = threading.Timer(0, randOpenMusic)
       rand.start()
def listplay():
    LIST=threading.Timer(0, listOpenMusic)
    LIST.start()


        
def oldMusic():
    oldList=[]
    if Lb.get(Lb.curselection()):
        selectname=Lb.get(Lb.curselection())
        oldList.append(selectname)
    return list(set(oldList))
def addoldMusic():
    list=oldMusic()
    #print (list)
    for music in list:
        if music not in Lb2.get(first=0, last=Lb2.size()-1):
          #print(Lb2.get(first=0, last=Lb2.size()-1))
          Lb2.insert(END,music)

def search():
    if E.get()=='':
        tkMessageBox.showinfo('提示','请输入歌曲信息在搜索')
    else:
            #Lb.delete(first=0,last=Lb.size())
            name=E.get()
            
            firstUrl = "http://s.music.163.com/search/get/?type=1&s={}&limit=100".format(name)
            
            #print (firstUrl)
           
            requst = requests.get(firstUrl)
            
            result = requst.text
            #print (result)
            #使用BeautifulSoup快速解析html文档
            dicts=json.loads(result)
            #print(dicts)
            dic=dicts["result"]["songs"]
            Lb.delete(0,END)
            for i in range(len(dic)):
                songname=dic[i]["name"]
                songid=dic[i]["id"]
                singer=dic[i]["artists"][0]["name"]
                pic=dic[i]["album"]["picUrl"]
                url='http://music.163.com/song/media/outer/url?id='+str(songid)+'.mp3'
                songurl='http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1'%str(songid)
                na=songname+'--'+singer
                #print (pic)
                Lb.insert(END,na)
                musicdic[na]=[url,pic,songurl]
#弹窗
class PopupDialog(Toplevel):
  def __init__(self, parent):
    super().__init__()
    self.title('设置文件存储地址')
    self.parent = parent # 显式地保留父窗口
    row1 = Frame(self)
    row1.pack(fill="x")
    Label(row1, text='路径：', width=8).pack(side=LEFT)
    self.path = StringVar()
    Entry(row1, textvariable=self.path, width=20).pack(side=LEFT)
    row3 = Frame(self)
    row3.pack(fill="x")
    Button(row3, text="取消", command=self.cancel).pack(side=RIGHT)
    Button(row3, text="确定", command=self.ok).pack(side=RIGHT)
  def ok(self):
    # 显式地更改父窗口参数
    self.parent.path = self.path.get()
    # 显式地更新父窗口界面
    
    self.destroy() # 销毁窗口
    return self.parent.path
  def cancel(self):
    self.destroy()

def setup_config():
    pw=PopupDialog(top)
    top.wait_window(pw)
    return pw.ok()
class section():

    def dowload(self):
        try:
              selectname=Lb.get(Lb.curselection())
              
        except:
              selectname=Lb2.get(Lb2.curselection())
        
        
        savedir=setup_config()
        url=musicdic[selectname][0]
        #print(url)
        savepath=os.path.join(savedir,selectname+'.mp3')
        urllib.request.urlretrieve(url,savepath)
        if savedir:
            tkMessageBox.showinfo('提示','下载完成')
    def play(self):
        try :
              selectname=Lb.get(Lb.curselection())     
        except  :
              selectname=Lb2.get(Lb2.curselection())
        url=musicdic[selectname]
        if selectname not in Lb2.get(0,END):
            Lb2.insert(END,selectname)
        var2.set(selectname)
        playmp3(selectname,url)
    def nextmusic(self):
        size=Lb2.size()
              
        i=random.randint(1,size)-1
        nextname=Lb2.get(i)
        #print(nextname)
        url=musicdic[nextname]
        playmp3(nextname,url)
    def addMusic(self):
        lists=oldMusic()
        #print (list)
        for music in lists:
            if music not in Lb2.get(first=0, last=Lb2.size()-1):
              #print(Lb2.get(first=0, last=Lb2.size()-1))
              Lb2.insert(END,music)
        

section = section()
#实例化刚刚写的类

class MusicButton(Frame):  
    def __init__(self, master):  
        frame = Frame(master)  
        frame.pack(side=TOP, fill=BOTH,expand=True)  
        
  
        self.button1 = Button(frame,  
                                      text="上一曲",  
                                      command=self.func1,
                                      width=8,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))
        

        self.button1.pack(side=LEFT)
  
        self.button2 = Button(frame,  
                                      text="播放",  
                                      command=self.func2,
                                      width=5,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))  
       
        self.button2.pack(side=LEFT)
  
        self.button3 = Button(frame,  
                                      text="暂停",  
                                      command=self.func3,  
                                      width=5,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))  
    
        self.button3.pack(side=LEFT)
        self.button5 = Button(frame,  
                                      text="停止",  
                                      command=self.func5,  
                                      width=5,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))  
      
        self.button5.pack(side=LEFT)
  
        self.button4 = Button(frame,  
                                      text="下一曲",  
                                      command=self.func4,
                                      width=8,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))
        
        self.button4.pack(side=LEFT)
        self.button6 = Button(frame,  
                                      text="重新播放",  
                                      command=self.func6,
                                      width=12,
                                      bg="blue",  
                                      fg="white",  
                                      font=("华文琥珀", 8))
        self.button6.pack(side=LEFT)
        

        
        
        
  
    def func1(self):  
        section.nextmusic()
        #labvar.set('上一曲')
    def func2(self):  
        pygame.mixer.music.unpause()
        #labvar.set('开始播放')
    def func3(self):  
        pygame.mixer.music.pause()
        #labvar.set('暂停播放')
    def func4(self):  
        section.nextmusic()
        #labvar.set('下一曲')
    def func5(self):
       
        pygame.mixer.music.stop()
        #labvar.set('停止播放')
    def func6(self):
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()
        

def popupmenu(event):
    menu.post(event.x_root,event.y_root)
 
def setVolume(val):
    volume = float(slider.get())
    pygame.mixer.music.set_volume(volume/100)


def process():
        if pygame.mixer.music.get_busy():
            proc.set(pygame.mixer.music.get_pos()/1000)
        else:
            
            proc.set(0)
        global timer
        timer = threading.Timer(1, process)
        timer.start()

timer = threading.Timer(1, process)
timer.start()
      

top=Tk()
top.iconbitmap('./temp/9.ico')
top.title('YINmusic')
top.geometry('1000x600+50+30')

#设置鼠标右键菜单
menu = Menu(top,tearoff=0)
#tearoff设置成0就不会有开头的虚线，也不会让你的菜单可以单独成为窗口，可以自己试验一下
menu.add_command(label="播放该歌曲",command=section.play)
menu.add_separator()
menu.add_command(label="播放下一首",command=section.nextmusic)
menu.add_separator()
menu.add_command(label="下载该歌曲",command=section.dowload)
menu.add_separator()
menu.add_command(label="添加至播放列表",command=section.addMusic)




# 第一版 搜索 播放插件
FR=Frame(top)
FR.pack(side=LEFT,fill=Y)



show = StringVar()
E = Entry(FR,textvariable = show,width="30")
E.pack()
B=Button(FR,text='搜 索',command=search)
B.pack()

BOTT=Frame(FR)
BOTT.pack(side=TOP,fill=Y)

BL=Button(BOTT,text='列表顺序播放',fg='green',command=listplay)
BL.pack(side=LEFT)

BL=Button(BOTT,text='列表随机播放',fg='green',command=randplay)
BL.pack(side=LEFT)




frameR = Frame(FR)  
frameR.pack()
bot=MusicButton(frameR)
slider = Scale(FR,label='音量',from_ =0, to = 100,orient=HORIZONTAL, command = setVolume)
slider.set(20)
slider.pack(side=BOTTOM)



Lb=Listbox(FR,width=50)
Lb.pack(expand=YES,fill=BOTH)
Lb.bind('<Double-Button-1>',ClickMusic)
Lb.bind('<Button-3>',popupmenu)


Lb2=Listbox(FR,width=50)
Lb2.pack(expand=YES,fill=BOTH)
Lb2.bind('<Double-Button-1>',ClickMusic)
Lb2.bind('<Button-3>',popupmenu)

scl=Scrollbar(Lb)
scl2=Scrollbar(Lb2)
Lb.config(yscrollcommand=scl.set)
Lb2.config(yscrollcommand=scl2.set)
scl.config(command=Lb.yview())
scl2.config(command=Lb2.yview())
scl.pack(side=RIGHT,fill=Y)
scl2.pack(side=RIGHT,fill=Y)

# 第二版 
message=Frame(top)
message.pack(side=LEFT,fill=Y,expand=True)

#第三版
song=Frame(message)
song.pack(side=TOP,fill=X,expand=True)

pic=Frame(song)
pic.pack(side=LEFT,fill=Y)



im=Image.open('./temp/start.jpg')
im=im.resize((300, 480),Image.ANTIALIAS)  
bm = ImageTk.PhotoImage(im)
piclabel = Label(pic, imag = bm)
piclabel.bm=bm
piclabel.pack(side=TOP)

proc = Scale(pic,label='进度',from_ =0,to=1000,orient=HORIZONTAL, command = setVolume)
proc.pack(side=BOTTOM)
proc.set(0)

#第四版
songword=Frame(song)
songword.pack(side=LEFT,fill=BOTH,expand=True)

var3=StringVar()
label3=Label(songword, textvariable=var3)
label3.pack(side=TOP,fill=X)

Lb3=Listbox(songword,width=300)
Lb3.pack(expand=YES,fill=BOTH)






#第五版
mark=Frame(message)
mark.pack(side=BOTTOM,fill=BOTH,expand=True)

var = StringVar()
label = Label( mark, textvariable=var,width=300, relief=RAISED,bg='green',fg='Red' )
var.set("copyRightBy :ChaoGuo.long")
label.pack(side=BOTTOM,fill=X)



var2=StringVar()
label2=Message(mark, textvariable=var2,width=300, relief=RAISED,bg='green',fg='Red')
label2.pack(side=BOTTOM,fill=X)




top.mainloop()





