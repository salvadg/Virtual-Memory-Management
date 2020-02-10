## Author: Salvadjg 
import numpy as np
import sys


if len(sys.argv) > 1 and sys.argv[1] == "-n":
    outFile  = "output-no-dp.txt"
    initFile = "init-no-dp.txt"
    inputFile = "input-no-dp.txt"
else:
    outFile  = "output-dp.txt"
    initFile = "init-dp.txt"
    inputFile = "input-dp.txt"

class PM:
    def __init__(self, *args, **kwargs):
        self.size = 1024*512 ## 1024 frames & 512 words each
        self.pm = [0] * self.size
        self.bitmap = [False] * 1024
        self.D = 1024*[512*[0]]
        self.quit = 0

    def read_block(self, b, m):
        for i in range(0, 512):
            self.pm[m + i ] = self.D[b][i]

    def initialize(self, line1, line2):
        l1 = iter(line1)
        self.bitmap[0] = True
        self.bitmap[1] = True
        for val in l1: ## Handle Line 1 (PT)
            s = val
            p = next(l1)
            f = next(l1) 
            
            self.pm[ val * 2 ] = p
            self.pm[2*s+1] = f

            if f > 0:
                self.bitmap[f] = True

        ### Handle Line 2 (Page)
        l2 = iter(line2)
        for val in l2: 
            s = val
            p = next(l2)
            f = next(l2)
    
            if self.pm[2*s+1] < 0:
                x = abs(self.pm[2*s+1])
                self.D[x][p] = f
                self.bitmap[f] = True

            else:
                self.bitmap[f] = True
            self.pm[ self.pm[s*2+1] * 512 + p ] = f
            
            
    def translate_VA(self,va_line):
        global outFile
        f = -1
        with open(outFile, mode = 'w') as outFile:
            for VA in va_line:
                s = VA >> 18 ##8
                w = VA & 0x1FF ##10
                p = (VA >> 9) & 0x1FF ## 1
                pw = VA & 0x3FFFF #522
         
                if pw < self.pm[2*s]:
                    if self.pm[2*s+1] < 0: ## PT not resident
                        ## find free frame:
                        for i,v in enumerate(self.bitmap):
                            if v == False:
                                f = i
                                self.bitmap[i] = True
                                break
                        self.read_block( abs(self.pm[2*s+1]), f*512 )
                        ## update ST
                        self.pm[2*s+1] = f

                    ## page fault: page is not resident 
                    if self.pm[ self.pm[2*s+1] * 512 + p ] < 0:
                        ## find free frame:
                        for i,v in enumerate(self.bitmap):

                            if v == False:
                                f = i
                                self.bitmap[i] = True
                                break
                        self.read_block( abs(self.pm[2*s+1]), f*512 )

                        ## update PT
                        self.pm[ self.pm[2*s+1] * 512 + p] = f

                      
                    outFile.write("{} ".format( self.pm[self.pm[2*s + 1] * 512 + p] * 512 + w ) )
                else:
                    outFile.write("-1 ")
                    
def handleInput(fileName):
    data = []
    with open(fileName, mode = 'r') as file:
        _lines = list(line for line in (l.strip() for l in file) if line)
        for lines in _lines:
            line = lines.split()
            data.append( list(map(int, line)) )
    return data

def main():
    global initFile
    global inputFile
    data = handleInput(initFile)
    VA = handleInput(inputFile)
    p = PM()
    p.initialize(data[0], data[1])   
    p.translate_VA(VA[0])
    
       
if __name__ == "__main__":
    main()


