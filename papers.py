import urllib2 as url
import getopt,sys
import sqllite
def spires(s_id):
    response = url.urlopen('http://inspirehep.net/record/'+s_id+'/export/hx')
    bib=False
    bibtex=""
    for line in response:
        if line.find("</pre>")==0:
            break;
        if bib:
            bibtex+=line
        if line.find("<pre>")==0:
            bib=True
    bibtex_dict=extract_bibtex(bibtex)
    data["title"]=bibtex_dict["title"]
    data["authors"]=bibtex_dict["author"]
    data["spires_id"]=value
    data["bibtex"]=bibtex
    return data
    
def arxiv(a_id):
    pass


def extract_bibtex(bibtex):
    d={}
    lines=bibtex.split("\n")
    d["key"]=lines[0].split("{")[1].split(",")[0]
    b=" ".join(lines[1:])
    b=""
    for l in lines[1:]:
        b+=" "+l.strip()
    entries=b.split('"')
    for e in entries[:-1]:
        e=e.strip(",")
        if e.find("=")>0 and e.find("%%CITATION")<0:
            key=e.split()[0]
        else:
            d[key]=e
    d["title"]=d["title"][1:-1]
    return d


opts,args=getopt.getopt(sys.argv[1:],"ha:s:");
data={}
if len(opts)>0:
    option,value=opts[0]
    if option=="-s":
        data=spires(value)
        data["summary"]=raw_input("Summary:")
    if option=="-a":
        data=arxiv(value)
else:
    data["title"]=raw_input("Title:")
    data["authors"]=raw_input("Authors:")
    data["summary"]=raw_input("Summary:")
    data["bibtex"]=raw_input("bibtex:")

print data