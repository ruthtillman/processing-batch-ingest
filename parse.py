import json, glob, os, shutil
from jq import jq

# Things to add:
# Take success directory and copy all .rof files to working directory
# Auto-rename all .rof and (make a backup/renamed copy of) .csv files before this starts.
# make originals folder for copies and move files there when appropriate.
# write JOB file

def copyROFs(remoteDirectory,workingDirectory):
    os.chdir(remoteDirectory)
    originalROF = glob.glob("*rof")
    for original in originalROF:
        newPathName = workingDirectory + "/original-" + original
        shutil.copy(original, newPathName)
    print "Original ROFs retrieved from batch ingester."

def copyAndRenameOriginalCSVs(workingDirectory,originals):
    os.chdir(workingDirectory)
    originalCSVs = glob.glob("*.csv")
    for csv in originalCSVs:
        backupCSV = originals + "/original-" + csv
        shutil.copy(csv, backupCSV)
    print "CSVs backed up to originals directory."

def fileCopyAndManipulation(remoteDirectory,workingDirectory):
    originals = workingDirectory + "/originals"
    if not os.path.exists(originals):
        os.makedirs(originals)
    copyROFs(remoteDirectory,workingDirectory)
    copyAndRenameOriginalCSVs(workingDirectory,originals)

def parseData(workingDirectory):
    os.chdir(workingDirectory)
    rofFiles = glob.glob("*.rof")
    for rof in rofFiles:
        updateRof = rof.replace("original-","")
        with open(rof) as successFile:
            metadata = json.load(successFile)
        PIDArray = jq('.[] | select(.["af-model"] != "GenericFile") |.pid?').transform(metadata, multiple_output=True)
        writePIDUpdateFile(PIDArray,rof)
        updateThumbs = jq('.[]|select(.["af-model"] != "GenericFile")|{type,"af-model",pid,properties,"properties-meta"}').transform(metadata, multiple_output=True)
        writeROFUpdateFile(updateThumbs, updateRof,rof)

def writePIDUpdateFile(PIDArray,rof):
    fileNum = rof.replace(".rof","").replace("original-metadata","")
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
    print updateRof + " created."

def cleanupROFOriginals(workingDirectory):
    originals = workingDirectory + "/originals"
    originalROFs = glob.glob("original*.rof")
    for originalROF in originalROFs:
        shutil.move(originalROF, originals)
    print "Original ROFs moved to folder 'originals.'"

def inputAndRun():
    workingDirectory = raw_input("The path to the local working directory: ")
    remoteDirectory = raw_input("The path to the batch ingest directory: ")
    fileCopyAndManipulation(remoteDirectory,workingDirectory)
    parseData(workingDirectory)
    cleanupROFOriginals(workingDirectory)

inputAndRun()
