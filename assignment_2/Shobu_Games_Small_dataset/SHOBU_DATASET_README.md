Shobu Game Dataset
------------------

This dataset consists of 104,396 randomly played games of Shobu (https://www.smirkandlaughter.com/shobu). The dataset was created using a Shobu game engine and random-move-making AI, both of which were written by Brandon S. Foltz. 

The data is organized in to two sub-folders:

**white** : Game files in which the white player was the winner.

**black** : Game files in which the black player was the winner.

This dataset was generated using the Shobu AI Playground, which you can find here: https://github.com/JayWalker512/Shobu

What's Shobu?
-------------

Shobu is a two-player board game by Smirk and Laughter: https://www.smirkandlaughter.com/shobu

You can find a link to a PDF of the game rules on that page.

What do the files look like?
----------------------------

The Shobu game engine outputs a JSON representation of the entire game that was played when it ends. 
The format of this game output is like so (abbreviated repeating structures with ellipses): 

```json
{
   "winner" : "BLACK",
   "turns" : [
      {
         "passive" : {
            "origin" : {
               "x" : 1,
               "y" : 7
            },
            "heading" : {
               "x" : 1,
               "y" : -1
            }
         },
         "aggressive" : {
            "origin" : {
               "x" : 6,
               "y" : 7
            },
            "heading" : {
               "x" : 1,
               "y" : -1
            }
         }
      },
      ...
      {
         "passive" : {
            "origin" : {
               "y" : 6,
               "x" : 2
            },
            "heading" : {
               "y" : -1,
               "x" : -1
            }
         },
         "aggressive" : {
            "origin" : {
               "y" : 5,
               "x" : 5
            },
            "heading" : {
               "x" : -1,
               "y" : -1
            }
         }
      }
   ],
   "game_states" : [
      {
         "turn" : "BLACK",
         "board" : "oooooooo................xxxxxxxxoooooooo................xxxxxxxx",
         "turnNumber" : 0
      },
      ...
      {
        "turn" : "BLACK",
         "board" : "o.....ooo.o.o.....o.....xxxx.ox...o.o.....x..x...xx...x......x..",
         "turnNumber" : 58
      }
   ]
}

```

License
-------

This dataset was created by Brandon S. Foltz in the Spring of 2020.

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.