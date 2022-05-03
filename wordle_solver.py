from wordle_recursive import pattern, solutions, alloptions, allpatterns, bestguess
from time import perf_counter
#from precalculated_patterns import patterndict
from precalculated_pattern_counts  import patterncountdict

def patterncountmatch( pattern, count, inputlist ):
  if len(pattern) != 5:
    print ( "pattern with invalid length:", pattern)
    exit

  outputlist = [ w for w in inputlist
                 if pattern in patterncountdict[w]
                 and patterncountdict[w][pattern] >= count ]

  return outputlist
#----------------------------------------------------------------------------
def patternmatch( pattern, inputlist ):
  if len(pattern) != 5:
    print ( "pattern with invalid length:", pattern)
    exit

  outputlist = [ w for w in inputlist if pattern in patterncountdict[w] ]

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
YY.GY
G.GGY
GGGG. 2
YYY..
GGG..
apert ...GY
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
      print( len(W), f"words with pattern '{words[0]}'")
      if len(W)<150:
        print(W)
    else:
      if words[0] in alloptions:
        # assume a guess word and a pattern
        W = guessmatch( [ (words[0],words[1]), ], W )
        print( len(W),  f"words")
        if len(W)<150:
          print(W)
      else:
        # assume a pattern and a number of occurences
        W = patterncountmatch( words[0], int(words[1]), W)
        print( len(W), f"words with pattern '{words[0]}' occuring {words[1]} times")
        if len(W)<150:
          print(W)
        
 

  g = bestguess(W, printProgress=True)
  print("\nbest guess: ",g)  
     
