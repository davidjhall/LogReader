
with open("access.log", "r") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content]
codes,urls = dict(),dict()

for line in content:
    parsedLine = line.split('"')
    url = parsedLine[1].split(" ")[1]
    status=parsedLine[2].split(" ")[1][0:2] +'x'
    codes[status] = codes.get(status,0)+1
    if status[0:2]=='40':
        urls[url] =urls.get(url,0)+1
with open("stats.log", "a") as myfile:
    myfile.write("----------------------\n")
    for i in codes:
        myfile.write("%s:%s|s \n"% ( i,codes[i]))
        # print ("%s:%s|s "% ( i,codes[i]))
    for i in urls:
        myfile.write("%s:%s|s \n" % (i, urls[i]))
        # print("%s:%s|s " % (i, urls[i]))
