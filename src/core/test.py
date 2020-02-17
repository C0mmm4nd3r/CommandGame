import random 

def game():
    count = 0
    ans = random.randint(1,5)
    while count < 2:
        value = int(input("input value : "))
        if value < ans:
            print("큽니다 시발련아")
        elif value > ans:
            print("작습니다 시발련아")
        else: 
            print("같네요")
            return True
        count+=1
    print("=========================== : ",ans)
    return False 

while True:
    count =0
    while game():
        count += 1 
    print("result : ",count)
