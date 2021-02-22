#! /usr/bin/env python3
# going through usr/bin/env to find the executible format
import os,sys,re #importing the os sys and re libraries for us to use.

def readline(): #method to read lines
    while True:#while True do the following
        environmentsetup()
        args=os.read(0,1024)#file discriptor is 0 and it reads 1 kb of characters        
        buffers=args.decode()#decodes the bytes into character strings
        newlinebuffer=buffers.splitlines()#will split the buffer list in to another list based on new lines
        for i in newlinebuffer:#this is for reading a line 
            execute(i.split())#will take the line and split them put them in a list and passed to execute
            
def execute(args):#Method called execute that takes in arguemnts which is a list
    if len(args)==0: #if arguments list is 0 then it will just return
        return
    elif args[0]=="pwd":#if user types pwd
        x=os.getcwd()#gets current working directory
        os.write(1,("%s\n"%x).encode())#writes the currend print working directory
    elif args[0].lower()=="exit": #if user says exit no matter what way you will exit
        sys.exit(0)
    elif args[0]=="cd..":#if argument is cd.. then user will go up one directory
        os.chdir("..")
    elif args[0]=="cd":#if users just inputs cd try and do one of the following
        try:
            if len(args)==2:#needs length 2 to change dir since we will be using what comes after cd
                os.chdir(args[1])#changes dir to name of second argument
            elif len(args)>2:#if more than 2 arguments then send error message
                os.write(1,("To many arguments try again"))
            else: #set path to home path 
                os.chdir(os.getenv("HOME"))
        except:#if not found then write the meesage 
            os.write(1,("cd %s: No file or directory with that name found" % args[1]).encode())
            pass
    elif "|" in args:#if | in args then create a pipe
        pipe(args)#goes to pipe method with arguments
    else:
        rc=os.fork()#creates a child process
        if rc < 0:# if returns 0 then fork failed
            os.write(2,("Fork failed, now returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc==0:#if the return value is 0 then go into commands method with the arguments
            command(args)#passes arguemnts to command method
        else:#child will wait till execution is done
            childpid=os.wait()
            
def pipe(args):#the pipes method that take in arguments
    left=args[0:args.index("|")]# gets data of left side of arguments before |
    right=args[len(left)+1:]#gets the data of right side of arguments after |
    pRead, pWrite = os.pipe()#making the read and write 
    rc=os.fork()##creates a child process
    if rc<0:# if the returns a 0 the for failed
        os.write(2, ("Fork has failed returning now %d\n" %rc).encode())#
        sys.exit(1)# used to exit
    elif rc==0:#if return value is 0 do the following
        os.close(1)#close file descriptor 1
        os.dup(pWrite)#copies the file descriptors of the child and puts it into pWrite
        os.set_inheritable(1,True)#
        for fd in (pRead,pWrite):
            os.close(fd)#closes all the file descriptors
        command(left)#inputs the left argument into commands
    else:
        os.close(0)#closes file descriptor 0
        os.dup(pRead)#copies the files descriptor of the parent and puts it into pRead
        os.set_inheritable(0,True)#
        for fd in (pWrite, pRead):
            os.close(fd)#closes file descriptors in both pRead,pWrite
        if "|" in right:#if it finds '|' on the right side of argument then it's piping it with right's varaibles
            pipe(right)#goes into pipe with variable pipe
        command(right)#inputs the right argument into commands
        
def redirect(args):
    if '>' in args:#Goes into redirection
        os.close(1)#close file descriptor 1
        os.open(args[args.index('>')+1],os.O_CREAT | os.O_WRONLY)#will create a file or write to a file depending on the bit
        os.set_inheritable(1,True)#set's inhertiable file descriptor for 1
        args.remove(args[args.index('>')+1])#remove info on the right of >
        args.remove('>')#remove the symbol no longer needed
    else:
        os.close(0)#close file descriptor 0
        os.open(args[args.index('<')+1],os.O_RDONLY)#open a file and reads only.
        os.set_inheritable(0,True)#set's inheritable file descriptor for 0
        args.remove(args[args.index('<')+1])#remove the info on the right
        args.remove('<')#remove the symbol and it's no longer needed

    for dir in re.split(":", os.environ['PATH']):
        prog = "%s/%s" % (dir,args[0])#load path and dir
        try:
            os.execve(prog, args, os.environ)#execute the program
        except FileNotFoundError:
            pass
    os.write(2, ("%s: command not found\n" %args[0]).encode())#if command fails write this to shell and exit
    sys.exit()
    
def command(args):#create a method called command that will take in arguments
    if "/" in args[0]:#if / found in argument then do the following
        program=args[0]#puts argument 0 into the value called program
        try:
            os.execve(program,args,os.environ)#execute a process with enviornment in mind
        except FileNotFoundError:
            pass
    elif ">" in args or "<" in args:#This is for if there's redirection in the argument
        redirect(args)#if there is redirection go to redirection with arguments
    else:
        for dir in re.split(":", os.environ['PATH']):#breaks the path apart by ppattern of : in the environment variable path
            program = "%s/%s" % (dir, args[0])#passes dir into first % to set up the file path then puts the first word in teh argument into the second %
            try:
                os.execve(program, args, os.environ)#tries to execute with given the parameters of program being the path, args being the argumetns and os.environ being the enviornment
            except FileNotFoundError:
                pass
    os.write(2, ("%s: command not found\n" % args[0]).encode())#error code 
    sys.exit()
    
def environmentsetup():    
    if 'PS1'in os.environ: #if PS1 is defined in the enviornemtn is defined
        os.write(1, (os.environ['PS1']).encode())#write with file descriptor 1 the enviornemnt pathof PS1
    else:#if PS1 is not found 
        os.write(1, ("> ").encode())
        
readline()
