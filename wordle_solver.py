from wordle_recursive import pattern, solutions, alloptions, allpatterns, bestguess
from time import perf_counter
from precalculated_patterns import patterndict

def patternmatch( patternlist, inputlist ):
  # patternlist is a comma separated list of patterns
  # e.g patternlist = 'GGY.Y, Y..G.'
  # of patterns from other people's posts of results.
  # The best patterns to use are those with fewest white squares
  patterns = set(( [x for x in patternlist.replace(' ','').split(',')] ))
  print("patterns:", patterns)
  if not(all( len(p)==5 for p in patterns)):
    print ( "patterns with invalid length:", [p for p in patterns if len(p) != 5])
    exit

  st = perf_counter()
  outputlist = [ w for w in inputlist if patterns <= patterndict[w] ]
  en = perf_counter()
  print(len(outputlist), "possible solutions after pattern matching, ",round(en-st,4),"sec")

  return outputlist
#----------------------------------------------------------------------------

def guessmatch( guesses, inputlist ):
  # guesses is a list of pairs of (guess,pattern)
  # e.g. guesses = [ ('abcde','Y....'), ('acdxx', 'Y....') ]
  st = perf_counter()
  outputlist = [ w for w in inputlist
                if all( pattern(w,guess)==p for (guess,p) in guesses)]
  en = perf_counter()
  #print(len(outputlist), "possible solutions after guess matching, ",round(en-st,4),"sec")
  #print( outputlist )
  return outputlist
#----------------------------------------------------------------------------

if __name__=="__main__":
  pmlist = patternmatch( 'GGG.., YGY.Y, GG.G., .G.YY,YGY..,.YYG., YG.GY', solutions)
  print ( pmlist )

  L2 = guessmatch([ ('saner','..GGY'), ], pmlist)
  print( L2 )
  
  g = bestguess(L2)
  print("best guess: ",g)
