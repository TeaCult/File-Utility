from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
import os
import time
import sys
import math
import random
import datetime
import urllib.request
import inspect
import re
from subprocess import Popen
from subprocess import PIPE

def runsysOld(s):
	with Popen(s.split(' '), stdout=PIPE) as proc:
		return proc.stdout.read().decode('utf-8')

def runsys(s):
	return os.popen(s).read()

def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def inspectAllVarSizes():
    for name, size in sorted(((name, sys.getsizeof(value)) for name, value in locals().items()),
                             key=lambda x: -x[1])[:10]:
        print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))


def readFromFile(fn):
	f=open(fn,'r')
	s=f.readlines()
	f.close()
	return s

def overwriteToFile(s,fn):
	f=open(fn,'w')
	f.writelines(s)
	f.close()
	return 0

def appendToFile(s,fn):
	f=open(fn,'+a')
	f.write(s)
	f.close()
	return 0

def readLines(fn):
	f=open(fn,'r')
	s=f.readlines()
	f.close()
	for i in range(len(s)):
		s[i]=s[i].replace('\n','');
	return s

def appendLines(s,fn):
	f=open(fn,'+a')
	for i in range(len(s)):
		s[i]=s[i]+'\n';
	f.write(''.join(s))
	f.close()
	return 0

def overwriteLines(s,fn):
	f=open(fn,'w')
	for i in range(len(s)):
		s[i]=s[i]+'\n';
	f.write(''.join(s))
	f.close()
	return 0



window = Tk()
window.title("First Prototype of Folder Compare written by G.G.")
window.geometry('1200x900')
lbl = Label(window, text="Folder1")
lbl2 = Label(window, text="Folder2")
lbl.grid(column=0, row=0)
lbl2.grid(column=0, row=1)
txt = Entry(window, width=50)
txt.grid(column=1, row=0)
txt2 = Entry(window, width=50)
txt2.grid(column=1, row=1)

def dComp(loc):
    b = os.popen("sudo find '"+loc+"' -type f").read().split('\n')
    b.pop()
    out = []
    for i in b:
        fname = i.replace('\n', '')
        size = int(os.popen("du -k '"+i+"'").read().split('\t')[0])
        typ = os.popen("file -b '"+i+"'").read().replace('\n', '')
        check = os.popen("md5sum '"+i+"'").read().split(' ')[0]
        out.append(check+'\t'+i+'\t'+str(size)+' kb'+'\t'+typ)
    return out

    #val = int(i.split('\t')[0].strip())
    #total = total+val
    #print(total, 'kB = ', round(total/1024, 2), 'MB = ', round(total/1024/1024, 2), '= GB')
    # for i in out:
    #    print(i)


def comp(loc):
    b = os.popen("sudo find '"+loc+"' -type f").read().split('\n')
    b.pop()
    out = []
    for i in b:
        fname = i.replace('\n', '')
        stat = os.popen('''stat -c "%y %s %n" "''' +
                        i+'"').read().replace('\n', '')
        out.append(stat)
    return out


def clicked():
    f1 = txt.get()
    f2 = txt2.get()
    scrltxt.insert(tk.INSERT, '')
    btn["text"] = "Checking"
    btn["state"] = "disabled"
    a = dComp(f1)
    b = dComp(f2)

    report = []

    for i in a:
        i = i.replace(f1, '')
        isOK = False
        for k in b:
            k = k.replace(f2, '')
            if i == k:
                isOK = True
        if not isOK:
            report.append('Folder 2 is missing: '+i+'\n')

    for i in b:
        i = i.replace(f2, '')
        isOK = False
        for k in a:
            k = k.replace(f1, '')
            if i == k:
                isOK = True
        if not isOK:
            report.append('Folder 1 is missing: '+i+'\n')

    for i in range(len(a)):
        a[i] = a[i]+'\n'

    for i in range(len(b)):
        b[i] = b[i]+'\n'
    # print(a+b)
    # print('REPORT:\n',report)
    scrltxt["state"] = "normal"
    scrltxt.insert(tk.INSERT, "FOLDER 1: "+f1+"\n"+''.join(a) +
                   "\n\nFOLDER 2: "+f2+"\n"+''.join(b)+"\n\nREPORT:\n"+''.join(report))
    btn["text"] = "Compare"
    btn["state"] = "active"
    scrltxt["state"] = "disabled"
    #inspectAllVarSizes()


def clicked2():
    f1 = txt.get()
    f2 = txt2.get()
    scrltxt.insert(tk.INSERT, '')
    btn["text"] = "Checking"
    btn["state"] = "disabled"
    a = comp(f1)
    b = comp(f2)

    report = []

    for i in a:
        i = i.replace(f1, '')
        isOK = False
        for k in b:
            k = k.replace(f2, '')
            if i == k:
                isOK = True
        if not isOK:
            report.append('Folder 2 is missing: '+i+'\n')

    for i in b:
        i = i.replace(f2, '')
        isOK = False
        for k in a:
            k = k.replace(f1, '')
            if i == k:
                isOK = True
        if not isOK:
            report.append('Folder 1 is missing: '+i+'\n')

    for i in range(len(a)):
        a[i] = a[i]+'\n'

    for i in range(len(b)):
        b[i] = b[i]+'\n'
#    print(a+b)
#    print('REPORT:\n',report)
    scrltxt["state"] = "normal"
    scrltxt.insert(tk.INSERT, "FOLDER 1: "+f1+"\n"+''.join(a) +
                   "\n\nFOLDER 2: "+f2+"\n"+''.join(b)+"\n\nREPORT:\n"+''.join(report))
    btn["text"] = "Compare"
    btn["state"] = "active"
    scrltxt["state"] = "disabled"
    #inspectAllVarSizes()

def clicked3():
    overwriteToFile(scrltxt.get("1.0", tk.END),'Comparision at '+str(time.time())+'test')

btn = Button(window, text="Compare Folders", command=clicked2)
btn2 = Button(window, text="Compare Folders Byte by Byte", command=clicked)
btn3 = Button(window, text="Save Output", command=clicked3)

btn.place(relx=0.5, rely=0, anchor=NW)
btn2.place(relx=0.5, rely=0.04, anchor=NW)
btn3.place(relx=0.9, rely=0.96, anchor=NW)

scrltxt = scrolledtext.ScrolledText(
    window, width=168, height=50, state="disabled")
scrltxt.place(relx=0, rely=0.1, anchor=NW)
window.mainloop()
