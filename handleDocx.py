#coding:utf-8
import zipfile
import os
import shutil

#global word_media #这是提取出的图片所在的绝对路径

fileList=[]
del_list=['\\_rels','\\customXml','\\docProps','\\word']

def extractDocx(path,savepath):
    f=zipfile.ZipFile(path,'r')

    for file in f.namelist():
        f.extract(file,savepath)

def my_unzip(rawpath):
    path=rawpath.replace("\\","\\\\")

    for root,dirs,files in os.walk(path):
        for h in files:                 #h为子文件每一项   
            fileList.append(h)
    for i in fileList:
        if i.endswith("docx"):            
            docxName = i.strip(".docx") #文件名，之后水印以该文件名保存
            before = path+"\\\\"+i
                      
            extractDocx(before,path)
            media=path+"\\\\word\\\\media"                  
            shutil.copytree(media, path+"\\"+docxName) #复制图片         

def delete(path):
    os.remove(path+"\\[Content_Types].xml")
    for i in del_list:
        raw_rm_path=path+i
        rm_path=raw_rm_path.replace("\\","\\\\")
        #print rm_path
        try:
            shutil.rmtree(rm_path)
        except:
            pass

#path='C:\\Users\\whale\\Desktop\\test\\12'
#my_unzip(path)
#delete(path)
