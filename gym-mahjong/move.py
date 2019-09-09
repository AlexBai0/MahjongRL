# import os
# import shutil
# import os.path
#
# class Traverse:
#     def __init__(self,workdir):
#         self.workdir = workdir
#
#     def traversefile(self,workdir):
#         count = 1
#         for filename in os.listdir(workdir):
#             file = os.path.join(workdir,filename)
#             if os.path.isdir(file):
#                 # print(file)
#                 count += self.traversefile(file) #计算该目录下所有的目录个数
#             else:
#                 continue
#         return count
#
#
# workdir = "/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/utils/converted/mjlog_pf4-20_n9"
# traverse = Traverse(workdir)
# print (traverse.traversefile(workdir))
# n=800001
# tgt = "/System/Volumes/Data/Users/alexbai/Desktop/Project/MahjongAIagent/sxb1376/utils/converted/gamelogs"
# for game in os.listdir(workdir):
#     for round in os.listdir(os.path.join(workdir,game)):
#         new_name = str(n)+'.txt'
#         n += 1
#         srcF = os.path.join(os.path.join(workdir,game),round)
#         tgtF = os.path.join(tgt,new_name)
#         shutil.copy(srcF,tgtF)
# # import numpy as np
# # a = np.array([[1,2,3],[4,5,6]])
# # a = a[np.newaxis , :]
# # print(a)

import numpy as np
a = np.zeros(34)
para = a.reshape(34, 1)
print(a)
print(para)

