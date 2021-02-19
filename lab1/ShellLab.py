#! /usr/bin/env python3
# going through usr/bin/env to find the executible format
import os,sys,re #importing the os sys and re libraries for us to use.

def readline(): #method to read lines
    args=os.read(0,1024)#file descriptor is 0 and it reads 1024 bytes
    while True:#while True do the following
        buffers=args.decode()#decodes the bytes into character strings
        os.write(1,f"{buffers}".encode())#will write using file descriptor 1 and show the message in the fstring which is buffers.
        newlinebuffer=buffer.splitlines()#will split the buffer list in to another list based on new lines
        for i in newlinebuffer:
            i.split()

    
