https://www.codingame.com/ide/puzzle/fantastic-bits

https://stackoverflow.com/questions/64025633/scipy-linear-sum-assignment-show-the-workings

2 options:
  - (Bronze 360/408) Munkres:
      Description sommaire du problème hongrois:
        https://www.developpez.net/forums/blogs/283256-f-leb/b17/python-problemes-daffectation-methode-hongroise/
      
      Implementation choice in this challenge:
      
      - First, we build a 2d matrix representing distances between each wizard and each snaffle
      
              distances---s1------s2-----s3------s4-------s5------s6------s7
      
              wiz_1-------50------70-----100-----120------80------150-----200
      
              wiz_2-------130-----20------5------179------20------30------40
      
      - Second, we create a dictionary to create an association from each wizard to a distinct snaffle describing the cost matrix in term of distance/duration of moves:
      
          `costs[(0, i), (1, j)] = matrix[0][i] + matrix[1][j] (i, j going from 1 to snaffles_count and i != j)
          `
      
      - Third, we choose the best combination to optimize global team effort (extracts the dictionary key (tuple) of minimum cost value)
      
          `best_combination = min(costs)`
      
          `i, j = best_combination[0][1], best_combination[1][1]`
      
      - Finally, we extract the snaffle target for each wizard:
      
          `wiz_1.target, wiz_2.target = snaffles[i], snaffles[j]`
  
  - (Bronze 243/418) Avec algorithme linéaire (module scipy.optimise.linear_sum_assignment):
      https://perso.ens-lyon.fr/ruben.staub/vrac/bash_tricks/trick_18.php


Replays:
- Ligue Bois 2: https://www.codingame.com/replay/496545129
- Ligue Bois 1 (with bludgers): https://www.codingame.com/share-replay/496563891
