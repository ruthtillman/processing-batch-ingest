import json, glob, os, shutil
from jq import jq

# Makes necessary JOB file in order to run the thumbnails update. Prints success message.

def makeJOBFile():
    jobString = '{ "Todo": ["validate","ingest","index"], "Finished": [] }'
    jobContent = json.loads(jobString)
    with open("JOB", 'w') as outfile:
        json.dump(jobContent, outfile, indent=4)
    print "JOB file created."

# Copy ROFs from the batch ingest success location and renames them as "original-metadata-n.rof". Prints success message.

def copyROFs(remoteDirectory,workingDirectory):
    os.chdir(remoteDirectory)
    originalROF = glob.glob("*rof")
    for original in originalROF:
        newPathName = workingDirectory + "/original-" + original
        shutil.copy(original, newPathName)
    print "Original ROFs retrieved from batch ingester."

# Copies the original submission CSVs to the directory "originals" and renames them "original-metadata-n.csv" to reflect what they are. Prints success message.

def copyAndRenameOriginalCSVs(workingDirectory,originals):
    os.chdir(workingDirectory)
    originalCSVs = glob.glob("*.csv")
    for csv in originalCSVs:
        backupCSV = originals + "/original-" + csv
        shutil.copy(csv, backupCSV)
    print "CSVs backed up to originals directory."

# Creates originals directory (if not exists), retrieves ROFs from remove server (but not into originals directory yet), runs the CSV copy/rename.

def fileCopyAndManipulation(remoteDirectory,workingDirectory):
    originals = workingDirectory + "/originals"
    if not os.path.exists(originals):
        os.makedirs(originals)
    copyROFs(remoteDirectory,workingDirectory)
    copyAndRenameOriginalCSVs(workingDirectory,originals)

# Uses JQ. Parses the ROF files to get PIDS and passes to CSV writing and parses the ROF file to get thumbnail/properties and passes to ROF writing.

def parseData(workingDirectory):
    os.chdir(workingDirectory)
    rofFiles = glob.glob("*.rof")
    for rof in rofFiles:
        updateRof = rof.replace("original-","")
        with open(rof) as successFile:
            metadata = json.load(successFile)
        PIDArray = jq('.[] | select(.["af-model"] != "GenericFile") |.pid?, .metadata["dc:title"]').transform(metadata, multiple_output=True)
        writePIDUpdateFile(PIDArray,rof)
        updateThumbs = jq('.[]|select(.["af-model"] != "GenericFile")|{type,pid,properties,"properties-meta"}').transform(metadata, multiple_output=True)
        writeROFUpdateFile(updateThumbs,updateRof,rof)

# Writes the JQ-extracted PID array into "pid-n.csv" and prints success message.

def writePIDUpdateFile(PIDArray,rof):
    fileNum = rof.replace(".rof","").replace("original-metadata","")
    outputFile = "pid" + fileNum + ".csv"
    f = open(outputFile, 'w')
    f.write('curate_id,dc:title\n')
    while PIDArray != []:
      varPID = '"' + str(PIDArray.pop(0)) + '"'
      varTitle = '"' + str(PIDArray.pop(0)) + '"'
      row = varPID + ',' + varTitle + '\n'
      f.write(row)
    f.close()
    print outputFile + " created."

# Writes the JQ extracted properties information into "metadata-n.rof" and prints success message.

def writeROFUpdateFile(updateThumbs, updateRof,rof):
    with open(updateRof, 'w') as outfile:
        json.dump(updateThumbs, outfile, indent=4)
    print updateRof + " created."

# Shuffles around the ROF files. First moves the "original-metadata-n.rof" files into the "originals" directory now that the work's been done on them. Then moves the new "metadata-n.rof" files into the "update-thumbnails" directory.

def cleanupROFs(workingDirectory):
    originals = workingDirectory + "/originals"
    originalROFs = glob.glob("original*.rof")
    for originalROF in originalROFs:
        shutil.move(originalROF, originals)
    print "Original ROFs moved to folder 'originals.'"
    thumbs = workingDirectory + "/update-thumbnails"
    if not os.path.exists(thumbs):
        os.makedirs(thumbs)
    thumbnailROFs = glob.glob("*.rof")
    for thumbnailROF in thumbnailROFs:
        shutil.move(thumbnailROF, thumbs)
    print "Thumbnail update ROFs moved to folder 'update-thumbnails.'"

# Gets the inputs and runs the main processes.

def inputAndRun():
    workingDirectory = raw_input("The path to the local working directory: ")
    remoteDirectory = raw_input("The path to the batch ingest directory: ")
    fileCopyAndManipulation(remoteDirectory,workingDirectory)
    parseData(workingDirectory)
    cleanupROFs(workingDirectory)
    makeJOBFile()

#Run the Program

inputAndRun()
