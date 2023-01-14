import glob, os
import wfdb
def fileattr(fileName):
    try:
        allFilePath = glob.glob("./project/models/data/"+fileName+".dat")
        global nameFile
        nameFile = fileName
        allFilePath = [os.path.splitext(path)[0] for path in allFilePath]
    except BaseException as e:
        return e
    return allFilePath

def getRaw():
    allFilePath = fileattr(nameFile)
    try:
        for i, dta in enumerate(allFilePath):
            rec = wfdb.rdrecord(dta, channels=[1])
            arrSignal = rec.p_signal[:, 0]
            arrLabel = rec.comments[4][22:]
    except BaseException as e:
        return e
    return arrSignal, arrLabel