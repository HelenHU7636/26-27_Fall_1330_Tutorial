#get code, turns, target and attempts_left(string), and convert them to int
code=int(input())
turns=int(input())
target=int(input())
atmpts_left=int(input())

#get the hundreds, tens and units from code
#h,t,u:int
h=code//100
t=(code//10)%10
u=code%10

#rotate h,t,u by turns
#h_t,t_t,u_t:int
h_t=(h+turns)%10
t_t=(t+turns)%10
u_t=(u+turns)%10

#assemble back as a result(int)
res=h_t*100+t_t*10+u_t
print(res)
if res==target and atmpts_left>0:
    print("True")
else:
    print("False")


"""WHY can't I simply treat code as string without 
converting to num and slice code with []?
e.g.
code=input()
h=int(code[0])"""
