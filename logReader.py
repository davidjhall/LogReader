# follow.py
#
# Follow a file like tail -f.
# 10:11 - 12:12

import time
def follow(thefile):
    concat = list()
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            print("sleeping")
            time.sleep(5)
            continue
        while (line):
            concat.append(line)
            line = thefile.readline()
        # print(concat)
        yield concat
        concat[:] = []

if __name__ == '__main__':
    logfile = open("access.log","r")
    loglines = follow(logfile)
    codes, urls = dict(), dict()
    myfile=open("stats.log", "a")
    for concat in loglines:

        for line in concat:
            # print("parsing "+line)

            parsedLine = line.split('"')
            url = parsedLine[1].split(" ")[1]
            status = parsedLine[2].split(" ")[1][0:2] + 'x'
            codes[status] = codes.get(status, 0) + 1
            if status[0:2] == '40':
                urls[url] = urls.get(url, 0) + 1

        print("saving")
        myfile.write("----------------------\n")
        for i in codes:
            myfile.write("%s:%s|s \n" % (i, codes[i]))
            print ("%s:%s|s "% ( i,codes[i]))

        for i in urls:
            myfile.write("%s:%s|s \n" % (i, urls[i]))
            print("%s:%s|s " % (i, urls[i]))

        myfile.flush()
        urls, codes = dict(),dict()



