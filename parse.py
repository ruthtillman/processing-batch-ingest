import json, glob, os
from jq import jq

def parseData(theDirectory):
    os.chdir(theDirectory)
    rofFiles = glob.glob("*.rof")
    for rof in rofFiles:
        updateRof = "update-" + rof
        with open(rof) as successFile:
            metadata = json.load(successFile)
        PIDArray = jq('.[] | select(.["af-model"] != "GenericFile") |.pid?').transform(metadata, multiple_output=True)
        writePIDUpdateFile(PIDArray,rof)
        updateThumbs = jq('.[]|select(.["af-model"] != "GenericFile")|{type,"af-model",pid,properties,"properties-meta"}').transform(metadata, multiple_output=True)
        writeROFUpdateFile(updateThumbs, updateRof,rof)

def writePIDUpdateFile(PIDArray,rof):
    fileNum = rof.replace(".rof","").replace("metadata","")
    outputFile = "pid" + fileNum + ".csv"
    f = open(outputFile, 'w')
    f.write('curate_id\n')
    while PIDArray != []:
        for PID in PIDArray:
            row = PID + '\n'
            f.write(row)
            PIDArray.pop(0)
    f.close()
    print outputFile + " created."

def writeROFUpdateFile(updateThumbs, updateRof,rof):
    with open(updateRof, 'w') as outfile:
        json.dump(updateThumbs, outfile, indent=4)
    print updateThumbs + "created."

def takeInputs():
    theDirectory = raw_input("The path to the directory where the files are stored: ")
    parseData(theDirectory)

takeInputs()
