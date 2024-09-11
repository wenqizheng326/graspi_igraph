import random

def testFileMaker(num,depth,textFileName):
    f = open(textFileName,"x")

    with open(textFileName,'a') as f:

        f.write(str(num)+" "+str(num)+ " "+str(depth)+"\n")

        for x in range(num):
            for y in range((num-1)):
                if x < num/2:
                    f.write("1" + " ")
                else:
                    f.write("0" + " ")

            if x < num/2:
                f.write("1" + "\n")
            else:
                f.write("0" + "\n")

    f.close()

    return "success"

testFileMaker(1000,1,"testFile-1000-2D.txt")
        
