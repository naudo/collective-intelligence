

## 1
Tanimoto is useful for calculating similarities based on the
intersection (overlap) of 2 sets. 

The Tanimoto similarity score could be calculated like  so


````python
def tanimoto(l1, l2):
      intersection = [common for common in l1 if l1 in l2]
      interesection_len = len(intersection)
      coefficient = intersection_len / (len(l1) + len(l2) -
intersection_len)
      return float(coefficient)
````


## 2 

Can't do since the delicious api went bust
