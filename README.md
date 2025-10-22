# Nonogram-SAT

## Poznámky
VELKE TODO: najit lepsi způsob na encoding než najít DNF a prehodit 

jazyk: vsechna policka

1. sloupec:
```
3
big or 0...n-3
    p_i and p_{i+1} and p_{i+2}
    
potom DNF do CNF 
a and přes všechny sloupce a řádky
```

1. řádek:
```
2 2
big or 0...n-(2 + 1 + 2)
    p_i and p_{i+1} and (
        big or i+2...n-2
            p_j and p_{j+1}
```


## Small nonogram

![Small nonogram](./src/small_nonogram.PNG)

### Encoding
```
10
3
2 1
1 1 5
1 8
2 6
3 4
2 6
1 8
1 1 5
2 3
2 2
1 1 1 1
1 5 1
2 1 2
5 
3 3
1 8
1 8
1 8
8
```