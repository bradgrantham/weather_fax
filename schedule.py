import urllib2
import bisect
import time

# http://tgftp.nws.noaa.gov/fax/hfreyes.txt

stations = [
    ["New Orleans, LA", "http://tgftp.nws.noaa.gov/fax/hfgulf.txt"],
    ["Pt. Reyes, CA", "http://tgftp.nws.noaa.gov/fax/hfreyes.txt"],
    ["Honolulu, HI", "http://tgftp.nws.noaa.gov/fax/hfhi.txt"],
    ["Kodiak, AK", "http://tgftp.nws.noaa.gov/fax/hfak.txt"],
    ["Boston, Massachusetts", "http://tgftp.nws.noaa.gov/fax/hfmarsh.txt"],
]

for (name, url) in stations:
    stream = urllib2.urlopen(url)
    content = stream.read()

    lines = content.split("\r\n")

    last_time = 0
    last_title = ""
    schedule = []
    for l in lines:
        if len(l) >= 5 and l[4] == "/":
            start1 = l[0:4]
            start2 = l[5:9]
            title = l[11:50]
            if start1 != "----":
                t = int(start1[0:2]) * 100 + int(start1[2:4])
                schedule.append((t, title))
                if t > last_time:
                    (last_time, last_title) = (t, title)
            if start2 != "----":
                t = int(start2[0:2]) * 100 + int(start2[2:4])
                schedule.append((t, title))
                if t > last_time:
                    (last_time, last_title) = (t, title)

    schedule.append((0, last_title))

    schedule.sort(key = lambda e : e[0])

    gmt = time.gmtime()

    now = gmt[3] * 100 + gmt[4]
    which = bisect.bisect_left([t for (t, title) in schedule], now)
    print "%s:" % name
    print "    current : %s started at %d" % (schedule[which - 1][1], schedule[which - 1][0])
    print "    next    : %s starting at %d" % (schedule[which][1], schedule[which][0])

# for start, title in schedule:
        # print start, title

