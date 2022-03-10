"""IPPcode21
@file interpret.py
@author Kozhevnikov Dmitrii (xkozhe00)
"""
import sys, re, fileinput
import xml.etree.ElementTree as ET

def checkStartArguments():
    """ Function which control validation of start arguments """

    sourcePath = ""
    inputPath = ""
    # how much arguments
    if len(sys.argv) == 2:
    
        # --help
        if sys.argv[1] == "--help":
            print("This program interprets code in language IPPcode21 parsed to XML")
            print("For start:")
            print("python3.8 interpret.py --source=file")
            print("or")
            print("python3.8 interpret.py --input=file")
            exit(0)
        
        # --source only
        elif sys.argv[1][:9] == "--source=":
            if sys.argv[1][9:] == "":
                print("ERROR: Invalid arguments", file = sys.stderr)
                exit(10)
            else:
                return sys.argv[1][9:], sys.__stdin__
        
        # --input only
        elif sys.argv[1][:8] == "--input=":
            if sys.argv[1][8:] == "":
                print("ERROR: Invalid arguments", file = sys.stderr)
                exit(10)
            else:
                return sys.__stdin__, sys.argv[1][8:]
        
        # error for 2 arguments
        else:
            print("ERROR: Invalid arguments", file = sys.stderr)
            exit(10)

    elif len(sys.argv) == 3:

        # --source --input
        if sys.argv[1][:9] == "--source=" and sys.argv[2][:8] == "--input=":

            if sys.argv[1][9:] == '' and sys.argv[2][8:] == '':
                print("ERROR: Invalid arguments", file = sys.stderr)
                exit(10)
            
            if sys.argv[1][9:] == '':
                sourcePath = sys.__stdin__
            else:
                sourcePath = sys.argv[1][9:]
            
            if sys.argv[2][8:] == '':
                inputPath = sys.__stdin__
            else:
                inputPath = sys.argv[2][8:]

            return sourcePath,  inputPath

        # --input --source
        elif sys.argv[2][:9] == "--source=" and sys.argv[1][:8] == "--input=":

            if sys.argv[2][9:] == '' and sys.argv[1][8:] == '':
                print("ERROR: Invalid arguments", file = sys.stderr)
                exit(10)

            
            if sys.argv[2][9:] == '':
                sourcePath = sys.__stdin__
            else:
                sourcePath = sys.argv[2][9:]
            
            if sys.argv[1][8:] == '':
                inputPath = sys.__stdin__
            else:
                inputPath = sys.argv[1][8:]

            return sourcePath,  inputPath
        
        # error
        else:
            print("ERROR: Invalid arguments", file = sys.stderr)
            exit(10)

    # bad argument count
    else:
        print("Bad arguments count", file = sys.stderr)
        exit(10)

class Stack():
    """ Class Stack creates a stack for storing variable values

    Attributes
    ----------
    stackData : list
        List of data

    Methods
    -------
    pushOnStack(data)
        Push data on stack
    pop()
        Pop data from stack
    """

    # create empty stack
    def __init__(self):
        self.stackData = []
    
    # push data on stack
    def pushOnStack(self, data):
        """ Push data on stack

        Parameters
        ----------
        data
            Data to stack
        """

        self.stackData.append(data)
    
    # pop data from stack
    def pop(self):
        """ Pop data on stack """

        stackLength = len(self.stackData)

        # error for empty stack
        if stackLength == 0:
            print("ERROR: Can't pop data from empty stack", file = sys.stderr)
            exit(56)
        return self.stackData.pop()

class Frame:
    """ Class Frame creates frames to control Global frames Temporary frames and Local frames

    Methods
    -------
    checkTypeOfFrame(frameName)
        Check type of Frame: GF, LF, TF
    set(name, setVal)
        Set value in frame
    get(name)
        Get value from frame
    addName(name)
        Added name in frame if it not exists
    """

    globFrame = {}
    locFrame = None
    tempFrame = None
    tempFrameStack = []

    @ classmethod
    def checkTypeOfFrame(cls, frameName):
        """ Check type of frame

        Parameters
        ----------
        frameName
            Name of frame
        """
        if frameName[:3] == "GF@":
            mainFrame = cls.globFrame

        elif frameName[:3] == "LF@":
            mainFrame = cls.locFrame

        elif frameName[:3] == "TF@":
            mainFrame = cls.tempFrame

        else:
            print("ERROR: Invalid frame syntax", file = sys.stderr)
            exit(32)
        
        return mainFrame

    @classmethod
    def set(cls, name, setVal):
        """ Set data in frame

        Parameters
        ----------
        name
            Name i frame
        setVal
            Value to set in frame
        """
        mainFrame = cls.checkTypeOfFrame(name)
        name = name[3:]

        if name not in mainFrame:
            print("ERROR: Could not set value", file = sys.stderr)
            exit(54)
        

        if type(setVal) == varType:
            setVal = setVal.getVal()

        mainFrame[name] = setVal

    @classmethod
    def get(cls, name):
        """ Get data from frame

        Parameters
        ----------
        name
            Name i frame
        """
        mainFrame = cls.checkTypeOfFrame(name)
        name = name[3:]

        if name not in mainFrame:
            print("ERROR: Could not get value", file = sys.stderr)
            exit(54)

        gettedVal = mainFrame[name]
        return gettedVal

    @classmethod
    def addName(cls, name):
        """ Added name in frame list

        Parameters
        ----------
        name
            Name in frame
        """
        mainFrame = cls.checkTypeOfFrame(name)
        name = name[3:]

        if name in mainFrame:
            print("ERROR: Global frame existed", file = sys.stderr)
            exit(59)
    
        mainFrame[name] = None
        

class varType:
    """ Class varType creates a variable of the var type

    Attributes
    ----------
    name
        Name of var variable

    Methods
    -------
    getVal()
        Get var value from frame
    getName()
        Get var name
    setVal(value)
        Set var value in frame
    getValAndType(typeOfVal)
        Get value and type of var
    """
    def __init__(self, name):
        self.name = name

    def getVal(self):
        """ Get var value """
        name = self.getName()
        return Frame.get(name)

    def getName(self):
        """ Get var name """
        return self.name

    def setVal(self, value):
        """ Set var value in frame

        Parameters
        ----------
        value
            Value of var
        """
        name = self.getName()
        Frame.set(name, value)

    def getValAndType(self, typeOfVal):
        """ Get value and type of var

        Parameters
        ----------
        typeOfVal
            Type of value
        """
        value = self.getVal()

        if type(value) != typeOfVal:
            print("ERROR: Bad type", file = sys.stderr)
            exit(53)
        
        return value

    def __str__(self):
        return self.getValAndType(str)
    
    def __int__(self):
        return self.getValAndType(int)

    def __bool__(self):
        return self.getValAndType(bool)

class labelType:
    """ Class labelType creates for control labels

    Methods
    -------
    saveLabel(name)
        Search and save label
    jumpOnLabel(name)
        Jump on label
    """
    labelList = {}  # List of labels
    
    @classmethod
    def saveLabel(cls, name):
        """ Save label if it exists

        Parameters
        ----------
        name
            Name of label
        """
        name = str(name)

        if name in cls.labelList:
            print("ERROR: Two identical labels", file = sys.stderr)
            exit(52)
        
        else:
            cls.labelList[name] = Interpretator.order


    @classmethod
    def jumpOnLabel(cls, name):
        """ Jump on label if it exists

        Parameters
        ----------
        name
            Name of label
        """
        name = str(name)

        if name not in cls.labelList:
            print("ERROR: Label does not exist", file = sys.stderr)
            exit(52)

        else:
            Interpretator.order = cls.labelList[name]

class symb:
    """ Class symb for <symb> """
    pass

class label:
    """ Class label creates for control label-type

    Attributes
    ----------
    name
        Name of label

    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class atype:
    """ Class atype creates for control type-type

    Attributes
    ----------
    name
        Name of type

    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class nill:
    """ Class nill creates for control nil-type

    Attributes
    ----------
    name
        Name of nil-type

    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Interpretator():
    """ Class Interpretator responsible for checking the program and interpreting it

    Methods
    -------
    isRootValid(root)
        Control validation of root in XML
    loadingInstructions(root)
        Loads the instructions, checks their correctness and executes them
    """
    stackForValues = Stack()    # stack for values
    callsStack = Stack()    # CALL/RETURN stack
    
    @staticmethod
    def isRootValid(root):
        """ Control validation of root in XML

        Parameters
        ----------
        root
            Root of XML file
        """      
        # <program> control
        if root.tag != "program":
            print("ERROR: Node <program> not found in root", file = sys.stderr)
            exit(32)

        # <language> control
        if "language" in root.attrib:
            language = root.attrib["language"]
            language = language.upper()

            # Head control
            if language != "IPPCODE21":
                print("ERROR: Node <language> have bad head", file = sys.stderr)
                exit(32)
            del root.attrib["language"]

        else:
            print("ERROR: Node <language> not found", file = sys.stderr)
            exit(32)
        
        # <name> control
        if "name" in root.attrib:
            del root.attrib["name"]
        
        # <description> control
        if "description" in root.attrib:
            del root.attrib["description"]
        
        # empty atribute control
        if len(root.attrib) != 0:
            print("ERROR: Bad attributes in file", file = sys.stderr)
            exit(32)
        
    @classmethod
    def loadingInstructions(cls, root):
        """ Loads the instructions, checks their correctness and executes them

        Parameters
        ----------
        root
            Root of XML file
        """   
        sortXML(root, 'order')
        rootLen1 = len(root)
        opcode = ""
        count = 0                                       # count of operations
        a = []                                          # order list
        readIndex = 0                                   # index in list

        for count in range(rootLen1):
            orded = int(root[count].attrib['order'])
            a.append(orded)
            count = count + 1
        
        instructionsNode = root.findall("./")           # take instructions node
        
        # searching and save labels
        for instrNode in instructionsNode:
            try:
                instrNode.attrib["opcode"].upper()
            except:
                print("ERROR: No opcode instruction", file = sys.stderr)
                exit(32)
            if instrNode.attrib["opcode"].upper() == "LABEL":
                cls.order = int(instrNode.attrib["order"])
                instr = checkInstruction(instrNode)
                opcode = instr.attrib["opcode"].upper()
                args = takeArgs(instr)
                countOfArgs = len(args)
                instrCarrying(opcode, args, countOfArgs, readIndex)

        i = 0                                           # iterator
        cls.order = int(root[i].attrib['order'])        # order 
        final = int(root[-1].attrib['order'])           # final order

        while cls.order <= final:
            
            """ Operation execution cycle """
            i = a.index(cls.order)                      # take position

            if opcode == "RETURN":
                i = i + 1
                if i >= count:
                    break

            nodeCommand = instructionsNode[i]           # take command
            instr = checkInstruction(nodeCommand)       # checking the correctness of the instructions
            opcode = instr.attrib["opcode"].upper()     # take opcode
            # skipping labels
            if opcode == "LABEL":
                i = i + 1
                cls.order = int(root[i].attrib['order'])
                continue
            args = takeArgs(instr)                      # take arguments arg
            countOfArgs = len(args)
            
            # final command control
            if i == count or cls.order == final:
                if opcode == "CALL":
                    instrCarrying(opcode, args, countOfArgs, readIndex)
                    continue
                else:
                    instrCarrying(opcode, args, countOfArgs, readIndex)                
                    break

            # commands with jumps
            if opcode != "JUMP" or opcode != "CALL" or opcode != "JUMPIFEQ" or opcode != "JUMPIFNEQ":
                i = i + 1
                cls.order = int(root[i].attrib['order'])

            instrCarrying(opcode, args, countOfArgs, readIndex)         # executing an instruction

            # special for read command
            if opcode == "READ":
                readIndex = readIndex + 1                               # iterate readIndex


def checkInstruction(instruction):
    """ Check the instruction correctness

    Parameters
    ----------
    instruction
        Instruction for check
    """   

    if instruction.tag != "instruction":
        print("ERROR: Invalid instruction", file = sys.stderr)
        exit(32)
    
    return instruction

def takeArgs(instruction):
    """ Takes arguments arg from instruction

    Parameters
    ----------
    instruction
        Instruction for working
    """   
    arguments = [None] * len(instruction)
    argNumber = 0

    # arg working
    for argNumber in instruction:

        # arg control
        if argNumber.tag[:3] != "arg":
            print("ERROR: Invalid arguments", file = sys.stderr)
            exit(32)
        
        argType = argNumber.attrib["type"]                                  # type of arg
        argValue = argNumber.text                                           # value of arg
        index = int(argNumber.tag[3:])                                      # index of arg
        try:
            arguments[index - 1] = takeArgsTypeAndValue(argType, argValue)      # takes type and value of arg
        except:
            print("ERROR: Invalid argument", file = sys.stderr)
            exit(32)

    return arguments

def takeArgsTypeAndValue(typeXML, valueXML):
    """ Takes type and value of argument

    Parameters
    ----------
    typeXML
        Type of argument from XML file
    valueXML
        Value of argument from XML file
    """ 

    # int type 
    if typeXML == "int":
        if not re.search(r"^[-+]?\d+$", valueXML):
            print("ERROR: Invalid int value", file = sys.stderr)
            exit(32)
        return int(valueXML)
    
    # type bool
    elif typeXML == "bool":
        if valueXML == "true":
            boolValue = True
        elif valueXML == "false":
            boolValue = False
        else: 
            print("ERROR: Invalid bool value", file = sys.stderr)
            exit(32)
        return boolValue
    
    # type nil
    elif typeXML == "nil":
        if valueXML != "nil":
            print("ERROR: Invalid nil value", file = sys.stderr)
            exit(32)
        return nill(valueXML)
    
    # type type
    elif typeXML == "type":
        if valueXML != "int" and valueXML != "string" and valueXML != "bool":
            print("ERROR: Invalid type value", file = sys.stderr)
            exit(32)
        return atype(valueXML)

    # type label
    elif typeXML == "label":
        if not re.search(r"^[\w\_\-\$\&\%\*\!\?][\w\_\-\$\&\%\*\!\?]*$", valueXML):
            print("ERROR: Invalid label value", file = sys.stderr)
            exit(32)
        return label(valueXML)
    
    # type var
    elif typeXML == "var":
        if not re.search(r"^(LF|TF|GF)@[\w\_\-\$\&\%\*\!\?][\w\_\-\$\&\%\*\!\?]*$", valueXML):
            print("ERROR: Invalid var value", file = sys.stderr)
            exit(32)
        return varType(valueXML)
    
    # type string
    elif typeXML == "string":

        # empty string
        if valueXML == None:
            valueXML = ""
        
        # control string
        if re.search(r"(?!\\[0-9]{3})[\s\\#]", valueXML):
            print("ERROR: Invalid string value", file = sys.stderr)
            exit(32)
        
        # decode string
        if not re.match(r'(\\[0-9]{0,2}($|[^0-9\\])|\\[0-9]{4,})', valueXML, re.UNICODE):
            decodeString = re.compile(r'(\\[0-9]{3})', re.UNICODE)
            blocks = decodeString.split(valueXML)
            valueXML = ''       # new string

            #cycle for creating new string with decoding symbols
            for block in blocks:
                if decodeString.match(block):
                    block = chr(int(block[1:]))
                valueXML += block

        return valueXML
    else:
        print("ERROR: Bad argument type", file = sys.stderr)
        exit(32)

def checkArgument(*arguments, args, countOfArgs):
    """ Checks whether the arguments are correct

    Parameters
    ----------
    *arguments
        Arguments passed for validation
    args
        Program arguments
    countOfArgs
        Number of program arguments
    """ 

    argLen = len(arguments)                                             # number of arguments passed

    # checking the number of passed and expected arguments
    if countOfArgs != argLen:
        print("ERROR: Invalid count of arguments", file = sys.stderr)
        exit(32)
    arguments = list(arguments)                                         # list for arguments
    i = 0

    # control arguments type
    for argument in args:
        if arguments[i] == symb:
            arguments[i] = [int, varType, bool, str, nill, atype]
        
        typeOfArg = type(argument)

        if type(arguments[i]) == type:
            if typeOfArg != arguments[i]:
                print("ERROR: Invalid type of argument", file = sys.stderr)
                exit(53)
        
        elif type(arguments[i]) == list:
            if typeOfArg not in arguments[i]:
                print("ERROR: Invalid type of argument", file = sys.stderr)
                exit(53)
        
        else:
            print("ERROR: Can't use instruction", file = sys.stderr)
            exit(53)
        
        i = i + 1
    

def instrCarrying(opcode, args, countOfArgs, readIndex):
    """ Checking arguments and executing instructions

    Parameters
    ----------
    opcode
        Command for executing
    args
        Arguments for command
    countOfArgs
        Number of program arguments
    readIndex
        Index for READ command
    """ 

    # Arithmetic, relational, boolean and conversion instructions

    if opcode == "ADD":
        checkArgument(varType, [varType, int], [varType, int], args=args, countOfArgs=countOfArgs)
        addResult = int(args[1]) + int(args[2])
        args[0].setVal(addResult)
    
    elif opcode == "SUB":
        checkArgument(varType, [varType, int], [varType, int], args=args, countOfArgs=countOfArgs)
        subResult = int(args[1]) - int(args[2])
        args[0].setVal(subResult)
    
    elif opcode == "MUL":
        checkArgument(varType, [varType, int], [varType, int], args=args, countOfArgs=countOfArgs)
        mulResult = int(args[1]) * int(args[2])
        args[0].setVal(mulResult)

    elif opcode == "IDIV":
        checkArgument(varType, [varType, int], [varType, int], args=args, countOfArgs=countOfArgs)

        if int(args[2]) == 0:
            print("ERROR: Trying to divide by 0", file = sys.stderr)
            exit(57)

        idivResult = int(args[1]) // int(args[2])
        args[0].setVal(idivResult)

    elif opcode == "LT" or opcode == "GT" or opcode == "EQ":
        checkArgument(varType, symb, symb, args=args, countOfArgs=countOfArgs)
        firstArg = args[1]
        secondArg = args[2]

        if type(firstArg) == varType:
            firstArg = args[1].getVal()
        
        if type(secondArg) == varType:
            secondArg = args[2].getVal()

        if firstArg == "nil" or secondArg == "nil":
            if opcode != "EQ":
                print("ERROR: Bad operation with nil-type", file = sys.stderr)
                exit(53)
            else:
                eqResult = firstArg == secondArg
                args[0].setVal(eqResult)
            
        elif (type(firstArg) != type(secondArg)):
            print("ERROR: Not equal types to LT/GT/EQ command", file = sys.stderr)
            exit(53)

        if opcode == "LT":
            ltResult = firstArg < secondArg
            args[0].setVal(ltResult)

        elif opcode == "GT":
            gtResult = firstArg > secondArg
            args[0].setVal(gtResult)

        elif opcode == "EQ":
            eqResult = firstArg == secondArg
            args[0].setVal(eqResult)
        
        else:
            print("ERROR: Bad operation in LT/GT/EQ command", file = sys.stderr)
            exit(99)
        
    elif opcode == "AND" or opcode == "OR" or opcode == "NOT":

        if opcode == "AND":
            checkArgument(varType, [varType, bool], [varType, bool], args=args, countOfArgs=countOfArgs)
            andResult = bool(args[1]) and bool(args[2])
            args[0].setVal(andResult)
        
        elif opcode == "OR":
            checkArgument(varType, [varType, bool], [varType, bool], args=args, countOfArgs=countOfArgs)
            orResult = bool(args[1]) or bool(args[2])
            args[0].setVal(orResult)

        elif opcode == "NOT":
            checkArgument(varType, [varType, bool], args=args, countOfArgs=countOfArgs)
            notResult = not bool(args[1])
            args[0].setVal(notResult)
    
    elif opcode == "INT2CHAR":
        checkArgument(varType, [varType, int], args=args, countOfArgs=countOfArgs)
        intValue = int(args[1])

        try:
            int2charResult = chr(intValue)
        except:
            print("ERROR: Bad operation INT2CHAR", file = sys.stderr)
            exit(58)
        
        args[0].setVal(int2charResult)

    elif opcode == "STRI2INT":
        checkArgument(varType, [varType, str], [varType, int], args=args, countOfArgs=countOfArgs)
        stringValue = str(args[1])
        positionInString = int(args[2])
        stringLen = len(stringValue)

        if positionInString >= stringLen or positionInString < 0:
            print("ERROR: Bad operation STRI2INT", file = sys.stderr)
            exit(58)
        
        stri2intResult = stringValue[positionInString]
        stri2intResult = ord(stri2intResult)
        args[0].setVal(stri2intResult)


    # Working with framework, function calls

    elif opcode == "MOVE":
        checkArgument(varType, symb, args=args, countOfArgs=countOfArgs)
        args[0].setVal(args[1])

    elif opcode == "CREATEFRAME":
        checkArgument(args=args, countOfArgs=countOfArgs)
        Frame.tempFrame = {}

    elif opcode == "PUSHFRAME":
        checkArgument(args=args, countOfArgs=countOfArgs)
        try:
            key = list(iter(Frame.tempFrame))[0]
            val = dict(Frame.tempFrame)[key]
        except:
            exit(55)

        if val == None:
            print("ERROR: Not defined frame", file = sys.stderr)
            exit(55)

        else:
            TF = Frame.tempFrame
            Frame.tempFrameStack.append(TF) # TF on stack
            Frame.locFrame = Frame.tempFrameStack[-1]   # LF = TF on stack
            Frame.tempFrame = None

    elif opcode == "POPFRAME":
        checkArgument(args=args, countOfArgs=countOfArgs)
        key = list(iter(Frame.locFrame))[0]
        val = dict(Frame.locFrame)[key]
        if val == None:
            print("ERROR: Not defined frame", file = sys.stderr)
            exit(55)
        
        else:
            Frame.tempFrame = Frame.tempFrameStack.pop()
            Frame.locFrame = None

    
    elif opcode == "DEFVAR":
        checkArgument(varType, args=args, countOfArgs=countOfArgs)
        argName = args[0].getName()
        try:
            Frame.addName(argName)
        except:
            exit(55)

    elif opcode == "CALL":
        order = Interpretator.order
        Interpretator.callsStack.pushOnStack(order)
        checkArgument(label, args=args, countOfArgs=countOfArgs)
        labelType.jumpOnLabel(args[0])

    elif opcode == "RETURN":
        checkArgument(args=args, countOfArgs=countOfArgs)
        Interpretator.order = Interpretator.callsStack.pop()



    # Working with the data tray

    elif opcode == "PUSHS":
        checkArgument(symb, args=args, countOfArgs=countOfArgs)
        Interpretator.stackForValues.pushOnStack(args[0])

    elif opcode == "POPS":
        checkArgument(varType, args=args, countOfArgs=countOfArgs)
        popsVal = Interpretator.stackForValues.pop()
        args[0].setVal(popsVal)


    # Working with strings

    elif opcode == "CONCAT":
        checkArgument(varType, [varType, str], [varType, str], args=args, countOfArgs=countOfArgs)
        concatResult = str(args[1]) + str(args[2])
        args[0].setVal(concatResult)

    elif opcode == "STRLEN":
        checkArgument(varType, [varType, str], args=args, countOfArgs=countOfArgs)
        string = str(args[1])
        strlenResult = len(string)
        args[0].setVal(strlenResult)

    elif opcode == "GETCHAR":
        checkArgument(varType, [varType, str], [varType, int], args=args, countOfArgs=countOfArgs)
        string = str(args[1])
        indexPosition = int(args[2])
        lenOfString = len(string)

        if indexPosition < 0 or indexPosition >= lenOfString:
            print("ERROR: Position is out of range", file = sys.stderr)
            exit(58)

        getcharResult = string[indexPosition]
        args[0].setVal(getcharResult)

    elif opcode == "SETCHAR":
        checkArgument(varType, [varType, int], [varType, str], args=args, countOfArgs=countOfArgs)
        stringSet = str(args[0])
        indexPosition = int(args[1])
        znak = str(args[2])
        lenOfString = len(stringSet)
        lenOfZnak = len(znak)

        if indexPosition < 0 or indexPosition >= lenOfString or lenOfZnak <= 0:
            print("ERROR: Position is out of range", file = sys.stderr)
            exit(58)

        setcharResult = stringSet[:indexPosition] + znak[0] + stringSet[indexPosition + 1:]
        args[0].setVal(setcharResult)


    # Working with types

    elif opcode == "TYPE":
        checkArgument(varType, symb, args=args, countOfArgs=countOfArgs)
        firstArg = args[1]

        if type(firstArg) == varType:
            firstArg = args[1].getVal()
        
        typeOfArg = str(type(firstArg))
    
        if re.search(r"^<class \'int\'>", typeOfArg):
            typeResult = "int"
            args[0].setVal(typeResult)

        elif re.search(r"^<class \'bool\'>", typeOfArg):
            typeResult = "bool"
            args[0].setVal(typeResult)

        elif re.search(r"^<class \'__main__.nill\'>", typeOfArg):
            typeResult = "nil"
            args[0].setVal(typeResult)

        elif re.search(r"^<class \'str\'>", typeOfArg):
            typeResult = "string"
            args[0].setVal(typeResult)
        else:
            typeResult = ""
            args[0].setVal(typeResult)


    # Program flow control instructions
  
    elif opcode == "LABEL":
        checkArgument(label, args=args, countOfArgs=countOfArgs)
        labelType.saveLabel(args[0])

    elif opcode == "JUMP":
        checkArgument(label, args=args, countOfArgs=countOfArgs)
        labelType.jumpOnLabel(args[0])

    elif opcode == "JUMPIFEQ":
        checkArgument(label, symb, symb, args=args, countOfArgs=countOfArgs)
        firstArg = args[1]
        secondArg = args[2]

        if type(firstArg) == varType:
            firstArg = args[1].getVal()

        if type(secondArg) == varType:
            secondArg = args[2].getVal()

        typeOfFirstArg = str(type(firstArg))
        typeOfSecondArg = str(type(secondArg))
        
        if (type(firstArg) == type(secondArg)) or (re.search(r"^<class \'__main__.nill\'>", typeOfFirstArg)) or (re.search(r"^<class \'__main__.nill\'>", typeOfSecondArg)):
            jumpifeqResult = firstArg == secondArg

            if str(firstArg) == "nil" and str(secondArg) == "nil":
                jumpifeqResult = True

            if jumpifeqResult == True:
                labelType.jumpOnLabel(args[0])

        else: 
            print("ERROR: Bad type in JUMPIFEQ", file = sys.stderr)
            exit(53)

    elif opcode == "JUMPIFNEQ":
        checkArgument(label, symb, symb, args=args, countOfArgs=countOfArgs)
        firstArg = args[1]
        secondArg = args[2]

        if type(firstArg) == varType:
            firstArg = args[1].getVal()

        if type(secondArg) == varType:
            secondArg = args[2].getVal()

        typeOfFirstArg = str(type(firstArg))
        typeOfSecondArg = str(type(secondArg))
        
        if (type(firstArg) == type(secondArg)) or (re.search(r"^<class \'__main__.nill\'>", typeOfFirstArg)) or (re.search(r"^<class \'__main__.nill\'>", typeOfSecondArg)):
            jumpifeqResult = firstArg != secondArg

            if str(firstArg) == "nil" and str(secondArg) == "nil":
                jumpifeqResult = False

            if jumpifeqResult == True:
                labelType.jumpOnLabel(args[0])

        else: 
            print("ERROR: Bad type in JUMPIFNEQ", file = sys.stderr)
            exit(53)

    elif opcode == "EXIT":
        checkArgument([varType, int], args=args, countOfArgs=countOfArgs)
        firstArg = args[0]

        if type(firstArg) == varType:
            firstArg = args[0].getVal()
        
        if int(firstArg) >= 0 and int(firstArg) <= 49:
            exit(int(firstArg))

        else:
            print("ERROR: Bad symb value in EXIT", file = sys.stderr)
            exit(57) 


    # Debug instructions

    elif opcode == "DPRINT":
        checkArgument(symb, args=args, countOfArgs=countOfArgs)
        pass

    elif opcode == "BREAK":
        checkArgument(args=args, countOfArgs=countOfArgs)
        pass

    # Input-output instructions
    
    elif opcode == "READ":
        checkArgument(varType, atype, args=args, countOfArgs=countOfArgs)
        lenOfArray = len(inputArray)
        readFlag = 0
        if readIndex > lenOfArray - 1:
            readString = ""
            readFlag = 1
        else:
            readString = inputArray[readIndex][0]
        argu = str(args[1])
        if argu == "bool":
            readString = readString.lower()
         
            if readString == "true":
                readResult = True
                args[0].setVal(readResult)
            
            else:
                readResult = False
                args[0].setVal(readResult)

        elif argu == "int":

            if not re.search(r"^[-+]?\d+$", readString):
                readResult = "nil"
                readResult = nill(readResult)
                args[0].setVal(readResult)
            
            else:
                readResult = int(readString)
                args[0].setVal(readResult)

        elif argu == "string":
            if readString == "" and readFlag == 0:
                readResult = ""
                args[0].setVal(readResult)
    
            elif re.search(r"(?!\\[0-9]{3})[\s\\#]", readString) or readFlag == 1:
                readResult = "nil"
                readResult = nill(readResult)
                args[0].setVal(readResult)

            else:
                readResult = str(readString)
                args[0].setVal(readResult)

        else:
            readResult = "nil"
            readResult = nill(readResult)
            args[0].setVal(readResult)
      
    elif opcode == "WRITE":
        checkArgument(symb, args=args, countOfArgs=countOfArgs)
        firstArg = args[0]
        if type(firstArg) == varType:
            firstArg = args[0].getVal()
        
        if type(firstArg) == bool:

            if firstArg == True:
                firstArg = "true"
                writeResult = str(firstArg)
                print(writeResult, end = '')
            
            else: 
                firstArg = "false"
                writeResult = str(firstArg)
                print(writeResult, end = '')

        elif re.search(r"^<class \'__main__.nill\'>", str(type(firstArg))):
            firstArg = ""
            writeResult = str(firstArg)
            print(writeResult, end = '')

        else:
            writeResult = str(firstArg)
            print(writeResult, end = '')

    else:
        print("ERROR: Bad code instruction", file = sys.stderr)
        exit(32)
    
    
def sortXML(parent, attribute):
    """ Function for sorting instructions by attribute order """ 
    try:    
        parent[:] = sorted(parent, key = lambda child: int(child.get(attribute)))       
    except:
        print("ERROR: Bad <order> instruction", file = sys.stderr)
        exit(32)
    
    rootLen = len(root)
    for command in range(rootLen - 1):
        if int(root[command].attrib['order']) == int(root[command + 1].attrib['order']):
            print("ERROR: Bad <order> instruction", file = sys.stderr)
            exit(32)
        elif int(root[command].attrib['order']) <= 0:
            print("ERROR: Bad <order> instruction", file = sys.stderr)
            exit(32)
        

""" Main function """

pathToSourceFile, pathToInputFile = checkStartArguments()   # take path to file
inputArray = [] # array for input values

if pathToInputFile == sys.__stdin__:

    for line in fileinput.input(files=()):
        name = line.strip().split("\t")
        inputArray.append(name)

else: 
 
    for line in fileinput.input(files=(pathToInputFile)):
        name = line.strip().split("\t")
        inputArray.append(name)

try:
    tree = ET.ElementTree(file=pathToSourceFile)
except IOError:
    print("ERROR: Bad opening input file", file = sys.stderr)
    exit(11)
except ET.ParseError:
    print("ERROR: Can't find elements in file", file = sys.stderr)
    exit(31)

root = tree.getroot()                   # take root
Interpretator.isRootValid(root)         # control validation of root
Interpretator.loadingInstructions(root) # take instructions
exit(0)