import os
from subprocess import Popen, PIPE


def run_pipes(cmds):
    """
    Run commands in PIPE, return the last process in chain
    """
    first_cmd, *rest_cmds = cmds
    procs = [Popen(first_cmd, stdout=PIPE)]
    for cmd in rest_cmds:
        last_stdout = procs[-1].stdout
        proc = Popen(cmd, stdin=last_stdout, stdout=PIPE)
        procs.append(proc)
    return procs[-1]

def changedir(args):
    os.chdir(args[1])


def main():
    while(True):
        currdir = os.getcwd()
        countpipe = 0
        data = input("user@developer:"+currdir+"$")
        data = data.split(' ')
        for i in range(len(data)):
            cur = data[i]
            if '|'==cur:
                countpipe+=1
        cmd = []
        testdata = data
        cur = 0
        for i in range(len(testdata)):
            if testdata[i] == "|":
                cmd.append(testdata[cur:i])
                cur = i+1
        cmd.append(testdata[cur:])
        if countpipe==0:    
            if data[0]=='cd':
                changedir(data)
            else:
                pid = os.fork()
                if not pid:
                    os.execvp(data[0],data)
                else:
                    os.wait()

        else:
            last_proc = run_pipes(cmd)
            stdout = last_proc.stdout
            for line in stdout:
                line = line.decode()
                print(line, end="")

if __name__=='__main__':
    main()