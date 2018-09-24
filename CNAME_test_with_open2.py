from dns import resolver
import dns
import os
import string
import csv

errcountA = 0
errcountCNAME = 0
errcountCNAME2 = 0
errcountNS = 0
errcountSOA = 0
errcountSOA2 = 0

list = []
combolist = []

sublist1 = open ("c:/temp/sublist2.txt", "r").read().replace('\r', '').splitlines()

print "\r\n"
print "List of URLs to be Resolved: "
print "\r\n"
print sublist1
print "\r\n"
print "there are %d total URLs in this list" %len(sublist1)
print "\r\n"
print "URLs being processed:"

for url in sublist1:
    A = []
    CNAME = []
    SOA = []
    SOA2 = []
    print "read %s prior to Resolver" %url.split()
    
    try:
        answer = dns.resolver.query(url, 'A', raise_on_no_answer=True)
        for rdata in answer:
            print rdata
            A.append(rdata.address) #(rdata.address)
            print type(A[0])
            print A
            #time.sleep(1)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        A = "IPv4 not found"
        errcountA += 1
    
    try:
        answer = dns.resolver.query(url, 'CNAME')
        for rdata in answer:
            print rdata
            CNAME.append(rdata.target)
            CNAME = str(CNAME).lstrip("[<DNS name ").rstrip(".>]")
            print CNAME
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        CNAME = "no CNAME found"
        errcountCNAME += 1
    
    try:
     	answer = dns.resolver.query(url, 'SOA')
        for rdata in answer:
            print rdata
            SOA.append(rdata.mname)
            SO2.append(rdata.rname)
            print SOA, SOA2
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        SOA = "no SOA found"
        SOA2 = "no SOA found"
        errcountSOA2 += 1

    list = [url, A, CNAME, SOA, SOA2]
    combolist.append(list)
    print "read %s after Resolver" %url
                
with open("c:/temp/subsresolvedtest.csv", 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for r in combolist:
        writer.writerow(r)

print "\r\n"
print "printing CNAME list:"
print "\r\n"
print CNAME
print "\r\n"
print "URLs Resolved:"
print "\r\n"
print combolist
print "\r\n"
print ("There were %d 'A' record errors") %errcountA
print "\r\n"
print ("There were %d CNAME record errors") %errcountCNAME
print "\r\n"
print ("There were %d nested SOA record errors") %errcountSOA
print "\r\n"
print ("Done")
