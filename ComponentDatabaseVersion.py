
import random
from jinja2 import Markup

#import os
#from sys import path as sysPath

#sysPath.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cyanoConstruct import NamedSequenceDB, SpacerDataDB, PrimerDataDB


def checkType(elemType, typeName):
    if(type(typeName) != str):
        raise TypeError("typeName not a string")
        
    if(type(elemType) != str):
        raise TypeError(typeName + " not a string")
    if(elemType not in ["Pr", "RBS", "GOI", "Term"]):
        raise ValueError(typeName + " not valid")

#okay! restructure this so that it's entirely wrapper stuff
#the ONLY thing the NamedSequence and Component will store are id numbers
#and it will NOT add anything to the database, it will simply, spit out the information needed to pass to the database

#should it clear its data once it's in the database? I don't know


class NamedSequence:
    #why is this here
    #typeShortToLong = {AllowedTypes.PR: "promoter", AllowedTypes.RBS: "ribosome binding site", AllowedTypes.GOI: "gene of interest", AllowedTypes.TERM: "terminator"}

    #all the many initialization methods
    
    def __init__(self):
        pass
    
    @classmethod
    def makeNew(cls, NStype, NSname, NSseq, nameID):
        #type checking
        checkType(NStype, "NStype")

        if(type(NSname) != str):
            raise TypeError("NSmame not a string")
        if(type(NSseq) != str):
            raise TypeError("NSseq not a string")
        if(type(nameID) != int):
            raise TypeError("newID not an int")
                
        newNS = cls()
        
        newNS.__type = NStype
        newNS.__name = NSname
        newNS.__seq = NSseq
        newNS.__nameID = nameID
        
        newNS.__inDatabase = False
        
        return newNS

    @classmethod
    def loadEntry(cls, newID):
        if(type(newID) != int):
            raise TypeError("NamedSequence newID not an int")
            
        newNS = cls()    
        
        #uhhhh
        newNS.__DBid = newID
        newNS.__inDatabase = True
        
        return newNS
                
    def setDBid(self, newID):
        if(type(newID) != int):
            raise TypeError("NamedSequence newID not an int")
            
        self.__DBid = newID
        self.__inDatabase = True
        
    #other stuff
        
    def __str__(self):
        return ("Named Sequence.\nType: " + self.getType() + "\nName: " + self.getName() + 
                "\nName ID: " + str(self.getNameID()) + "\nSequence:\n" + self.getSeq())
        
    #getters
    def getDBid(self):
        if(self.getInDatabase):
            return self.__DBid
        else:
            return -1 #I don't know what it should do here, actually
    
    def getInDatabase(self):
        return self.__inDatabase
    
    def getEntry(self):
        if(self.getInDatabase()):
            return NamedSequenceDB.query.get(self.getDBID())
        else:
            raise Exception("Not in database")
    
    def getType(self):
        if(self.getInDatabase()):
            return NamedSequenceDB.query.get(self.getDBID()).getType()
        else:
            return self.__type
        
    def getName(self):
        if(self.getInDatabase()):
            return NamedSequenceDB.query.get(self.getDBID()).getName()
        else:
            return self.__name
    
    def getSeq(self):
        if(self.getInDatabase()):
            return NamedSequenceDB.query.get(self.getDBID()).getSeq()
        else:
            return self.__seq
    
    def getNameID(self):
        if(self.getInDatabase()):
            return NamedSequenceDB.query.get(self.getDBID()).getNameID()
        else:
            return self.__nameID

class SpacerData:
    start = "GAAGAC" #enzyme recog. site?
    end = "GTCTTC"

    #spacers for elements 0 and T
    spacer0L = "AGGA"
    spacer0R = "AAAA"
    spacerTL = "ACTC"
    spacerTR = "TACA"
    
    #spacers, from highest allowed fidelity to lowest    
    spacers985 = [spacer0L, spacer0R]
    spacers981 = ["TAGA","GATA","ATTA"]
    spacers958 = ["CTAA", "TGAA", "CCAG", "CGGA", "CATA"]
    spacers917 = ["GGAA", "GCCA", "CACG", "CTTC", "TCAA", "ACTG", "AAGC", "GACC", "ATCG", "AGAG", "AGCA", "TGAA", "GTGA", "ACGA", "ATAC", "CAAG", "AAGG"]

    spacers = spacers985 + spacers981  + spacers958 + spacers917

    #max position for an element for a given fidelity
    max985 = 0
    max981 = len(spacers981)
    max958 = max981 + len(spacers958)
    max917 = max958 + len(spacers917) + 1

    @staticmethod
    def getMaxPosition():
        return len(SpacerData.spacers) - 1

    def __init__(self):
        self.__inDatabase = False
        return

    @classmethod
    def makeNew(cls, position, isTerminal):
        #type checking
        if(type(position) != int):
            raise TypeError("position is not an int")
        if(type(isTerminal) != bool):
            raise TypeError("isTerminal is not a boolean")

        newSpacerData = cls()

        if(position == 999): #special position for terminator
            newSpacerData.__spacerLeft = SpacerData.spacerTL
            newSpacerData.__spacerRight = SpacerData.spacerTR
            
            newSpacerData.__isTerminal = False #idk
            newSpacerData.__terminalLetter = "T" #I. don't know what to put here

        #validation
        elif(position < 0 or position > SpacerData.getMaxPosition()):
            raise ValueError("Position out of bounds. (0-" + str(SpacerData.getMaxPosition()) + ")")
        
        elif(position == SpacerData.getMaxPosition() and not isTerminal):
            raise Exception("Position " + position + " must be terminal.")
        
        #most kinds of things
        else:
            #left
            newSpacerData.__spacerLeft = SpacerData.spacers[position]
            
            #right
            if(isTerminal):
                newSpacerData.__spacerRight = SpacerData.spacerTL
                newSpacerData.__isTerminal = True
                newSpacerData.__terminalLetter = "L" #L for last I suppose
                
            else:
                newSpacerData.__spacerRight = SpacerData.spacers[position + 1]
                newSpacerData.__isTerminal = False
                newSpacerData.__terminalLetter = "M"
        
            if(position == 0):
                newSpacerData.__terminalLetter = "S" #to indicate it's the start

        newSpacerData.__position = position
        
        #set the NN on each side
        newSpacerData.setNN()
        newSpacerData.setFullSpacerSeqs()
        
        newSpacerData.__inDatabase = False
        
        return newSpacerData

    @classmethod
    def loadEntry(cls, newID):
        if(type(newID) != int):
            raise TypeError("newID not an int")
            
        newSpacerData = cls()
            
        newSpacerData.__DBid = newID
        newSpacerData.__inDatabase = True
        
        return newSpacerData
        
    def setDBid(self, newID):
        if(type(newID) != int):
            raise TypeError("newID not an int")
            
        self.__DBid = newID
        self.__inDatabase = True

    def setFullSpacerSeqs(self):
        self.__fullSeqLeft = self.getSpacerLeft() + self.getLeftNN() + SpacerData.start
        self.__fullSeqRight = SpacerData.end + self.getRightNN() +  self.getSpacerRight() #actually, I don't know if it's that simple or if complementary bases need to be found

    def setNN(self):
        #technically, T is allowed in certain circumstances, but that would require passing in
        #the element type, which would be a pain
        self.__leftNN = random.choice(["A", "G", "C"]) + random.choice(["A", "G", "C"])
        self.__rightNN = random.choice(["A", "G", "C"]) + random.choice(["A", "G", "C"])

    #complicated getters
    def __str__(self):
        retStr = "Spacers for position " + str(self.getPosition())
        if(self.getIsTerminal()):
            retStr += " is terminal"
        else:
            retStr += " is not terminal"
            
        retStr += "\nLeft:\n" + self.getSpacerLeft()
        retStr += "\nRight:\n" + self.getSpacerRight()
        retStr += "\nTerminal Letter: " + self.getTerminalLetter()
        return retStr

    #basic getters
    def getInDatabase(self):
        return self.__inDatabase
        
    def getID(self):
        return self.__DBid
    
    def getPosition(self):
        if(self.getInDatabase()):   #query the database if it's in
            return SpacerDataDB.query.get(self.getID()).getPosition()
        else:                       #the instance directly otherwise
            return self.__position 

    def getSpacerLeft(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getSpacerLeft()
        else:
            return self.__spacerLeft
    
    def getSpacerRight(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getSpacerRight()
        else:
            return self.__spacerRight
    
    def getIsTerminal(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getIsTerminal()
        else:
            return self.__isTerminal
    
    def getTerminalLetter(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getTerminalLetter()
        else:
            return self.__terminalLetter

    def getLeftNN(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getLeftNN()
        else:
            return self.__leftNN
    
    def getRightNN(self):
        if(self.getInDatabase()):
            return SpacerDataDB.query.get(self.getID()).getRightNN()
        else:
            return self.__rightNN

    def getFullSeqLeft(self):
        return self.getSpacerLeft() + self.getLeftNN() + SpacerData.start

    def getFullSeqRight(self):
        return SpacerData.end + self.getRightNN() + self.getSpacerRight() #except the complementary probably


class PrimerData:
    def __init__(self):
        self.__inDatabase = False
    
    @classmethod
    def makeNew(cls, seq, TMgoal, TMrange):
        #type checking
        if(type(seq) != str):
            raise TypeError("seq not a string.")
        if(type(TMgoal) != int and type(TMgoal) != float):
            raise TypeError("TMgoal not an int or float.")
        if(type(TMrange) != int and type(TMrange) != float):
            raise TypeError("TMrange not an int or float")

        newPrimerData = cls()        
        
        #get the primers
        newPrimerData.findPrimers(seq, TMgoal, TMrange)
 
        
        return newPrimerData

    @classmethod
    def loadEntry(cls, newID):
        if(type(newID) != int):
            raise TypeError("newID not an int")
        
        newPrimerData = cls()
            
        newPrimerData.__DBid = newID
        newPrimerData.__inDatabase = True

        return newPrimerData
    
    def setDBid(self, newID):
        if(type(newID) != int):
            raise TypeError("newID not an int")
            
        self.__DBid = newID
        self.__inDatabase = True


    @classmethod
    def makeNull(cls):
        nullData = cls.makeNew("", 0, 0)
        nullData.__seqLeft = "Chose not to make primer."
        nullData.__seqRight = "Chose not to make primer."
        
        return nullData
    
    def addSpacerSeqs(self, spacerData):
        if(type(spacerData) != SpacerData):
            raise TypeError("spacerData not a SpacerData")
            
        #add them; again, complementary, inversion, etc. needed somewhere, I just don't know where
        self.__seqLeft = spacerData.getFullSeqLeft() + self.getSeqLeft()

        self.__seqRight = self.getSeqRight() + spacerData.getFullSeqRight() 
    
    def findPrimers(self, seq, TMgoal, TMrange):
        if(TMgoal <= TMrange):
            self.__primersFound = False
        
        else:
            try:
                #left primer
                TML = 0
                numAL = 0
                numTL = 0
                numGL = 0
                numCL = 0
                i = 0
        
                while abs(TML - TMgoal) > TMrange:
                    if seq[i] == "A":
                        numAL +=1
                    elif seq[i] == "T":
                        numTL +=1
                    elif seq[i] == "G":
                        numGL +=1
                    elif seq[i] == "C":
                        numCL +=1
                        
                    TML = 64.9 + 41*(numGL + numCL - 16.4)/(numAL + numTL + numGL + numCL)
                    
                    i += 1
                        
                #right primer
                TMR = 0
                numAR = 0
                numTR = 0
                numGR = 0
                numCR = 0
                j = -1
        
                while abs(TMR - TMgoal) > TMrange:
                    if seq[j] == "A":
                        numAR +=1
                    elif seq[j] == "T":
                        numTR +=1
                    elif seq[j] == "G":
                        numGR +=1
                    elif seq[j] == "C":
                        numCR +=1
    
                    TMR = 64.9 + 41*(numGR + numCR - 16.4)/(numAR + numTR + numGR + numCR)
    
                    j -= 1
            
                #compare the two
                if(i + j > len(seq)):
                    self.__primersFound = False
                    
                else:
                    self.__primersFound = True
    
                    self.__seqLeft = seq[0:i]
                    self.__GCleft = (numGL + numCL) / len(self.__seqLeft)
                    self.__TMleft = TML
                    
                    self.__seqRight = seq[j:]
                    self.__GCright = (numGR + numCR) / len(self.__seqRight)
                    self.__TMright = TMR
            
            except IndexError:
                self.__primersFound = False
        
        if(not self.getPrimersFound()):
            self.__seqLeft = "Not found."
            self.__GCleft = 0
            self.__TMleft = 0
            
            self.__seqRight = "Not found."
            self.__GCright = 0
            self.__TMright = 0

    def __str__(self):
        if(self.getPrimersFound()):
            tempGCleft = str(round(self.getGCleft() * 100, 4))
            tempGCright = str(round(self.getGCright() * 100, 4))
            tempTMleft = str(round(self.getTMleft(), 3))
            tempTMright = str(round(self.getTMright(), 3))
            
            retStr = "Left Primer: \nSequence: " + self.getSeqLeft() + "\nGC content: " + tempGCleft + "%\nTM: " + tempTMleft + "°C"
            retStr += "\n\nRight Primer: \nSequence: " + self.getSeqRight() + "\nGC content: " + tempGCright + "%\nTM: " + tempTMright + "°C"
        else:
            retStr = "No primers found."
        
        return retStr
    
    #basic getters
    def getID(self):
        return self.__DBid
    
    def getInDatabase(self):
        return self.__inDatabase
    
    def getPrimersFound(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getPrimersFound()
        else:
            return self.__primersFound
    
    def getSeqLeft(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getSeqLeft()
        else:
            return self.__seqLeft
    
    def getGCleft(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getGCleft()
        else:
            return self.__GCleft
    
    def getTMleft(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getTMleft()
        else:
            return self.__TMleft
    
    def getSeqRight(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getSeqRight()
        else:
            return self.__seqRight
    
    def getGCright(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getGCright()
        else:
            return self.__GCright
    
    def getTMright(self):
        if(self.getInDatabase()):
            return PrimerDataDB.query.get(self.getID()).getTMright()
        else:
            return self.__TMright





class Component:
    start = "GAAGAC" #enzyme recog. site?
    end = "GTCTTC"
        
    #standard init, requires NamedSequence, SpacerData, and PrimerData
    def __init__(self, namedSeq, spacerData, primerData):
        #type checking
        if(type(namedSeq) != NamedSequence):
            raise TypeError("namedSeq not a NamedSequence")
        if(type(spacerData) != SpacerData):
            raise TypeError("spacerData not a SpacerData")
        if(type(primerData) != PrimerData):
            raise TypeError("primerData not a PrimerData")
        
        #assign
        self.__namedSeq = namedSeq
        self.__primerData = primerData
        self.__spacerData = spacerData
        
        self.__inDatabase = False
    
    """@classmethod
    def loadEntry(cls, newID):
        if(type(newID) != int):
            raise TypeError("newID not an int")
        
        self.__DBid = newID
        
        entry = ComponentDB.query.get(newID)
            
        newPrimerData.__DBid = newID
        newPrimerData.__inDatabase = True

        return newPrimerData"""
    
    def setID(self, newID):
        if(type(newID) != int):
            raise TypeError("Component newID not an int")
        
        self.__DBid = newID
        self.__inDatabase = True
        
    
    #does not require a NamedSequence, SpacerData, or PrimerData to create the component
    @staticmethod
    def makeFromNew(elemType, name, seq, position, isTerminal, TMgoal, TMrange):
        """I would like to re-think the utility of this function. Is it convenient anymore?"""
        
        #type checking
        checkType(elemType, "elemType")

        if(type(name) != str):
            raise TypeError("name not a string")
        if(type(seq) != str):
            raise TypeError("seq not a string")
        if(type(position) != int):
            raise TypeError("position not an int")
        if(type(isTerminal) != bool):
            raise TypeError("isTerminal is not a bool")
        if(type(TMgoal) != int and type(TMgoal) != float):
            raise TypeError("TMgoal not an int or float")
        if(type(TMrange) != int and type(TMrange) != float):
            raise TypeError("TMrange not an int or float")
        
        #make the other class instances
        newNamedSequence = NamedSequence(elemType, name, seq)
        newSpacerData = SpacerData(position, isTerminal)
        newPrimerData = PrimerData(seq, TMgoal, TMrange)
        
        #make the component
        newComponent = Component(newNamedSequence, newSpacerData, newPrimerData) #or such
        return (newComponent, newNamedSequence)
    
    #requires a NamedSequence, but not a SpacerData or PrimerData to create the component
    @staticmethod
    def makeWithNamedSeq(namedSequence, position, isTerminal, TMgoal, TMrange):
        """Do not use it right now, please."""
        #type checking
        if(type(namedSequence) != NamedSequence):
            raise TypeError("namedSequence not a NamedSequence")
        if(type(position) != int):
            raise TypeError("position not an int")
        if(type(isTerminal) != bool):
            raise TypeError("isTerminal is not a bool")
        if(type(TMgoal) != int and type(TMgoal) != float):
            raise TypeError("TMgoal not an int or float")
        if(type(TMrange) != int and type(TMrange) != float):
            raise TypeError("TMrange not an int or float")
            
        #spacer and primer data
        newSpacerData = SpacerData(position, isTerminal)
        newPrimerData = PrimerData(namedSequence.getSeq(), TMgoal, TMrange)
        
        #make the component
        newComponent = Component(namedSequence, newSpacerData, newPrimerData) #or such
        return newComponent

    #complicated getters
    def getFullSeq(self):
        #return self.getLeftSpacer() + self.getLeftNN() + Component.start + self.getSeq() + Component.end + self.getRightNN() + self.getRightSpacer()
        return self.getFullSpacerLeft() + self.getSeq() + self.getFullSpacerRight()
    
    def getLongName(self):
        retStr = self.getType() + " " + self.getName() + " Position: " + str(self.getPosition())
        if(self.getTerminal()):
            retStr += " terminal"
        else:
            retStr += " non-terminal"
        
        return retStr

    def getHTMLdisplay(self):
        retStr = "ID: " + str(self.getID()) + "<br>"

        retStr += "Position: " + str(self.getPosition()) + "<br>"
        retStr += "Terminal?: " + str(self.getTerminal()) + "<br>"

        retStr += "<br><span class = 'emphasized'>Spacers:</span><br>"
        retStr += "Left: " + self.getLeftSpacer() + "<br>"
        retStr += "Right: " + self.getRightSpacer() + "<br>"
        
        retStr += "<br><span class = 'emphasized'>Primers:</span><br>"
        retStr += "Left primer:<br>GC content: " + str(round(self.getLeftGC() * 100, 4)) + "%<br>TM: " + str(round(self.getLeftTM(), 4)) + "<br>Sequence:<br>" + self.getLeftPrimer() + "<br><br>"
        retStr += "Right primer:<br>GC content: " + str(round(self.getRightGC() * 100, 4)) + "%<br>TM: " + str(round(self.getRightTM(), 4)) + "<br>Sequence:<br>" + self.getRightPrimer() + "<br>"

        return Markup(retStr)

    def __str__(self):
        retStr = "Name: " + self.getName() + "\n"
        retStr += "seq: " + self.getSeq() + "\n"
        retStr += "elemType: " + self.getType() + "\n"
        retStr += "terminal: " + str(self.getTerminal()) + "\n"
        retStr += "position: " + str(self.getPosition()) + "\n"
        retStr += "leftPrimer: " + self.getLeftPrimer() + "\n"
        retStr += "leftGC: " + str(self.getLeftGC()) + "\n"
        retStr += "leftTM: " + str(self.getLeftTM()) + "\n"
        retStr += "rightPrimer: " + self.getRightPrimer() + "\n"
        retStr += "rightGC: " + str(self.getRightGC()) + "\n"
        retStr += "rightTM: " + str(self.getRightTM()) + "\n"
        retStr += "leftSpacer: " + self.getLeftSpacer() + "\n"
        retStr += "rightSpacer: " + self.getRightSpacer() + "\n"
        retStr += "leftNN: " + self.getLeftNN() + "\n"
        retStr += "rightNN: " + self.getRightNN()
        return retStr
    
    def getCompZIP(self):
        #primers and complete sequence
        retDict = {}
        
        idStr = self.getID()
        idStrAndName = self.getID() + " (" + self.getName() + ")"
        
        retDict[idStr + "-CompleteSequence.fasta"] = ">" + idStrAndName + " complete sequence\n" + self.getFullSeq()
        retDict[idStr + "-LeftPrimer.fasta"] = ">" + idStrAndName + " left primer\n" + self.getLeftPrimer()
        retDict[idStr + "-RightPrimer.fasta"] = ">" + idStrAndName + " right primer\n" + self.getRightPrimer()
        
        return retDict
    
    #basic getters
    def getDBid(self):
        return self.__DBid
    
    def getID(self):
        nameID = self.getNamedSequence().getNameID()
        retStr = self.getType() + "-" + str(nameID).zfill(3) + "-" + str(self.getPosition()).zfill(3) + self.getTerminalLetter()
        return retStr


    def getNamedSequence(self):
        return self.__namedSeq
    
    def getName(self):
        return self.getNamedSequence().getName()
    
    def getSeq(self):
        return self.getNamedSequence().getSeq()
    
    def getType(self):
        return self.getNamedSequence().getType()

    
    def getSpacerData(self):
        return self.__spacerData

    def getTerminal(self):
        return self.getSpacerData().getIsTerminal()
    
    def getTerminalLetter(self):
        return self.getSpacerData().getTerminalLetter()
    
    def getPosition(self):
        return self.getSpacerData().getPosition()

    def getLeftSpacer(self):
        return self.getSpacerData().getSpacerLeft()
    
    def getRightSpacer(self):
        return self.getSpacerData().getSpacerRight() #what is this naming

    def getLeftNN(self):
        return self.getSpacerData().getLeftNN()
    
    def getRightNN(self):
        return self.getSpacerData().getRightNN()

    def getFullSpacerLeft(self):
        return self.getSpacerData().getFullSeqLeft()

    def getFullSpacerRight(self):
        return self.getSpacerData().getFullSeqRight()


    def getPrimerData(self):
        return self.__primerData
    
    def getLeftPrimer(self):
        return self.getPrimerData().getSeqLeft()
    
    def getLeftGC(self):
        return self.getPrimerData().getGCleft()
    
    def getLeftTM(self):
        return self.getPrimerData().getTMleft()
    
    def getRightPrimer(self):
        return self.getPrimerData().getSeqRight()
    
    def getRightGC(self):
        return self.getPrimerData().getGCright()
    
    def getRightTM(self):
        return self.getPrimerData().getTMright()
    