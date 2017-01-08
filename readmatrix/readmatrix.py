# -*- coding: utf-8 -*-
"""
Created on Sat Jan 07 14:01:06 2017

@author: test2
"""

import numpy as np


def ReadMatrix(row_num,column_num,filename):
    
    lists_of_read = []
    try:
        inputfid = open(filename,'rb')
    except IOError as e:
        print "Error: file open error: ",e
    else:
        for eachline in inputfid:
            lists = eachline.strip().split()
            for ii in range(len(lists)):
                lists_of_read.append(float(lists[ii]))
       
        if len(lists_of_read) > row_num * column_num:
            print 'numbers of data in file ' + filename + \
            ' are greater than the maxtrix you set!'
            return -1
        elif len(lists_of_read) < row_num * column_num:
            print 'numbers of data in file ' + filename + \
            ' are less than the maxtrix you set!'
            return -1
        else:
            arr = np.array(lists_of_read)
            arr = arr.reshape(row_num,column_num)
            return arr

def WriteMatrix(arr,filename):
    try:
        outputfid = open(filename,'w')
    except IOError as e:
        print "Error: file open error: ",e
    else:
        if type(arr) is int:
            print 'Matrix print in ' + filename + ' failed!'
        else:
            (row_num,column_num) = arr.shape
            for ii in range(row_num):
                if ii != 0:
                    outputfid.write('\n')
                for jj in range(column_num):
                    outputfid.write("%12.4f " %arr[ii][jj])
            
if __name__ == '__main__':
    arr = ReadMatrix(4,4,'test.txt')
    WriteMatrix(arr,'write.txt')    
     
            
        
        