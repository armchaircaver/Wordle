from wordlists import solutions, alloptions
#import wordle_solver
from time import perf_counter
from collections import defaultdict
from itertools import product
#from microdict import mdict

verbose=False

def setVerbose(x):
  verbose=x

print(len(solutions),"solutions, ",len(alloptions), "alloptions")
allpatterns = [ ''.join(x) for x in product('.GY',repeat=5) ]

highest_used_shortlist = 0 # the highest positioned item in shortlist

# estimate of number of guesses to complete, for a list of solutions
# of a certain size
estimate_to_complete = [x**1.1 - 1  for x in range(1000)]
estimate_to_complete[0:4]=[0, 0, 1, 2.55]
#print( estimate_to_complete[0:7])

#------------------------------------------------------------------------------------------------------------
patterncache = defaultdict(str)
#patterncache = mdict.create(dtype="str:str", key_len=10, val_len=5)  

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
      squaresum += estimate_to_complete[x] - estimate_to_complete[x-1]
      

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

def avg( distribution, cutoff ):
  #if verbose: print("avg:", [len(distribution[p]) for p in distribution])
  denominator = sum( len(distribution[p]) for p in distribution)
  numerator_cutoff = cutoff * denominator

  smallest_numerator=0.0

  for p in distribution:

    if p=='GGGGG':
      continue
    
    if len(distribution[p]) == 1:
      smallest_numerator += 1

    else : 
      smallest_numerator += 2 * len(distribution[p]) - 1

  if (smallest_numerator > numerator_cutoff ) :
      #stats.smallest_cutof_hits++;
      return smallest_numerator / denominator



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

    if numerator > numerator_cutoff :
      #if numerator - numerator_cutoff < 0.1:
      #  print(f"numerator = {numerator}, numerator_cutoff={numerator_cutoff}")
      #  print(distribution)
      break
    
  #if verbose: print("avg completed:", [len(distribution[p]) for p in distribution])
  # print( "average: ", numerator,"/", sum( len(distribution[p]) for p in distribution ) )
  return numerator/denominator    

#----------------------------------------------------------------------------
def minavg(solutions) :
    bg = bestguess(solutions);
    return bg[0];

#----------------------------------------------------------------------------
bestguess_cache=defaultdict(tuple)
bestguess_stats = defaultdict(list)

def bestguess(solutions, printProgress=False):
  # find the guess that produces the best average for the solutions
  # and return the pair (av, guess) where av is the average number
  # of subsequent guesses needed to complete if 'guess' is chosen next

  global highest_used_shortlist
  
  if len(solutions) == 1:
    if printProgress: print("no need to search")
    return (0.0, solutions[0])

  if len(solutions) == 2:
    if printProgress: print("no need to search")
    return (0.5, solutions[0])
  
  if tuple(solutions) in bestguess_cache:
    return bestguess_cache[tuple(solutions)]

  starttime = perf_counter()
  bestavg = 10.0**30
  bestguess = '?????'
  reserveguess = '?????'

  # first, consider guesses from words in the solution list
  if len(solutions) < 25:
    for guess in solutions:
      solsbypattern = defaultdict(list)

      for sol in solutions:
        p = pattern( sol, guess )
        solsbypattern[p].append(sol)
      
      if len(solsbypattern)==len(solutions):
        # can't do better than this
        bestguess_stats[len(solutions)].append((len(solutions)-1)/len(solutions))
        return ( (len(solutions)-1)/len(solutions), guess)
      
      if len(solsbypattern)==len(solutions)-1:
        reserveguess=guess

      a = avg( solsbypattern, bestavg )
      #print("solution word guess", guess, "average=",a)
      
      if a < bestavg:
        bestavg = a
        bestguess = guess


  if reserveguess != "?????":
    bestguess_stats[len(solutions)].append(1.0)
    return (1.0, reserveguess)
  
  sl = shortlist(30,solutions)
  sl_pos=0
  used_pos=0
  if printProgress: print("shortlist = ", [guess for (cost,guess,_) in sl])
  for (squaresum, guess, solsbypattern ) in sl:

    if len(solsbypattern)==len(solutions):
      # can't do better than this
      bestguess_stats[len(solutions)].append(1.0)
      return ( 1.0, guess)

         
    a = avg( solsbypattern, bestavg )

    if printProgress:
      if a < bestavg:
        print(f"'{guess}', average to complete: {a}")
      else:
        print(f"'{guess}' not as good as '{bestguess}'")
        


    if a < bestavg:
      bestavg = a
      bestguess = guess
      used_pos=sl_pos

    sl_pos+=1
    
  if verbose: print( "search: best average = ", bestavg)    

  if bestguess == '?????':
    raise Exception( "search: failed to find bestguess" )
    
  bestguess_cache[tuple(solutions)] = (bestavg, bestguess)
  
  if used_pos > highest_used_shortlist:
    print( f"highest shortlist position {used_pos}")
    print(f"bestguess={bestguess}")
    print(len(solutions),solutions)
    highest_used_shortlist = used_pos
     
  bestguess_stats[len(solutions)].append(bestavg)
  return (bestavg, bestguess)

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

