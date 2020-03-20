import sys

print("Starting the Assembler")

# Simple Ways to figure out what I am looking at
def representsInt(myInt : int):
    try:
        int(myInt)
        return True
    except:
        return False
def representsHex(myInt: str):
    if(myInt.lower().startswith('0x')):
        myInt = myInt[2:]
        try:
            int(myInt, 16)
            return True
        except:
            raise ValueError
    else:
        return False

def representsBin(myInt: str):
    if(myInt.lower().startswith('0b')):
        myInt = myInt[2:]
        try:
            int(myInt, 2)
            return True
        except:
            raise ValueError
    else:
        return False

# Simple class to hold label data
class Label:
    def __init__(self, name = '', definition = '', lineNumber = 0):
        self.name = name
        self.definition = definition
        self.lineNumber = lineNumber
    
    def __eq__(self, other):
        if type(other) is str:
            return self.name == other
        else:
            return self.name == other.name

class Log:
    def __init__(self, fileName):
        self.filename = fileName + '.out'
    def log(self, string):
        print(string)
        f = open(self.filename, 'a')
        f.write(str(string) + '\n')



#Main Assembler
class hackAssembler:
    

    def __init__(self, logger):
        self.currentLineNumber = 0
        self.currentLabelNumber = 16
        # Holders for the label classes (Makes it easy to print)
        self.currentMemory = []
        self.RAMLabels = []
        self.ROMLabels = []
        self.EQULabels = []
        self.logger = logger

        # Dictionary to all the EQU symbold
        self.equLabelsDict = {

        }

        # All Labels that will change the assembly
        self.labels = {
            "SP"    : 0,
            "LCL"   : 1,
            "ARG"   : 2,
            "THIS"  : 3,
            "THAT"  : 4,
            "R0"    : 0,
            "R1"    : 1,
            "R2"    : 2,
            "R3"    : 3,
            "R4"    : 4,
            "R5"    : 5,
            "R6"    : 6,
            "R7"    : 7,
            "R8"    : 8,
            "R9"    : 9,
            "R10"   : 10,
            "R11"   : 11,
            "R12"   : 12,
            "R13"   : 13,
            "R14"   : 14,
            "R15"   : 15,
            "SCREEN": 16384,
            "KBD"   : 24576
        }

        # All Comparison Conversions
        self.compConversion = {
            "0"     : 0b0101010,
            "1"     : 0b0111111,
            "-1"    : 0b0111010,
            "D"     : 0b0001100,
            "A"     : 0b0110000,
            "!D"    : 0b0001101,
            "!A"    : 0b0110001,
            "~D"    : 0b0001111,
            "~A"    : 0b0110001,
            "D+1"   : 0b0011111,
            "A+1"   : 0b0110111,
            "D-1"   : 0b0001110,
            "A-1"   : 0b0110010,
            "D+A"   : 0b0000010,
            "D-A"   : 0b0010011,
            "A-D"   : 0b0000111,
            "D&A"   : 0b0000000,
            "D|A"   : 0b0010101,
            "M"     : 0b1110000,
            "!M"    : 0b1110001,
            "~M"    : 0b1110011,
            "M+1"   : 0b1110111,
            "M-1"   : 0b1110010,
            "D+M"   : 0b1000010,
            "D-M"   : 0b1010011,
            "M-D"   : 0b1000111,
            "D&M"   : 0b1000000,
            "D|M"   : 0b1010101,

            # Additional Types XHACK
            "!D&A"  : 0b0010000,
            "D&!A"  : 0b0000100,
            "!D&!A" : 0b0010100,
            "!(D&A)": 0b0000001,
            "!(!D&A)": 0b0010001,
            "!(D&!A)": 0b0000101,
            "!(!D&!A)": 0b0010101,

            "!D|A"  : 0b0000101,
            "D|!A"  : 0b0010001,
            "!D|!A" : 0b0000001,
            "!(D|A)": 0b0010100,
            "!(!D|A)": 0b0000100,
            "!(D|!A)": 0b0010000,
            "!(!D|!A)": 0b000000,

            "!D&M"  : 0b1010000,
            "D&!M"  : 0b1000100,
            "!D&!M" : 0b1010100,
            "!(D&M)": 0b1000001,
            "!(!D&M)": 0b1010001,
            "!(D&!M)": 0b1000101,
            "!(!D&!M)": 0b1010101,

            "!D|M"  : 0b1000101,
            "D|!M"  : 0b1010001,
            "!D|!M" : 0b1000001,
            "!(D|M)": 0b1010100,
            "!(!D|M)": 0b1000100,
            "!(D|!M)": 0b1010000,
            "!(!D|!M)": 0b100000
        }

        #All destination conversions
        self.destConversion = {
            None    : 0b000,
            "M"     : 0b001,
            "D"     : 0b010,
            "MD"    : 0b011,
            "A"     : 0b100,
            "AM"    : 0b101,
            "AD"    : 0b110,
            "AMD"   : 0b111
        }

        # All Jump Conversions
        self.jumpConversion = {
            None    : 0b000,
            "JGT"   : 0b001,
            "JEQ"   : 0b010,
            "JGE"   : 0b011,
            "JLT"   : 0b100,
            "JNE"   : 0b101,
            "JLE"   : 0b110,
            "JMP"   : 0b111

        }



    # Starts the entire assembler
    def assembler(self, currentFile: str):
        totalFile = ""
        inComment = False
        for index, currentLine in enumerate(currentFile):
            currentLine = currentLine.strip()
            if not inComment:
                commentStart = currentLine.find('/*')
                commentEnd = currentLine.find('*/')
                if(commentStart != -1):
                    if(commentEnd != -1):
                        inComment = True
                        continue
                    else:
                        currentLine = currentLine[:commentStart] + currentLine[commentEnd:]
            else:
                commentEnd = currentLine.find('*/')
                currentLine = currentLine[commentEnd:]
                inComment = False

            lineComment = currentLine.find('//')
            if(lineComment != -1):
                currentLine = currentLine[:lineComment]

            currentLine.strip()

            try: 
                if(len(currentLine)):
                    # Do Stuff Here
                    newLine = ''

                    if(self.equLabelsDict.get(currentLine) != None):
                        currentLine = self.equLabelsDict.get(currentLine)

                    if(len(currentLine) == 0 or currentLine.startswith("//") or currentLine.startswith('.EQU')):
                        newLine = None
                    
                    elif(currentLine.startswith('@') or currentLine.startswith('(')):
                        #Looking at an A Type
                        newLine = self.aType(index, currentLine)
                    else:
                        # We are looking at a c type instruction
                        newLine =  self.cType(index, currentLine)
                    if(newLine != None): # Must have been a comment or a blank line
                            totalFile += newLine + "\n"
            except Exception as ex:
                self.logger.log(ex.args)
                number, error, line = ex.args if (len(ex.args) == 3) else ex.args, None, None
                self.logger.log(f'ERROR - On line {number}\n{error}\n{line}')
        return totalFile
            
    def aType(self, lineNumber, line : str):
        AInst = line.strip('@')
        AInst = AInst.strip()
        if AInst.startswith('('):
            return None
        if(len(AInst) == 0): # Make sure we are not looking at a blank line
            raise Exception(lineNumber, "A-Type Illegal Value: Not a Number", line)

        # Figure out what Kinda number or text we are looking at
        try:
            if(representsInt(AInst) or representsHex(AInst) or representsBin(AInst)):
                location = 0
                if(representsInt(AInst)):
                    location = int(AInst)
                elif(representsHex(AInst)):
                    location = int(AInst[2:], 16)
                else:
                    location = int(AInst[2:], 2)
                if(location < 0):
                    raise Exception(lineNumber, "A-Type Illegal Value: Number cannot be Negative", line)
                if(location > 0b111111111111111):
                    raise Exception(lineNumber, "A-Type Illegal Value: Number is larger than a 15 bit number", line)
                location &= ~(1 << 15)
                locationText = bin(location)[2:].zfill(16)  # Convert to binary text
                return locationText
            else:
                if(self.labels.get(AInst) is not None):     # If we already have the label, say it 
                    return bin(self.labels.get(AInst))[2:].zfill(16)
                else:
                    raise Exception(lineNumber, "A-Type No Value", line)
        except ValueError:
            raise Exception(lineNumber, "Value is not a number", line)

    def xType(self, lineNumber, line:str):
        if(representsHex('0'+ line)): # Make sure it is hex and convert it to an int
            command = int(line[1:], 16)
            if(command > 127):
                raise Exception(lineNumber, "x Type Instruction is greater than the number of commands", line)
            return command  # Convert to binary string
        else:
            raise Exception(lineNumber, "X Type Instuction is not Hexadecimal", line)

    def cType(self, lineNumber, line : str):
        cDefinition = 0xe000    # Base C Type Intruction

        # Find All the different Parts
        destText = line.split('=')[0].strip() if '=' in line else None
        jumpText = line.split(';')[1].strip() if ';' in line else None
        destIndex = line.find('=')
        jumpIndex = line.find(';')
        compText = line[destIndex + 1 if destIndex != -1 else 0 : jumpIndex if jumpIndex != -1 else len(line)].strip()

        comp = int()
        if(compText.lower().startswith('x')):
            comp = self.xType(lineNumber, compText)
        else:
            comp = self.compConversion.get(compText)

        # Convert Text to int
        
        if(comp is None):
            raise Exception(lineNumber, "Illegal C-Type computation: Not a valid Computation Mnemonic", line)
        dest = self.destConversion.get(destText)
        if(dest is None and destText is not None):
            raise Exception(lineNumber, "Illegal C-Type computation: Not a valid Destination Mnemonic", line)
        jump = self.jumpConversion.get(jumpText)
        if(jump is None and jumpText is not None):
            raise Exception(lineNumber, "Illegal C-Type computation: Not a valid Jump Mnemonic", line)

        # Or with the base C Type and convert to binary
        intLine = cDefinition
        intLine |= (int(comp) << 6)
        intLine |= (int(dest) << 3)
        intLine |= (int(jump) << 0)
        intLine = bin(intLine)[2:].zfill(16)
        return intLine
    
    def validInstruction(self, currentLine: str): # ONLY CHECKS IF IT IS SOMEWHAT FORMATTED CORRECTLY
        if(currentLine.startswith('@')):
            return True
        
        if(len(currentLine.strip()) < 1):
            return False
        
        if(currentLine.startswith('//')):
            return False
        
        if(currentLine.find('=') != -1 or currentLine.find(';') != -1):
            return True
        elif(currentLine.startswith('X')):
            return True
        return False
    
    def getLabels(self, currentFile):
        # Does the first run through to find all the labels. Adds them to their respective buckets
        for key in self.labels: # Adds the inital ones as well
            self.RAMLabels.append(Label(key, self.labels.get(key), -1))
        inComment = False
        for lineNumber, currentLine in enumerate(currentFile):
            try: 
                currentLine = currentLine.strip()
                if not inComment:
                    commentStart = currentLine.find('/*')
                    commentEnd = currentLine.find('*/')
                    if(commentStart != -1):
                        if(commentEnd != -1):
                            currentLine = currentLine[:commentStart] + currentLine[commentEnd+2:]
                        else:  
                            inComment = True
                            continue
                else:
                    commentEnd = currentLine.find('*/')
                    currentLine = currentLine[commentEnd:]
                    inComment = False
                currentLine.strip()

                label = currentLine.strip('@')
                label = label.strip()
                if(len(label) == 0 and currentLine.startswith('@')):
                    raise Exception(lineNumber, "Illegal Label: Label cannot be blank", currentLine)

                try:
                    if(currentLine.startswith('@') and not (representsInt(label) or representsHex(label) or representsBin(label))):
                        newLabel = Label(label, 0, lineNumber)
                        if(self.labels.get(label) == None and (newLabel not in self.currentMemory)):
                            self.currentMemory.append(newLabel)

                    elif(currentLine.startswith('(')):
                        label = currentLine.strip("(")
                        label = label.replace(")", "")
                        label = label.strip()
                        if(label in self.currentMemory):
                            self.currentMemory.remove(label)
                        if(self.labels.get(label) != None):
                            raise Exception(lineNumber, "Illegal Label Redefinition", currentLine)
                        self.labels[label] = self.currentLineNumber
                        self.ROMLabels.append(Label(label, self.currentLineNumber, lineNumber))

                    elif(currentLine.startswith('.EQU ')):
                        try:
                            splitLine = currentLine.split(' ')
                            self.EQULabels.append(Label(splitLine[1], splitLine[2], lineNumber))
                            self.equLabelsDict[splitLine[1]] = splitLine[2]
                        except:
                            raise Exception(lineNumber, "Illegal EQU: EQU not formatted Correctly", currentLine)
                    if(self.validInstruction(currentLine) == True):
                        self.currentLineNumber += 1

                except ValueError:
                    raise Exception(lineNumber, "Value is not a number", currentLine)
            except Exception as ex:
                self.logger.log(ex.args)
                number, error, line = ex.args if len(ex.args) == 3 else (ex.args[0], None, None)
                self.logger.log(f'ERROR - On line {number}\n{error}\n{line}')

        for items in self.currentMemory:
            self.labels[items.name] = self.currentLabelNumber
            items.definition = self.currentLabelNumber
            self.RAMLabels.append(items)
            self.currentLabelNumber += 1

if(len(sys.argv) < 2):
    print("Must include at least 1 input file")
    sys.exit()


for filePath in sys.argv[1:]:
    fileName = filePath.split(".")[0]
    logger = Log(fileName)
    assembler = hackAssembler(logger)
    file = open(filePath)

    if(file.mode != 'r'):
        continue

    currentFile = file.readlines()
    # Read labels
    assembler.getLabels(currentFile)
    # Compile Program
    totalFile = assembler.assembler(currentFile)

    newFileName = fileName+ ".hack"
    newFile = open(newFileName, "w")
    newFile.write(totalFile)
    newFile.close()
    logger.log(f'Outputed to -> {newFileName}')

    tableFile = ''
    tableFile += ('Symbolic Table Time!\nRAM Addresses:\n')
    
    tableFile += ('|Name\t|Value\t|Line Num\t|\n')
    for item in assembler.RAMLabels:
        tableFile += (f'|{item.name.ljust(30)}|{str(item.definition).ljust(10)}|{str(item.lineNumber).ljust(10)}|\n')

    tableFile += ('ROM Addresses:\n')
    tableFile += ('|Name\t|Value\t|Line Num\t|\n')
    for item in assembler.ROMLabels:
        tableFile += (f'|{item.name.ljust(30)}|{str(item.definition).ljust(10)}|{str(item.lineNumber).ljust(10)}|\n')
    
    tableFile += ('EQU Values:\n')
    tableFile += ('|Name\t|Value\t|Line Num\t|\n')
    for item in assembler.EQULabels:
        tableFile += (f'|{item.name.ljust(30)}|{str(item.definition).ljust(10)}|{str(item.lineNumber).ljust(10)}|\n')

    tableFileName = newFileName + 'table.txt'
    newTableFile = open(tableFileName, 'w')
    newTableFile.write(tableFile)
    newTableFile.close()
    logger.log(tableFile)
    logger.log(f'Also Written To -> {tableFileName}')

    
    
    
            