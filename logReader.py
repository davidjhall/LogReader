#  logReader.py
#       reads a specific nginx formatted log file every 5 seconds and writes status codes to stats.log file
#

# imports
import time

# variables
#  Using simple debug flag (for now)  instead of loglevels
debug = True
sleepTime = 5

#  Original spec calls for /var/log -- swap out these lines to run locally
path = '/var/log/'
#  path = './'

nginxFile = path+'nginx/access.log'
outputFile = path+'stats.log'

#  follow ( thefile)
#       function, borrowed from http://www.dabeaz.com/generators/ to tail the end of a log file
#       Uses yield to give up each change to log file after scrolling to end
#       Modified to collect all changes done during sleep peiod and then give up at once in concat
def follow(thefile):
    concat = list()
    thefile.seek(0,2)
    while True:
        concat[:] = []  # Empty the list
        line = thefile.readline()
        if not line:
            if debug:
                print("sleeping")
            time.sleep(sleepTime)
            continue
        while (line):
            concat.append(line)
            line = thefile.readline()
        yield concat


if __name__ == '__main__':
    logfile = open(nginxFile,"r")
    loglines = follow(logfile)
    statsfile=open(outputFile, "a")
    for concat in loglines:
        urls, codes = dict(),dict()  # empty the lists
        for line in concat:
            # Parsing out the lines
            #   This version 'cheats' in that it only looks for status codes and the url ( by parsing on " )
            #   A correct version would parse out each of the nginx elements, but I did this way for speed/solve, not long-term use
            parsedLine = line.split('"')
            #  First quoted element is the URL string
            url = parsedLine[1].split(" ")[1]
            #  status code is first integer following  it
            #  we are only interested in first 2 characters of status code, so it's string[0:2] + 'x'
            status = parsedLine[2].split(" ")[1][0:2] + 'x'
            codes[status] = codes.get(status, 0) + 1
            #  if status code is fail, save it in separate dictionary
            #    ( original version incoorrectly had 40x for testing because test file didn't have robust 50x codes)
            if status[0:2] == '50':
                urls[url] = urls.get(url, 0) + 1

        # write to output file
        # If windows, file will be 0 bytes before program finish, but a 'type stats.log' will show output
        if debug:
            print("saving")
        statsfile.write("----------------------\n")

        for i in codes:
            statsfile.write("%s:%s|s \n" % (i, codes[i]))
            if debug:
                print ("%s:%s|s "% ( i,codes[i]))
        for i in urls:
            statsfile.write("%s:%s|s \n" % (i, urls[i]))
            if debug:
                print("%s:%s|s " % (i, urls[i]))

        statsfile.flush()
