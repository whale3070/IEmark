# -*- coding: utf8 -*-

import os
from PIL import Image,ImageEnhance

num=0

def set_opacity(im, opacity):
    """设置透明度"""
 
    assert opacity >=0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im
 
def watermark(im, mark, position, opacity=1):
    """添加水印"""
 
    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        #if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            #print "The mark image size is larger size than original image file."
            #return False
 
        #设置水印位置
        if position == 'left_top':
            x = 0
            y = 0
        elif position == 'left_bottom':
            x = 0
            y = im.size[1] - mark.size[1]
        elif position == 'right_top':
            x = im.size[0] - mark.size[0]
            y = 0
        elif position == 'right_bottom':
            x = im.size[0] - mark.size[0]-5
            y = im.size[1] - mark.size[1]-30
        else:
            x = (im.size[0] - mark.size[0]) / 2
            y = (im.size[1] - mark.size[1]) / 2
 
        layer = Image.new('RGBA', im.size,)
        layer.paste(mark,(x,y))
        return Image.composite(layer, im, layer)
    except Exception as e:
        #print ">>>>>>>>>>> WaterMark EXCEPTION:  " + str(e)
        return False
 
def water(filename,mark):
    try:
        im = Image.open(filename) #原图
        image = watermark(im, mark, 'right_bottom', 1)
        image.save(filename)
        #image.show()
    except Exception as e:
        return False
        
def dirlist(path,mark):#返回指定的文件夹包含的文件或文件夹的名字的列表    
    global num         #所以指定目录下的所有图片都会被打水印
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath,mark)
        else:
            water(filepath,mark)
            num += 1
            print filepath, num
 

        


