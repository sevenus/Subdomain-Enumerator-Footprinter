from dns import resolver
import dns
import os
import string
import csv
import urllib2

errcountA = 0
errcountCNAME = 0
errcountCNAME2 = 0
errcountWHOIS1 = 0
errcountWHOIS2 = 0
errcountSOA = 0
errcountSOA2 = 0

list1 = []
combolist = []

sublist1 = open ("c:/temp/sublist.txt", "r").read().replace('\r', '').splitlines()

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
    WHOIS = []
    CNAME = []
    CNAME2 = []
    SOA = []
    SOA2 = []
    WHOIS1 = []
    WHOIS2 = []
    print "read %s prior to Resolver" %url.split()
    
    try:
        answer = dns.resolver.query(url, 'A', raise_on_no_answer=True)
        for rdata in answer:
            print rdata
            A.append(rdata.address) #(rdata.address)
            print A
            print "first A record only:"
            print A[0]
        response = urllib2.urlopen("https://www.port43whois.com/whois.php?domain="+A[0])
        for records in response:
            WHOIS.append(records)
     except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        A = "IPv4 not found"
        WHOIS1 = "NetName not found"
        WHOIS2 = "Org info not found"
        errcountA += 1
        errcountWHOIS1 += 1
        errcountWHOIS2 += 1
    
    try:
        answer = dns.resolver.query(url, 'CNAME')
        for rdata in answer:
            print rdata
            CNAME.append(rdata.target)
            CNAME = str(CNAME).lstrip("[<DNS name ").rstrip(".>]")
            print CNAME
        answer = dns.resolver.query(CNAME, 'CNAME')
        for rdata in answer:
            print rdata
            CNAME2.append(rdata.target)
            CNAME2 = str(CNAME2).lstrip("[<DNS name ").rstrip(".>]")
            print CNAME2
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        CNAME = "no CNAME found"
        CNAME2 = "no nested CNAME"
        errcountCNAME += 1
        errcountCNAME2 += 1
    
    try:
     	answer = dns.resolver.query(url, 'SOA')
        for rdata in answer:
            print rdata
            SOA.append(rdata.mname)
            SOA2.append(rdata.rname)
            print SOA, SOA2
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        SOA = "no SOA found"
        SOA2 = "no SOA found"
        errcountSOA += 1
        errcountSOA2 += 1
    try:
        print "printing WHOIS1: %s" %WHOIS[18]
        print "printing WHOIS2: %s" %WHOIS[27:32] + WHOIS[45]
        WHOIS1 = str(WHOIS[18])
        WHOIS2 = str(WHOIS[27:32]) + str(WHOIS[45])
    except:
        print "no data to concatenate"
    
    list1 = [url, str(A).replace("u", ""), CNAME, CNAME2, WHOIS1.rstrip("\n"), WHOIS2.rstrip("\n"), SOA, SOA2]
    combolist.append(list1)
    print "read %s after Resolver" %url

    #print "printing WHOIS %s" %WHOIS

                
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
print ("There were %d CNAME2 record errors") %errcountCNAME2
print "\r\n"
print ("There were %d nested SOA record errors") %errcountSOA
print "\r\n"
print ("Done")
'''print combolist[0][2]
print combolist[1][2]
print combolist[2][2]'''
print "\r\n"
print "\r\n"

#time.sleep(1)
