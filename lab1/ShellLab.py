#! /usr/bin/env python3
# going through usr/bin/env to find the executible format
import os,sys,re #importing the os sys and re libraries for us to use.

def readline(): #method to read lines
    args=os.read(0,1024)#file descriptor is 0 and it reads 1024 bytes
    while True:#while True do the following
        buffers=args.decode()#decodes the bytes into character strings
        os.write(1,f"{buffers}".encode())#will write using file descriptor 1 and show the message in the fstring which is buffers.
        newlinebuffer=buffers.splitlines()#will split the buffer list in to another list based on new lines
        for i in newlinebuffer:
            i.split()
        args=os.read(0,1024)

def execute(args):#Method called execute that takes in arguemnts which is a list
    if len(args)==0: #if arguments list is 0 then it will just return
        return
    elif args[0].lower()=="exit": #if user says exit no matter what way you will exit
        sys.exit(0)
    elif args[0]=="cd..":#if argument is cd.. then user will go up one directory
        chdir(".."}
    elif args[0]=="cd":#if users just inputs cd try and do one of the following
        try:
            if len(args)==2:#needs length 2 to change dir since we will be using what comes after cd
                os.chdir(args[1])#changes dir to name of second argument
            elif len(args>2):#if more than 2 arguments then send error message
                os.write(1,("To many arguments try again")
            else:#set path to home path 
                os.chdir(getenv("HOME"))
        except:
            os.write(1,("cd %s: No file or directory with that name found" % args[1]).encode())
            pass
    

while True:
    if 'PS1'in os.environ: #if PS1 is defined in the enviornemtn is defined
        os.write(1, (os.environ['PS1']).encode())#write with file descriptor 1 the enviornemnt pathof PS1
    else:#if PS1 is not found 
        os.write(1, ("> ").encode())
    readline()
