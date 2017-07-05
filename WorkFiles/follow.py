# follow.py
#
# Follow a file like tail -f.

import time
def follow(thefile,i):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            i = 0
            print("sleeping")
            time.sleep(5)

            continue
        yield line

if __name__ == '__main__':
    logfile = open("access.log","r")
    i = 0
    loglines = follow(logfile,i)

    for line in loglines:
        print (line),
        i += 1
        print (i)
