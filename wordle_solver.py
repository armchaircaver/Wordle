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
  #print(len(outputlist), "possible solutions after pattern matching, ",round(en-st,4),"sec")

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

  inputdata =  b"""
salet ...G.
YY.G.
"""
  
  blines = inputdata.split(b'\n')

  W = solutions[:]
  
  for bline in blines:
    line = bline.decode("utf-8")
    print("\n",line)
    
    if len(line)==0:
      continue
    
    words = line.split()
    if len(words)==1:
      # assume it is a pattern
      W = patternmatch( words[0], W)
      print( len(W), "words")
      if len(W)<150:
        print(W)
    else:
      # assume a word and a pattern
      W = guessmatch( [ (words[0],words[1]), ], W )
      print( len(W), "words")
      if len(W)<150:
        print(W)
  # special matching
  
  """
  W = [w for w in W
       if len([ x for x in alloptions if x[0]+x[2]+x[3]+x[4] == w[0]+w[2]+w[3]+w[4] ]) > 4]
  print( "special matching", len(W), "words")
  if len(W)<150:
    print(W)
  W = [w for w in W
       if len([ x for x in alloptions
                if x[1]+x[2]+x[0] == w[1]+w[2]+w[0]]) > 3]
  print( "special matching", len(W), "words")
  if len(W)<150:
    print(W)
  """

  g = bestguess(W, printProgress=True)
  print("\nbest guess: ",g)  
     
