costs =["array dei costi"]
N = 10
K = 10
best = 0
current = 0
total_cost = 0
win = 0
for i in range(0,K):
    current = openBox(N)
    if current>best :
        best = current
    total_cost+=costs[i]
    win = best-total_cost
    #### calcolo soglia (>)
    t=win+total_cost+costs[i+1]
    ####
    prob = 0
    for x in range(0,N):
        if x<t:
            prob += t+1/(N+1)
        else:
            prob+= x/(N+1)
    if prob < 0.5:
        break


