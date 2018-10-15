#coding:utf-8
from PIL import Image,ImageEnhance
import shutil
import imageio #处理gif动图
import zipfile
import handleDocx #解压缩word文档
import os
import sys
import png #为静态图打水印
import tkinter as tk
from tkinter import ttk

global get_picName #这是gif图片名称,定义在下面了
global List
global stripname
global path

List = []
        
def copyFile(before):#备份图片的函数
    
    wpath = before+"\\waterprint"
    folder = os.path.exists(wpath)
    #print wpath
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        #os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        shutil.copytree(before, wpath)
        #print "---  new folder...  ---"
        #print "---  OK  ---"
    else:
        #print "---  There is this folder!  ---"
        pass
def WaterMark(wpath,what):
    realpath = os.getcwd() 
    ichunqiu = realpath+"\\i.png"
    echunqiu = realpath+"\\e.png"
    if what == 'i':               #png图片打i春秋水印
        mark = Image.open(ichunqiu)      
        png.water(wpath,mark)
        #break
    elif what == 'e':             #png图片打e春秋水印
        #water_path = "D:\\pywatermark\\factory\\e.png"         #mark一下，到时候要替换为相对路径，用os模块
        mark = Image.open(echunqiu) 
        png.water(wpath,mark)
        #break
    else:
        print "error, you choice false watermark!"
        #break    
def IsDir(path): #列出目录下所有文件名
    #返回指定的文件夹包含的文件或文件夹的名字的列表 
    #所以指定目录下的所有图片都会被打水印
    This_path = path+"\\waterprint"
    filelist = os.listdir(This_path)
    
    for filename in filelist:
        filepath = os.path.join(This_path, filename)  
        if os.path.isdir(filepath): #判断filepath是否是目录
             makeChoice(filepath)
        else:
            IsPic(path)
            break
                 
def IsPic(path):
    This_path = path+"\\waterprint"
    filelist = os.listdir(This_path)  
    for filename in filelist:
        filepath = os.path.join(This_path, filename) 
        if filepath.endswith('png') or filepath.endswith('PNG'):
            #print filepath
            WaterMark(filepath,mark)
            
        elif filepath.endswith('gif') or filepath.endswith('GIF'):
            processImage(filepath) #给出的是需要split的gif图片的绝对路径
            os.remove(filepath)                
            for a in List:
                create_gif(a, filepath) #合成

        else:
            #print 'failed to recognized.'         
            pass   
def analyseImage(path): #处理png图片
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results
        
def processImage(path): #处理gif图
    
    image_list = []
    mode = analyseImage(path)['mode']
    im = Image.open(path)
    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    
    try:
        while 1: 
            ''''' 
            If the GIF uses local colour tables, each frame will have its own palette. 
            If not, we need to apply the global palette to the new frame. 
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            ''''' 
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image? 
            If so, we need to construct the new frame by pasting it on top of the preceding frames. 
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            
            get_picName = ''.join(os.path.basename(path).split('.')[:-1]) #这一段代表图片名称
            stripname = ''.join(os.path.basename(path))             #这一段代表图片名称，包括后缀
            
            gif_path= path.strip(stripname)+'\\%s-%d.png' % (get_picName, i)            
            image_list.append(gif_path) #保存切分后的图片为一个列表，准备合成
            new_frame.save(gif_path, 'PNG')     
            
            WaterMark(gif_path,mark) #给gif切分png打水印
            
            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1) 
    except EOFError:
       pass
    List.append(image_list)
    
def create_gif(image_list, gif_name): #合成为gif图
    frames = []
    smaller_image = []
    smaller_image = image_list[0:-1:2] #跳帧保存
    for image_name in smaller_image:
        frames.append(imageio.imread(image_name))
    # Save them as frames into a gif 
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.3)
    #print image_list
    return      
        
def judgment(path,mark): # path:C:\Users\whale\Desktop\test\docx\complex

    filelist = os.listdir(path) #['silic.docx'] 列出文件名称
    file_dic = []
    pic_path = []
    file_dic = [i.strip('.docx') for i in filelist] #['silic']
    pic_path = [os.path.join(path, i) for i in file_dic]  #C:\Users\whale\Desktop\test\docx\complex\silic

    for filename in filelist:
        #print filename silic.docx
        if filename.endswith('docx'): #提取出docx图片到同名文件夹，并且删除多余文件。
            handleDocx.my_unzip(path)
            handleDocx.delete(path)
            break
        else:
            copyFile(path)
            IsDir(path)
            for a in List:
                for b in a:
                    os.remove(b)
            break
    for i in pic_path:
        #print i
        #word_media=filepath.strip(".docx")
        for root,dirs,files in os.walk(i):
            for h in files:
                docxPicPath = i+"\\"+h
                #print 'docxpicpath:'+docxPicPath
                WaterMark(docxPicPath,mark)  

def startButton():
    path = name.get().replace("\\","\\\\")    
    radSel = GUIchoice.get()
    if   radSel == 1: 
        global mark
        mark="i"
        judgment(path,mark)  

    elif radSel == 2: 
        #rad2.configure(text='done ' + name.get())
        mark="e"
        judgment(path,mark)  

if __name__ == '__main__':
    win = tk.Tk()
    win.title("Watermark Program")
    win.resizable(0,0)

    ttk.Label(win,text="Input the path of the picture: ").grid(column=0,row=0)

    action = ttk.Button(win, text="start",command=startButton)
    action.grid(column=3,row=0)

    name = tk.StringVar()
    nameEntered = ttk.Entry(win, width=50, textvariable=name)
    nameEntered.grid(column=1, row=0)
    nameEntered.focus()

    GUIchoice = tk.IntVar()
    rad1=tk.Radiobutton(win,text='i chunqiu',variable=GUIchoice,value=1) #,command=
    rad1.grid(column=0,row=1,sticky=tk.W)    
    rad1.select()

    rad2 = tk.Radiobutton(win,text='e chunqiu',variable=GUIchoice,value=2) #,command=
    rad2.grid(column=1,row=1,sticky=tk.W)

    win.mainloop()  
        


   
        
            


