import os
from glob import glob
import re

l = 'D:\\Face\\Tensor_ver\\1'
fl=glob(os.path.join(l,'*'))
fl=sorted(fl)
# zn=os.path.basename(fl[-1])
# x=re.findall('\d+',zn)
x=len(fl)
zn=len(str(x))

for i in fl:
    # n=os.path.basename(i)
    dir,n=os.path.split(i)
    fexe=os.path.splitext(n)[-1]
    x = re.findall('\d+', n)
    fn=x[0].zfill(zn)+fexe
    fn=os.path.join(dir,fn)
    os.rename(i,fn)
