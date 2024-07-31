import os

def check():
    f = open(os.getcwd()+'/telegram/checker/check.txt', 'r')
    cc = f.read()
    f.close()
    return cc=='1'