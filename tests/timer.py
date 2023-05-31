timer_set = open("timer.txt", "w")
timer_set.write("Time left: \nPercentage done: ")
timer_set.close()

def timer_update(new_status):
    timer = open("timer.txt", "r")
    lines = timer.readlines()
    timer.close()
    
    timer = open("timer.txt", "w")
    lines[0] = new_status
    timer.write(lines[0]+"\n"+lines[1])
    print("Timer updated: "+new_status)
    timer.close()
    
    
timer_update("test1")
timer_update("test2")
timer_update("test3")
timer_update("test4")
timer_update("test5")

timer = open("timer.txt", "r+")
lines = timer.readlines()
print(lines)