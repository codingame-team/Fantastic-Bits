[Tuto Bob](https://www.codingame.com/blog/lazy-keep-simple/?utm_source=codingame&utm_medium=details-page&utm_campaign=cg-blog&utm_content=fantastic-bits)

[Markdown syntax](https://www.ionos.fr/digitalguide/sites-internet/developpement-web/markdown/)

|Strategy #|Wood 2|Wood 1|Bronze|Silver|Gold|Legend|
|-|-|-|-|-|-|-|
|1|1/267|1/423|8/481|x|x|x|
|2|1/267|1/423|1/481|305/951|x|x|

1. move to Bronze

```
for each player

done = false

if player has a snaffle
       throw to center of goal at max power
       done = true
       
if not done
       find snaffle closest to player
       move to the snaffle’s position at max thrust (predicted position on next turn)
```

2. move to Silver

``` new rules:
(Wood 1) De nouvelles entités sont disponibles : les bludgers rentrent en jeu !
(Bronze) Les sorciers peuvent désormais utiliser de la magie pour lancer des sorts.
```

```
for each player
   done = false
   if player has a snaffle
       throw to center of goal at max power
       done = true
   if not done and mana >= 15 and player did not accio in the past 6 turns
       accio snaffle closest to “matching” opponent (0<->2, 1<->3)
       mana -= 15
       done = true
   if not done
       find snaffle closest to player
       move to the snaffle’s position at max thrust
```

3. move to Gold

```
for each player
   done = false
   [ throw code ]
   if not done and mana >= 20 and player did not flipendo in the past 3 turns
       for each snaffle (ordered by increasing distance from player)
           if snaffle is not between player and goal
              continue
           compute line between player and snaffle
           if line intersects the goal line between the posts
               flipendo snaffle
               mana -= 20
               done = true
               break
   [ new accio code ]
   [ move code ]
```
