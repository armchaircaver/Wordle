with open('solutions.txt') as f:
    lines = f.read().splitlines()
    _solutionlist = lines[0]

with open('guesses.txt') as g:
    linesg = g.read().splitlines()
    _sortedalloptionlist = linesg[0]

solutions = [s for s in _solutionlist.split(",")]
alloptions = [s for s in _sortedalloptionlist.split(",")] + solutions

    
if __name__=="__main__":
    print (len(solutions), len(alloptions) )
