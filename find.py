from datetime import datetime

def toDate(time):
    y1,m1,d1 = map(int, time.split('-'))
    start = datetime(y1, m1, d1)
    return start

def findNeighbors(homecity, funcitys, startTime, endTime):
    lines = open("queries.txt").read().split("\n")
    found = []
    for line in lines:
        if not line:
            continue
        print line.split("\t")

        uid,uname,hcity,fcitys,stime,etime = line.split("\t")
        fcitys = fcitys.split(" ")
        if hcity == homecity:
            n_common = len(set(funcitys).intersection(fcitys))
            score = n_common / float(len(funcitys)+len(fcitys))
            if score >= 0.5:
                sdelta = abs((toDate(startTime) - toDate(stime)).days)
                edelta = abs((toDate(endTime) - toDate(etime)).days)
                if sdelta < 4 and edelta < 4:
                    rstring = "%s %s %s %s %s %s" % (uname, hcity, " ".join(fcitys), stime, etime, "%s@gmail.com" % uname)
                    found.append(rstring)
    if not found:
        found.append("Sorry, you will be alone :-(")
    return "\n".join(found)


if __name__ == "__main__":
    print findNeighbors("Helsinki", ["Munich", "Milan", "Berlin"], "2015-12-01","2015-12-07")
    print findNeighbors("Helsinki", ["Barcelona", "Berlin", "Paris"], "2015-12-01","2015-12-15")
