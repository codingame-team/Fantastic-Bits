[Tuto Bob](https://www.codingame.com/blog/lazy-keep-simple/?utm_source=codingame&utm_medium=details-page&utm_campaign=cg-blog&utm_content=fantastic-bits)

[Markdown syntax](https://www.ionos.fr/digitalguide/sites-internet/developpement-web/markdown/)

|Strategy #|Wood 2|Wood 1|Bronze|Silver|Gold|Legend|
|-|-|-|-|-|-|-|
|1|1/267|1/423|8/481|x|x|x|
|2|x|x|x|x|x|x|

1. move to Bronze

```
for each player

done = false

if player has a snaffle
       throw to center of goal at max power
       done = true
       
if not done
       find snaffle closest to player
       move to the snaffle’s predicted position at max thrus
```

2. move to Silver

``` new rules:
(Wood 1) De nouvelles entités sont disponibles : les bludgers rentrent en jeu !
(Bronze) Les sorciers peuvent désormais utiliser de la magie pour lancer des sorts.
```

````
for each player

   done = false

   if player has a snaffle

       throw to center of goal at max power

       done = true

   if not done and mana >= 20 and player did not accio in the past 6 turns

       accio snaffle closest to “matching” opponent (0<->2, 1<->3)

       mana -= 20

       done = true

   if not done

       find snaffle closest to player

       move to the snaffle’s position at max thrust
```

3. move to Bronze
