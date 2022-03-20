from wordlists import solutionlist
from wordle_recursive import bestguess,setVerbose, pattern, allpatterns, clearcaches
from time import perf_counter
from collections import defaultdict


setVerbose(False)
solutions = [s for s in solutionlist.split(",")]

def BGY(p):
  return p.replace('.','B')

#-----------------------------------------------------------------------------------  

totalsolsfound = 0
totalguesses = 0
lastpatternprinted = '?????'

#-----------------------------------------------------------------------------------  
def traverse(depth, startguess, inputlist):
  global totalsolsfound ,totalguesses, lastpatternprinted
 
  pg = defaultdict(list)
  for w in inputlist:
    pg[ pattern(w,startguess) ].append(w)


  print(" "+startguess, end=' ', flush=True)
  for p in sorted(pg):

    if depth==1:
      clearcaches()
      
    if lastpatternprinted =='GGGGG':
      print(" "*(13*(depth-1)+6) + BGY(p)+str(depth),end='' if p !='GGGGG' else'\n', flush=True)
    else:  
      print(BGY(p)+str(depth),end='' if p !='GGGGG' else'\n', flush=True)
    lastpatternprinted=p
    
     
    if  p=='GGGGG':
      totalsolsfound +=1 
      totalguesses += depth
    else:  
      g2 = bestguess( pg[p] )
      traverse(depth+1,  g2, pg[p] )
    
traverse(1, 'salet', solutions )

print("total solutions found", totalsolsfound)
print("total guesses ", totalguesses)
print("average = ", totalguesses/totalsolsfound)


