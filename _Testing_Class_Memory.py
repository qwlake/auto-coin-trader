# import tracemalloc
# import ctypes
# from sys import getsizeof

# class f():
#     def __init__(self, a):
#         self.a = a
        
# class b():
#     def __init__(self, a):
#         self.a = a
#     def run(self):
#         list1 = []
#         for i in range(5):
#         	testing = f(2)
#         	list1.append(testing)
#         return list1

# tracemalloc.start()
# time1 = tracemalloc.take_snapshot()

# test = b(1)

# list1 = test.run()

# time2 = tracemalloc.take_snapshot()
# stats = time2.compare_to(time1, 'lineno')
# # for i in stats:
# # 	print(i,'\n')
    
# print(id(list1[0]))

# fid = id(list1[0])
# listid = id(list1)

# time2 = tracemalloc.take_snapshot()
# stats = time2.compare_to(time1, 'lineno')
# # for i in stats:
# # 	print(i,'\n')

# # for e in list1:
# #     del e
# del list1[0]
# del list1[0]
# del list1[0]
# del list1[0]
# del list1[0]
# del list1

# # time3 = tracemalloc.take_snapshot()
# # stats = time3.compare_to(time2, 'lineno')
# # for i in stats:
# # 	print(i,'\n')

# print(ctypes.cast(listid, ctypes.py_object).value)

import math
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as pt

################################################################################

start_time = time.time()

def sigmoid(x, a=1):
    return 1 / (1 + np.exp(-(a*x))) # numpy의 브로드캐스트
 
x = np.array([-1.0, 1.0, 2.0])
#print(np.exp(-x))
y = sigmoid(x)
print(y)
 
x = np.arange(-10, 10, 0.1)
y = sigmoid(x)
pt.plot(x,y)
pt.ylim(-0.1, 1.1)
pt.show()

a = 0.05

t1 = sigmoid(130, a)
t2 = sigmoid(100, a)
t3 = sigmoid(100, a)
t4 = sigmoid(50, a)

# t1 = sigmoid(60, a)
# t2 = sigmoid(30, a)
# t3 = sigmoid(30, a)
# t4 = sigmoid(-20, a)

print(t1-t2,t3-t4)

# u, d = 130, 100
# rate = np.log(u+2)/np.log10(d+u+2)*u-d
# print(rate)

# u, d = 100, 50
# rate = np.log(u+2)/np.log10(d+u+2)*u-d
# print(rate)

# u, d = 30, 15
# rate = np.log(u+2)/np.log10(d+u+2) + (u*0.007) - (d*0.007)
# print(rate)

# u, d = 150, 450
# rate = np.log(u+2)/np.log10(d+u+2) + (u*0.007) - (d*0.007)
# print(rate)

# u, d = 47, 20
# rate = np.log(u+2)/np.log10(d+u+2) + (u*0.007) - (d*0.007)
# print(rate)

# u, d = 20, 0
# rate = np.log(u+2)/np.log10(d+u+2) + (u*0.007) - (d*0.007)
# print(rate)

# u, d = 47, 20
# rate = np.log(u+2)/np.log10(d+u+2)*u-d
# print(rate)

# u, d = 20, 0
# rate = np.log(u+2)/np.log10(d+u+2)*u-d
# print(rate)

end_time = time.time()-start_time
print("time:", end_time)

################################################################################

# def fun1(n):
# 	return range(n)
# a = fun1(10)
# print(type(a))

################################################################################

# list1 = []
# for i in range(10):
#     list1.append(1)
# nplist = np.array(list1)
# print(nplist)
# print(np.shape(nplist))

################################################################################

# start_time = time.time()
# lst = [0 for _ in range(10)]
# print(lst)
# end_time = time.time()-start_time
# print("time:", end_time)

# start_time = time.time()
# result = [0]*10
# print(result)
# end_time = time.time()-start_time
# print("time:", end_time)

################################################################################

# list1 = [1, 2, 3]
# nd = np.array(list1)

# t = np.isfinite(nd)
# print(t)
# i = np.invert(t)
# print(i)


# nd[i] = 0
# print(nd)

################################################################################

# list1 = []
# print(list1)
# np = np.array(list1)

# minV = np.min(np)

# print(minV)

################################################################################

# bool1 = False
# bool2 = False

# if not bool1 or not bool2:
#     print("yes")
    
    
################################################################################

# a = 0
# b = 30

# a = np.array(a)
# b = np.array(b)

# print(a/b)


################################################################################

# list1 = [1,1,1,1,1]
# list2 = [2,2,2,2,2,2,2,2,2,2]
# list3 = [1,2,3,4,5,6,7,8,9,10]

# lst1 = []
# for i in range(10):
#     lst2 = []
#     for j in range(20):
#         lst2.append(list3)
#     lst1.append(lst2)
    
# a = np.array(lst1)
# print(np.shape(a), a)

# for i, e in enumerate(a):
#     for j in range(10):
#     	print(e[:,j])


################################################################################

# t = None
# q = [1,2,3,4,5,6]
# w = q[1:t]
# print(w[None])

################################################################################

# temp = []
# for i in range(1,16):
#     temp.append(i*0.065)
    
# print(temp)
################################################################################

import random
for i in range(10):
	print(random.randint(0,3))


