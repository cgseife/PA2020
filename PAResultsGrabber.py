import json
import datetime
import requests

### MAIN BODY ###

endpoint = "https://www.electionreturns.pa.gov/api/ElectionReturn/GetCountyBreak?officeId=1&districtId=1&methodName=GetCountyBreak&electionid=undefined&electiontype=undefined&isactive=undefined"
params = {}

requestobj = requests.get(endpoint,params)
electionstring = requestobj.text

todaydate = datetime.datetime.now()
todaystring = todaydate.strftime("%Y%m%d")+"-" +todaydate.strftime("%H%M%S")
fileprefix = "PA.results."+todaystring
outfilename = fileprefix + ".json"
outfile = open(outfilename,"w")
print(electionstring,file=outfile)
outfile.close()

delimiter = "\t"
outfilename = fileprefix + ".tsv"
try:
    electionstrdict = json.loads(electionstring)
    electiondict = json.loads(electionstrdict) ## FOR SOME REASON, PA'S FILE IS A STRING -- STARTS WITH QUOTE MARKS. THIS ELIMINATES.
except:
    print("Whoops! Decode error")
    electiondict = {}
countydict = electiondict["Election"]["Statewide"][0]
headerlist = []
for header in countydict["ADAMS"][0].keys(): #Pull off headers from first entry
    headerlist.append(header)
headerstring = delimiter.join(headerlist)

outfile=open(outfilename,"w")
print(headerstring,file=outfile)
for county in countydict.keys():
    for itemdict in countydict[county]:
        datalist = []
        for header in headerlist:
            if header in itemdict.keys():
                datalist.append(itemdict[header])
            else:
                datalist.append("")
        datastring = delimiter.join(datalist)
        print(datastring,file=outfile)

outfile.close()
