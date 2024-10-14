from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
#import matplotlib.pyplot as plt
import string
import random
import numpy as np
import argparse
import os
import time
def SplitHMS(seconds):
    h = int(seconds/3600)
    hr = seconds%3600
    m = int(seconds/60)
    s = int(seconds%60)
    return h,m,s
def GetImageGrayScale(imgname):
    return Image.open(imgname).convert('LA')
def GetPercentage(m1,m2):
    return (m1*100)/m2
def GetLoadingBar(m1,m2):
    return int((m1*10)/m2)
def ConvertImage(img,Scale=9):
    size = img.size
    keycharss = "abcdefghjkmnopqrsuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ"
    keychars = []
    for x in range(int(size[0]/Scale)):
        ykey = []
        for y in range(int(size[1]/Scale)):
            key = random.choice(keycharss)
            ykey.append(key)
        keychars.append(ykey)
        ma = GetPercentage(x+1,size[0]/Scale)
        mb = GetLoadingBar(x+1,size[0]/Scale)
        print("Chars Creating %s%s [%s%s]  \r"%("%",ma,"="*mb," "*(10-mb)),)
    img = img.convert("LA").convert("RGB")
    imgz = Image.new('RGB', size)
    draw = ImageDraw.Draw(imgz)
    font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SEGOEUI.TTF", Scale)
    for x in range(int(size[0]/Scale)):
        for y in range(int(size[1]/Scale)):
            key = keychars[x][y]
            pos = (int(x*Scale),int(y*Scale))
            pixel = img.getpixel(pos)
            if(np.mean(pixel)/255.0 > 0.4):
                draw.text(pos,random.choice(string.ascii_uppercase),(pixel[0],pixel[1],pixel[2]),font=font)
            else:
                draw.text(pos,key,(pixel[0],pixel[1],pixel[2]),font=font)
        ma = GetPercentage(x+1,size[0]/Scale)
        mb = GetLoadingBar(x+1,size[0]/Scale)
        print("Image Creating %s%s [%s%s]  \r"%("%",ma,"="*mb," "*(10-mb)),end="\r")
    return imgz
def ConvertImageX(img,Scale=9,Xchar="=",alphanum = 0.4):
    size = img.size
    keycharss = "abcdefghjkmnopqrsuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ"
    keychars = []
    for x in range(int(size[0]/Scale)):
        ykey = []
        for y in range(int(size[1]/Scale)):
            key = random.choice(keycharss)
            ykey.append(key)
        keychars.append(ykey)
        ma = GetPercentage(x+1,size[0]/Scale)
        mb = GetLoadingBar(x+1,size[0]/Scale)
        print("Chars Creating %s%s [%s%s]  \r"%("%",ma,"="*mb," "*(10-mb)),end="\r")
    img = img.convert("LA").convert("RGB")
    imgz = Image.new('RGB', size)
    draw = ImageDraw.Draw(imgz)
    font = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SEGOEUI.TTF", Scale)
    bm = time.time()
    h,m,s = SplitHMS(((size[0]/Scale)-x)*(time.time()-bm))
    d=0
    for x in range(int(size[0]/Scale)):
        bm = time.time()
        for y in range(int(size[1]/Scale)):
            key = keychars[x][y]
            pos = (int(x*Scale),int(y*Scale))
            pixel = img.getpixel(pos)
            if(np.mean(pixel)/255.0 > alphanum):
                draw.text(pos,Xchar,(pixel[0],pixel[1],pixel[2]),font=font)
            else:
                draw.text(pos,key,(pixel[0],pixel[1],pixel[2]),font=font)
        if(x%50):
            h,m,s = SplitHMS(((size[0]/Scale)-x)*(time.time()-bm))
            s = int(np.mean([d,s]))
            d =s
        ma = GetPercentage(x+1,size[0]/Scale)
        mb = GetLoadingBar(x+1,size[0]/Scale)
        print("Image Creating %s%s [%s%s] Kalan Sure : %ss %sm %sh   \r"%("%",ma,"="*mb," "*(10-mb),s,m,h),)
    return imgz
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image","-i",help="Fotograf konumu",required=True,type=str)
    parser.add_argument("--scale","-S",help="Font buyuklugu",type=int,default=9)
    parser.add_argument("--usexchar","-UX",help="XChar ",action="store_true")
    parser.add_argument("--alphanum","-A",help="Belirlediginiz opakligin ustune ulasan pixellere xchar atanir. Default=0.4 (0>x>1)",type=float,default=0.4)
    parser.add_argument("--xchar","-X",help="Belirlediginiz opakligin ustune ulasan pixellere xchar atanir. Default='='",type=str,default="=")
    args = parser.parse_args()
    if(args.image):
        print("d1")
        if(os.path.isfile(args.image)):
            print("d2")
            if(args.usexchar):

                print("Using xchar.")
                fname =args.image
                img = GetImageGrayScale(fname)
                newimg = ConvertImageX(img,args.scale,args.xchar,args.alphanum)
                newimg.save("edited.%s"%(fname))
            else:
                fname =args.image
                img = GetImageGrayScale(fname)
                newimg = ConvertImage(img,args.scale)
                newimg.save("edited.%s"%(fname))
            #plt.imshow(newimg)
            #plt.show()
    else:
        parser.print(usage())
if __name__ == '__main__':
    main()
