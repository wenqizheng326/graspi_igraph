import random

def testFileMaker(num,depth,textFileName):
    f = open(textFileName,"x")

    with open(textFileName,'a') as f:

        f.write(str(num)+" "+str(num)+ " "+str(depth)+"\n")

        for x in range(num):
            for y in range(num-1):
                f.write(str(random.randint(0,1)) + " ")
            f.write(str(random.randint(0,1)) + "\n")

    f.close()

    return "success"

testFileMaker(1000,1,"testFile-1000.txt")
        
