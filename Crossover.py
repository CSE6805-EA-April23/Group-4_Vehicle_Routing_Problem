
import random
def cx_partially_matched(ind1, ind2):

    child1 = [0]*len(ind1)
    child2 = [0] *len(ind2)
    # print(child1)
    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    # print("CutPoint1 ",cxpoint1) #0
    # print("CutPoint2 ", cxpoint2)
    backup = cxpoint1
    part1 = ind1[cxpoint1:cxpoint2+1] #slice data 1
    part2 = ind2[cxpoint1:cxpoint2+1] #slice data 2
    rule1to2 = list(zip(part1, part2))
    i=0
    while(cxpoint1<cxpoint2):
        child1[cxpoint1]=part2[i]
        cxpoint1+=1 # 6
        i+=1
    i=0
    cxpoint1 = backup

    while(cxpoint1<cxpoint2):
        child2[cxpoint1]=part1[i]
        cxpoint1+=1
        i+=1
    i=0


    for t1,t2 in rule1to2:
        print(f't1 {t1} t2 {t2}')


    print("before cross ",child1)
    while i<len(child1):
        
        if(child1[i]==0):
            if(ind1[i] not in child1):
                child1[i]= ind1[i]
            else:    
                for t1,t2 in rule1to2:
                    if (t1==child1[i]):
                        if(t2 not in child1):
                            print("fairuz bolse 0 ", t2)
                            child1[i] = t2
                        else:
                            t1 =t2
        i+=1
        
        
    # print(rule1to2)
    print("CROSS ",child1)
    # print(child2)
        
    
    # print (part1)
    # print (part2)
    # print ("zip ",rule1to2)
    return ind1, ind2


def order_cross_over(ind1, ind2):
    child1 = [0]*len(ind1)
    child2 = [0] *len(ind2)
    # print(child1)
    cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
    # print("CutPoint1 ",cxpoint1) #0
    # print("CutPoint2 ", cxpoint2)
    backup = cxpoint1
    part1 = ind1[cxpoint1:cxpoint2+1] #slice data 1
    part2 = ind2[cxpoint1:cxpoint2+1] #slice data 2

    i=0
    while(cxpoint1<cxpoint2):
        child1[cxpoint1]=part1[i]
        cxpoint1+=1 # 6
        i+=1
    i=0
    cxpoint1 = backup

    while(cxpoint1<cxpoint2):
        child2[cxpoint1]=part2[i]
        cxpoint1+=1
        i+=1

    print(child1)
    print(child2)







order_cross_over([1,2,9,4,5,6,7,8,3],[3,9,4,7,6,5,2,1,8])







