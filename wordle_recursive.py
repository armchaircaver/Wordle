from wordlists import solutionlist, sortedalloptionlist
#import wordle_solver
from time import perf_counter
from collections import defaultdict
from itertools import product

verbose=False

def setVerbose(x):
  verbose=x

solutions = [s for s in solutionlist.split(",")]
alloptions = [s for s in sortedalloptionlist.split(",")]
allpatterns = [ ''.join(x) for x in product('.GY',repeat=5) ]

SHORTLEN = 15 # length of shortlist

# pre calculate powers of integers
powers = [x**1.1 for x in range(1000)]

#------------------------------------------------------------------------------------------------------------
def reset():
  global solutions
  solutions = [s for s in solutionlist.split(",")]

#------------------------------------------------------------------------------------------------------------
patterncache = defaultdict(str)
def pattern(solutionword : str, guess :str ) -> str:

  if solutionword+guess in patterncache:
    return patterncache[solutionword+guess]
  
  list_solutionword = list(solutionword)
  p = ['.']*5

  # find greens first, and remove the letter from the solution
  # so that we don't get false yellows for a repeated letter in the guess word
  for i,g in enumerate(guess):
    if solutionword[i] == g:
      p[i] = 'G'
      list_solutionword[i]='.'
  
  # find yellows, removing a matched letter from the solution
  # so that we don't get further false yellows for a repeated letter in the guess word
  for i,g in enumerate(guess):
    if g in list_solutionword:
      if p[i] != 'G':
          p[i] = 'Y'
          list_solutionword[list_solutionword.index(g)]='.'

  result = ''.join(p)
  patterncache[solutionword+guess] = result
  return result    

def clearcaches():
  global patterncache, minavg_cache
  patterncache.clear()
  minavg_cache.clear()
#----------------------------------------------------------------------------
def shortlist(n, solutions):

  # returns a list of triples (squaresum, guess, solsbypattern )
  # solsbypattern is a dictionary keyed on pattern, with a list of solutions matching each pattern

  # the list returned is the list for guesses with the smallest squaresum

 
  slist = []
  assert len(solutions) > 2  
  starttime = perf_counter()
  letters = usefulletters(solutions)
  
  for guess in alloptions:
    
    #if len(letters.intersection(set(guess)))<1:
    #  continue
    
    squaresum = 0 
    solsbypattern = defaultdict(list)
    totalsbypattern = defaultdict(int)

    for sol in solutions:
      p = pattern( sol, guess )
      solsbypattern[p].append(sol)
      totalsbypattern[p] += 1

      # accumulate the sum of squares of totals for each pattern
      # incrementing the sum of squares: x**2 - (x-1)**2 = 2*x-1
      # squaresum += 2*totalsbypattern[p] - 1

      # this seems to produce a better shortlist
      x = totalsbypattern[p]
      squaresum += powers[x] - powers[x-1]
      

      if len(slist) == n and squaresum > slist[-1][0]:
        break

    if squaresum == len(solutions) and guess in solutions:
      # we have found a guess that distributes each solution
      # in a different pattern
      # and one of the solutions is a guess
      #if verbose: print("shortlist:", guess, "distributes all solutions in different patterns")
      return [ (squaresum, guess, solsbypattern) ]
    
    if len(slist) < n or squaresum < slist[-1][0]:
      #if verbose: print( guess, round(squaresum/len(solutions),2) )
      slist.append( (squaresum, guess, solsbypattern ) )
      slist.sort()
      if len(slist) > n:
        slist.pop()

  return slist
#----------------------------------------------------------------------------

def avg( distribution ):
  #if verbose: print("avg:", [len(distribution[p]) for p in distribution])
  numerator = 0
  for p in distribution:

    if p=='GGGGG':
      continue
    
    if len(distribution[p]) == 1:
      numerator += 1

    elif  len(distribution[p]) == 2:
      numerator += 3

    else:
      #if verbose: print("avg calling minavg:", distribution[p])
      numerator += (minavg(distribution[p]) + 1)*len(distribution[p])

  #if verbose: print("avg completed:", [len(distribution[p]) for p in distribution])
  return numerator/sum( len(distribution[p]) for p in distribution )    

#----------------------------------------------------------------------------
minavg_cache=defaultdict(str)

def minavg(solutions):
  if tuple(solutions) in minavg_cache:
    return minavg_cache[tuple(solutions)]
  
  if verbose: print("minavg : ", solutions)
  m = 1<<31

  slist = shortlist(SHORTLEN, solutions)
  
  for (squaresum, guess, solsbypattern ) in slist:
    #if verbose: print("minavg calling avg:", solsbypattern)
    a = avg( solsbypattern )
    if a < m:
      m = a
  minavg_cache[tuple(solutions)] = m    
  return m     
#----------------------------------------------------------------------------
def bestguess(solutions):
  # find the guess that produces the best average for the solutions
  
  if len(solutions) <= 2:
    if verbose: print("no need to search")
    return solutions[0]
  
  starttime = perf_counter()
  bestavg = 10.0**30
  bestguess = '?????'

  # first, consider guesses from words in the solution list
  if len(solutions) < 25:
    for guess in solutions:
      solsbypattern = defaultdict(list)

      for sol in solutions:
        p = pattern( sol, guess )
        solsbypattern[p].append(sol)
      
      if len(solsbypattern)==len(solutions):
        # can't do better than this
        return guess
      
      a = avg( solsbypattern )
      if a < bestavg:
        bestavg = a
        bestguess = guess

    
  sl = shortlist(SHORTLEN,solutions)
  if verbose: print("shortlist = ", sorted([guess for (_,guess,_) in sl]))
  for (squaresum, guess, solsbypattern ) in sl:

    if len(solsbypattern)==len(solutions):
      # can't do better than this
      return guess

    a = avg( solsbypattern )
    if a < bestavg:
      bestavg = a
      bestguess = guess

  if verbose: print( "search: best average = ", bestavg)    

  if bestguess == '?????':
    raise Exception( "search: failed to find bestguess" )
    
  return bestguess

#-------------------------------------------------------------------------------------------------------
def usefulletters(solutions):
  #find guess words with at least one of the letters in a list of solutions
  # that isn't a letter in all the solutions

  letters = set.union( *[set(x) for x in solutions] )
  #print("letters : ", sorted(letters) )

  common = set.intersection( *[set(x) for x in solutions] )
  #print("common letters : ", sorted(common) )

  notcommon = letters - common
  if verbose: print("useful letters:", notcommon)
  return notcommon

#-----------------------------------------------------------------------------------  

