import urllib2
import bisect
import time

# http://tgftp.nws.noaa.gov/fax/hfreyes.txt

sched = """0140/1400  TEST PATTERN                            120/576
0143/1403  NE PACIFIC GOES IR SATELLITE IMAGE      120/576      00/12      6 
0154/1414  PACIFIC GOES IR SATELLITE IMAGE         120/576      00/12      5 
0205/1425  TROPICAL SEA STATE ANALYSIS             120/576      00/12      4 
0215/1435  TROPICAL 48HR SURFACE FORECAST          120/576      12/00      4 
0225/----  TROPICAL 48HR WIND/WAVE FORECAST        120/576      1200       4 
0235/----  TROPICAL 72HR WIND/WAVE FORECAST        120/576      1200       4 
0245/1445  500MB ANALYSIS                          120/576      00/12      1 
0255/1455  SEA STATE ANALYSIS, WIND/WAVE ANALYSIS  120/576      00/12    1/8 
0305/1505  PRELIM SURFACE ANALYSIS(PART 1 NE PAC)  120/576      00/12      2 
0318/1518  PRELIM SURFACE ANALYSIS(PART 2 NW PAC)  120/576      00/12      3 
0331/1531  FINAL  SURFACE ANALYSIS(PART 1 NE PAC)  120/576      00/12      2 
0344/1544  FINAL  SURFACE ANALYSIS(PART 2 NW PAC)  120/576      00/12      3 
0357/1557  CYCLONE DANGER AREA* or HIGH WIND/WAVES 120/576      03/15     10 
0408/1608  TROPICAL SURFACE ANALYSIS               120/576      00/12      4 
0655/1840  TEST PATTERN 
0657/----  2033Z  REBROADCAST (96HR 500MB)         120/576      1200       1 
0707/----  2043Z  REBROADCAST (96HR SURFACE)       120/576      1200       1 
0717/----  2053Z  REBROADCAST (96HR WIND/WAVE)     120/576      1200       1 
0727/----  2103Z  REBROADCAST (96HR WAVE PERIOD)   120/576      1200       1 
----/1842  SST ANALYSIS                            120/576      LATEST     9
----/1852  SST ANALYSIS                            120/576      LATEST     6  
0737/1902  TROPICAL GOES IR SATELLITE IMAGE        120/576      06/18      7 
0748/1913  WIND/WAVE ANALYSIS                      120/576      06/18      8 
0758/1923  24HR 500MB FORECAST                     120/576      00/12      1 
0808/1933  24HR SURFACE FORECAST                   120/576      00/12      8 
0818/1943  24HR WIND/WAVE FORECAST                 120/576      00/12      8 
0828/1953  48HR 500MB FORECAST                     120/576      00/12      1 
0838/2003  48HR SURFACE FORECAST                   120/576      00/12      1 
0848/2013  48HR WIND/WAVE FORECAST                 120/576      00/12      1 
0858/2023  48HR WAVE PERIOD/SWELL DIRECTION        120/576      00/12      1 
----/2033  96HR 500MB FORECAST                     120/576      1200       1 
----/2043  96HR SURFACE FORECAST                   120/576      1200       1 
----/2053  96HR WIND/WAVE FORECAST                 120/576      1200       1 
----/2103  96HR WAVE PERIOD/SWELL DIRECTION        120/576      1200       1 
0908/2113  PACIFIC GOES IR SATELLITE IMAGE         120/576      06/18      5 
0919/2124  SURFACE ANALYSIS (PART 1 NE PACIFIC)    120/576      06/18      2 
0932/2137  SURFACE ANALYSIS (PART 2 NW PACIFIC)    120/576      06/18      3 
0945/2150  TROPICAL SURFACE ANALYSIS               120/576      06/18      4 
0959/2204  TROPICAL 24HR WIND/WAVE FORECAST        120/576      00/12      4 
1009/2214  CYCLONE DANGER AREA* or HIGH WIND/WAVES 120/576      09/21     10 
1120/2320  TEST PATTERN                            120/576
1124/2324  BROADCAST SCHEDULE (PART 1)             120/576
1135/2335  BROADCAST SCHEDULE (PART 2)             120/576
1146/----  REQUEST FOR COMMENTS                    120/576
1157/----  PRODUCT NOTICE BULLETIN                 120/576
1208/----  TROPICAL 48HR WIND/WAVE FORECAST        120/576      0000       4 
1218/----  TROPICAL 72HR WIND/WAVE FORECAST        120/576      0000       4 
1228/2346  TROPICAL 48HR WAVE PERIOD/SWELL DIR     120/576      00/12      4 
----/2356  TROPICAL 72HR WAVE PERIOD/SWELL DIR     120/576      0000       4"""

stations = [
    ["New Orleans, LA", "http://tgftp.nws.noaa.gov/fax/hfgulf.txt"],
    ["Pt. Reyes, CA", "http://tgftp.nws.noaa.gov/fax/hfreyes.txt"],
    ["Honolulu, HI", "http://tgftp.nws.noaa.gov/fax/hfhi.txt"],
    ["Kodiak, AK", "http://tgftp.nws.noaa.gov/fax/hfak.txt"],
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

