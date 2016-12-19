from PIL import Image,ImageEnhance
import requests
from io import BytesIO
import numpy as np
import uuid
import os
import time
import itertools
import copy
from captcha import TotallyShit,clf
global visited
from random import Random
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def checkPoint(im,i,j):
    ret=0
    #print(arr[5])
    for ii in range(max(i-1,0),min(i+2,64)):
        for jj in range(max(j-1,0),min(j+2,21)):
            if(im.getpixel((ii,jj))==0):
                ret += 1

    return ret

def getVisited(im,x,y):
    global visited
    global totalvisited
    if x<=65 and x>=0  and y>=0 and y<=22:
        if im.getpixel((x,y))==0:
            visited.append((x,y))
            totalvisited.append((x, y))
            if(x,y+1) not in visited:
                getVisited(im,x,y+1)
            if (x, y -1) not in visited:
                getVisited(im,x, y - 1)
            if (x+1, y ) not in visited:
                getVisited(im,x+1, y)
            if (x - 1, y) not in visited:
                getVisited(im, x - 1, y)

flag=1
while(flag):
    s = requests.session()
    response = s.get("http://tkkc.hfut.edu.cn/getRandomImage.do")
    print("获取验证码OK")
    img = Image.open(BytesIO(response.content))
    img.save("temp0.bmp")
    img.show()
    print(str(img.size[0]) + " * " + str(img.size[1]))
    Lim  =  img.convert( 'L' )
    threshold  =   70
    table  =  []
    for  i  in  range( 256 ):
          if  i  <  threshold:
             table.append(0)
          else :
             table.append( 1 )
     #  convert to binary image by the table
    bim  =  Lim.point(table, '1')
    bim2=copy.deepcopy(bim)
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            if bim.getpixel((i,j))==0 and checkPoint(bim,i,j)<=2:
                bim2.putpixel((i,j),255)
            else:
                pass
    bim.save("temp.bmp")
    bim2.save("temp2.bmp")
    global visited
    global totalvisited
    split_result=[]
    visited = []
    totalvisited = []
    #bim2.show()
    #cap = input("输入整个验证码:")
    cnt=0
    clf2 = clf()
    ans=""
    for i in range(0, img.size[0]):
        if((i,10) not in totalvisited and bim2.getpixel((i,10))==0):
            visited = []
            getVisited(bim2, i,10)
            max_x=(max(visited,key=lambda x: x[0])[0])
            min_x=(min(visited,key=lambda x: x[0])[0])
            max_y=(max(visited,key=lambda x: x[1])[1])
            min_y=(min(visited,key=lambda x: x[1])[1])
            split_result.append((min_x,min_y,max_x,max_y))
            box = (min_x,min_y,max_x,max_y)
            #print(visited)
            #print (box)
            crop = bim2.crop(box)
            crop=crop.resize((20, 20), Image.ANTIALIAS)
            # if not os.path.exists('Alpha/' + cap[cnt]):
            #     os.makedirs('Alpha/' + cap[cnt])
            # crop.save("Alpha/" + cap[cnt] + "/" + random_str() + ".bmp")

            #开始识别
            gim = crop.convert("L")
            np_part_array = np.array(TotallyShit(gim)).reshape(1,-1)
            predict_num = clf2.predict(np_part_array)
            ans+=predict_num[0]
            cnt+=1
    print(split_result)
    print("验证码为:"+ ans)
    flag=0
