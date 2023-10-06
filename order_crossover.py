# -*- coding: utf-8 -*-
"""Order_crossOver.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-jV8X4Lm7uR8XuliiVns_lCpw4XjQTrQ
"""

def order_cross_over(ind1, ind2):
    child1 = [0]*len(ind1)
    child2 = [0] *len(ind2)

    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    print("CutPoint1 ",cxpoint1)
    print("CutPoint2 ", cxpoint2)
    backup = cxpoint1
    part1 = ind1[cxpoint1:cxpoint2+1] #slice data 1
    part2 = ind2[cxpoint1:cxpoint2+1] #slice data 2

    i=0
    while(cxpoint1<cxpoint2):
        child1[cxpoint1]=part1[i]
        cxpoint1+=1
        i+=1
    i=0
    cxpoint1 = backup

    while(cxpoint1<cxpoint2):
        child2[cxpoint1]=part2[i]
        cxpoint1+=1
        i+=1

    print(child1)
    print(child2)