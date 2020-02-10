### ABOUT
Virtual Memory (VM) manager simulation.
VM manager initializes the Physical Memory (PM) from an input file consisting of 2 lines
- Line 1 contains triples of integers, which define the contents of the ST
- Line 2 contains triples of integers, which define the contents of the PTs

The VM then reads Virtual Address (VA) and translates to Physical Address

VM assumes the PM will always have sufficient free frames for demand paging

## HOW TO RUN:
    Before running all necessary input files must be added to the same folder as PM.py
### INPUTS:
    The default file names:
         - "init-dp.txt"
         - "input-dp.txt"
         - "init-no-dp.txt"
         - "input-no-dp.txt"
    If there is a name change in the files, it must be updated in the global variables:
        - inputFile
        - initFile

## Command line:
    python ./PM.py {-n}

#### optional: 
    -n  -> option to run program using no-dp files and produce "output-no-dp.txt"
#### Default output: 
    output-dp.txt
