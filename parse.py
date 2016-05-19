import json
from jq import jq

def parseData():
    theFile = raw_input("Ingest file name if in current directory or full filepath and filename: ")
    with open(theFile) as successfulIngest:
      metadata = json.load(successfulIngest)
    pidTitle = jq('.[] | select(.["af-model"] != "GenericFile") |.pid?, .metadata["dc:title"]').transform(metadata, multiple_output=True)
    writeFile(pidTitle)

def writeFile(pidTitle):
    outputFile = raw_input("File name: ")
    f = open(outputFile, 'w')
    f.write('PID,Title\n')
    while pidTitle != []:
      PID = '"' + pidTitle.pop(0) + '"'
      title = '"' + pidTitle.pop(0) + '"'
      row = PID + ',' + title + '\n'
      f.write(row)

    f.close()

parseData()
