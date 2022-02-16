A helper to suggest the next word to enter into worde, based on the green, yellow and grey letters found so far. 

The search algorithm examines each word W from the thousands allowed, calculating the viable solution word that would maximise the number of viable solutions still available if word W were entered next.

The word that minimises that maximum is the one recommended by the algorithm.

Using the information (green, yellow, grey) from the first word entered into Wordle, the algorithm typically takes 3 or 4 seconds on a laptop to choose a recommended next word. The run time reduces significantly as information from more words becomes available. 

The best version is wordle_yellowpos.py, which improves on the previous program, wordle_minimax_bitmap.py,  by using the position of yellow letters as well as their existence.
