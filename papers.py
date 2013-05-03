import urllib2 as url
import getopt,sys
import sqlite3
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c2 = conn.cursor()
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
    data["inspire_id"]=value
    data["bibtex"]=bibtex
    return data
    
def arxiv(a_id):
    pass

def add_keywords():
    inp="start"
    ret=[]
    while inp:
        ret.append(inp)
        inp=raw_input("Keyword:")
    return ret[1:]

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

def insert(data):
    record=(data["title"],data["authors"],data["inspire_id"],data["arxiv_id"],data["summary"],data["bibtex"])
    c.execute("INSERT INTO papers VALUES (Null,?,?,?,?,?,?)",record)
    conn.commit()
    paper_id=c.lastrowid
    keywords=[]
    for k in data["keywords"]:
        keywords.append((k,paper_id))
    c.executemany("INSERT INTO keywords VALUES (Null,?,?)",keywords)
    conn.commit()

def html(entry,keywords):
    h='<h2><a href="http://inspirehep.net/record/'+str(entry["inspire_id"])+'">'+entry["title"]+"</a></h2><h3>"+entry['authors']+"</h3><h4>"
    for k in keywords:
        h+=k+", "
    h+="</h4><p>"+entry["summary"]+"</p>"
    return h
def get_keywords(paper_id):
    keywords=[]
    for keyword in c2.execute('Select * from keywords where paper_id='+str(paper_id)):
        keywords.append(keyword["keyword"])
    return keywords


opts,args=getopt.getopt(sys.argv[1:],"ha:i:bd:");
data={}
if len(opts)>0:
    option,value=opts[0]
    if option=="-i":
        data=spires(value)
        cont=raw_input("Continue with paper with title "+data["title"]+":")
        if cont =="n":
            sys.exit(0)
        data["summary"]=raw_input("Summary:")
        data["keywords"]=add_keywords()
        data["arxiv_id"]=None
        insert(data)
    if option=="-a":
        data=arxiv(value)
    if option=="-b":# Write out a bibtex file of all the entries
        for row in c.execute('SELECT * FROM papers'):
            print row["bibtex"]
    if option=="-d": #Generate HTML output of all of the papers with the keyword value, if supplied

        if value=="all":
            print "<html><head><title>Papers</title></head><body>"
            for row in c.execute('SELECT * FROM papers'):
                paper_id=row[0]
                keywords=get_keywords(paper_id)
                print html(row,keywords)
            print "</body></html>"
        else:
            papers=[]
            for row in c2.execute('Select * from keywords where keyword="'+value+'"'):
                paper_id=row["paper_id"]
                if paper_id not in papers:
                    papers.append(paper_id)

            print "<html><head><title>Papers with keyword "+value+"</title></head><body><h1>Papers with keyword "+value+"</h1>"
            for p in papers:
                for row in c.execute('SELECT * FROM papers where id='+str(p)):
                    keywords=get_keywords(p)
                    print html(row,keywords)
            print "</body></html>"


            


        
else:
    data["title"]=raw_input("Title:")
    data["authors"]=raw_input("Authors:")
    data["summary"]=raw_input("Summary:")
    data["bibtex"]=raw_input("bibtex:")
    data["keywords"]=add_keywords()
    insert(data)
