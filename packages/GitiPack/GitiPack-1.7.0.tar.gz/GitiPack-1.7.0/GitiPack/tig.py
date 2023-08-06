import time


webg()

def ctig():
    global f
    f = open("Tig-Go.tig", 'a', encoding="UTF-8")
    f.write("————————————\n")
    ti = time.strftime("%Y-%m-%d %H:%M:%S\n", time.gmtime())
    f.write(ti)

def webg():
    ctig()
    f.write("Deal with: giti-web.github.io\n")

def ctime():       #获取当前时间戳
    return time.time()

def mtime():       #返回可读字符串
    return time.ctime()

def stime():       #返回格式化后的时间
    return time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())

# ——————————

def w(r):
    f.write(r)
    f.write('\n')

# ——————————

def jc(n):                 #阶乘
    if n == 1:
        return 1
    else:
        return jc(n-1)*n

def pertion(l, s, e):      #对列表进行全排列
    w("进行全排列")
    if s == e:
        w(','.join(l))
    else:
        for i in range(s,e+1):
            l[s],l[i]=l[i],l[s]
            # 将这个元素和第一个元素交换
            pertion(l,s+1,e)
            l[s],l[i]=l[i],l[s]
            # 换回位置

def gcd(n1, n2):            #最大公因数
    return gcd(n2,n1%n2) if n2>0 else n1

def lcm(n1, n2):            #最小公倍数 (必须在有楼上的情况下)
    return n1*n2//gcd(n1,n2)

def power(base,exponent):   #快速幂
    res=1
    while exponent:
        if exponent & 1:  #判断当前的最后一位是否为1，如果为1的话，就需要把之前的幂乘到结果中
            res*=base
        base*=base  #一直累乘，如果最后一位不是1的话，就不用了把这个值乘到结果中，但是还是要乘
        exponent=exponent>>1
    return res

