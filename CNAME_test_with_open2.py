from dns import resolver
import dns
import os
import csv
errcountA = 0
errcountCNAME = 0
errcountCNAME2 = 0
list = []
combolist = []
with open ("c:/temp/sublist.txt") as sublist:
    for url in sublist:
        A = []
        CNAME = []
        CNAME2 = []
        url = url.strip()
        try:
            answer = resolver.query(url, 'A')
            for rdata in answer:
                A.append(rdata.address)
        except:
            A = "no IPV4 found"
            errcountA += 1
            continue
        try:
            answer = resolver.query(url, 'CNAME')
            for rdata in answer:
                CNAME.append(rdata.target)
        except:
            CNAME = "no CNAME found"
            errcountCNAME += 1
            continue
        try:
        	answer = resolver.query(CNAME, 'CNAME')
        	for rdata in answer:
        		CNAME2.append(rdata.target)
        except:
        	CNAME2 = "no nested CNAMEs"
        	errcountCNAME2 += 1
            continue
        finally:
            list = [url, A, CNAME, CNAME2]
            #list = zip(url,A,CNAME)
            combolist.append(list)

with open("c:/temp/subsresolvedtest.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for r in combolist:
        writer.writerow(r)
print "\r\n"
print A
print "\r\n"
print CNAME
print "\r\n"
print url
print "\r\n"
print list
print "\r\n"
print combolist
print "\r\n"
print ("There were %d A record errors") %errcountA
print ("There were %d CNAME record errors") %errcountCNAME
print "\r\n"
print ("%d CNAME records are not nested") %errcountCNAME2
print "\r\n"
print ("Done")



