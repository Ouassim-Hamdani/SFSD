from sys import getsizeof
from pickle import dumps,loads
from texttable import Texttable
class Bloc():
    """Bloc structure"""
    """blocSize : integer representing the number of elements in a bloc"""
    """other parameters have default values and they represent the length of champs in an element"""
    """Our bloc has 4 champs seperated by * and the void is filled by #"""
    def __init__(self,blocSize:int,fChLen=10,sChLen=15,tChLen=8,foChLen=10):
        self.blocSize = blocSize
        self.tab = ["#"*fChLen+"*"+"#"*sChLen+"*"+"#"*tChLen+"*"+"#"*foChLen]*blocSize # ["###*##*##*##","###*##*##*##"]
        self.nb = 0
def AffEnTete(f,ordre:int,cara:int):
    '''Writes file caracteristics'''
    '''Note, the caracterestic are delt as integers'''
    startAdress = ordre*getsizeof(dumps(0))
    #startAdress represent the adress on the file where to write the cara.
    with open(f.filePath,"rb+") as fi:
        fi.seek(startAdress,0)
        fi.write(dumps(cara))
def Entete(f,ordre:int):
    '''Acess the caracteristic of file f, with the given order'''
    startAdress= ordre*getsizeof(dumps(0))
    with open(f.filePath,"rb") as fi:
        fi.seek(startAdress,0)
        return loads(fi.read(getsizeof(dumps(0))))
    
class File():
    def __init__(self,filePath:str,blocSize:int):
        '''BlocSize : Integer representing the numbers of elements in a bloc'''
        '''filePath : String represeting the name of our file in the current directory or a directory to the file'''
        self.blocSize = blocSize
        self.filePath = filePath
        self.bufSize = getsizeof(dumps(Bloc(blocSize))) + len(Bloc(blocSize).tab[0])*(blocSize-1)+(blocSize-1)
        #bufSize : Iterative size of bits to Iterate elements, used in readBloc,writeBloc'''
        #The following section checks if the file already exixst if not, it will create it
        try:
            with open(filePath) as ff:
                pass
        except FileNotFoundError:
            with open(filePath,"w") as ff:
                pass
    def writeBloc(self,blocAdress:int,bloc:Bloc):
        """Equivilant to EcrireDir, writes a bloc to a given adress on the file"""
        '''blocAdress : integer representing the number/adress of the bloc in the file'''
        '''bloc : The bloc to write of class Bloc'''
        '''Warning this function doesn't wipe out the buf, if you want to do that call cleanBuf function'''
        nb=0
        for i in bloc.tab:
            if i.count("#")<43:
                nb+=1
            else:
                break
        bloc.nb=nb
        with open(self.filePath,"rb+") as f:
            f.seek(2*getsizeof(dumps(0))+blocAdress*(self.bufSize))
            f.write(dumps(bloc))
    def readBloc(self,blocAdress:int,buf:Bloc):
        """Equivilant to LireDir, reads a bloc from a given adress and writes it to buf"""
        '''blocAdress : integer representing the bloc number/adress where to read from'''
        '''buf : a buffer of class Bloc where to store our bloc'''
        cleanBuf(buf) #Functions that make sure our buf is clean of any previous data, wipes out data
        with open(self.filePath,"rb") as f:
            f.seek(2*getsizeof(dumps(0))+blocAdress*(self.bufSize))
            buf.tab = loads(f.read(self.bufSize)).tab
            f.seek(2*getsizeof(dumps(0))+blocAdress*(self.bufSize))
            buf.nb =  loads(f.read(self.bufSize)).nb
    def createFile(self):
        '''Initial load of a file (Chargement initial)'''
        buf = Bloc(self.blocSize)
        blocIterator = 0 #i
        elementIterator = 0 #j
        total = 0 #total number of insertions
        while True:
            total+=1
            etud = [input("Prenom : "),input("Nom : "),input("nombre d'inscri : "),input("Filiere : ")]
            if elementIterator < buf.blocSize:
                fillChamps(etud,buf,elementIterator) # buf.tab[i] = etud
                elementIterator+=1
                buf.nb+=1
            else:
                self.writeBloc(blocIterator,buf) #EcrireDir(f,blocIterator,buf)
                cleanBuf(buf)
                fillChamps(etud,buf) #buf.tab[0] = etud
                elementIterator = 1
                blocIterator+=1
            an = input("Do you wanna stop? (y)")
            if an.lower()=="y":
                break
        self.writeBloc(blocIterator,buf)
        AffEnTete(self,0,total)
        AffEnTete(self,1,blocIterator+1)
    def printContent(self):
        '''Prints the content of the file'''
        buf = Bloc(self.blocSize)
        t=1
        print(f"\n> > > File : {self.filePath}\n")
        ta = Texttable()
        ta.add_row(['First Name','Last Name','ID',"Filiere"])
        ta.set_cols_dtype(['t','t','t','t'])
        for i in range(Entete(self,1)):
            self.readBloc(i,buf)
            ta.add_row(["BlOC",f"NUMBER {i}","BlOC",f"NUMBER {i}"])
            for stInd in range(buf.nb):
                if buf.tab[stInd][0]!="-":
                    stud=buf.tab[stInd]
                    stud = stud.split("*")
                    stud = [x.replace("#","") for x in stud]
                    ta.add_row(stud)
                    #print(f"Student #{t}\n  Name : {stud[0]}\n  Last Name : {stud[1]}\n  ID : {stud[2]}\n  Filiere : {stud[3]}")
                    #print("-----------------------------")
                    t+=1
        print(ta.draw())
def cleanBuf(buf): 
    """Function that empty the buffer tab (tkhalih all ####*###)"""
    """Buf.tab is list of stirngs and strings have champs represented as  ##, seperator is *"""
    buf.nb=0
    for i in range(len(buf.tab)):
        tempL = buf.tab[i].split("*")
        for j in range(len(tempL)):
            tempL[j]="#"*len(tempL[j])
        buf.tab[i] = "*".join(tempL)
def fillChamps(champs,buf,pos=0):
    """Function that takes champs (list of champ to fill(4) and pos of element on bloc (index) and buf where will save the champs"""
    '''The pos is set to 0, when an argument is not passed'''
    '''Do the cleaning first'''
    listS = buf.tab[pos].split("*")
    """Buf is an object of class Bloc with tab beigng list of element, element is a string"""
    for i,el in enumerate(champs): 
        listS[i] = el+listS[i][len(el):]
    buf.tab[pos] = "*".join(listS)
def readContent(element):
    '''Take in an element of our buffer and returns a list of it's data'''
    return [x.replace("#","") for x in element.split("*")]