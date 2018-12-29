from os import listdir 
import sys

# Validate parameters
if len(sys.argv) > 3:
    print "Feed me more parameters..."
    sys.exit()
elif sys.argv[1][-3:len(sys.argv[1])] != "pth":
    print "I only accept .pth files to convert."
elif sys.argv[2][-4:len(sys.argv[2])] != "html":
    print "I can only generate .html files!"

# Open/create files
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")

inputmod = input.read().split("\n")
inputmod = list(filter(None, inputmod)) # filter out empty stuff to make for less loops

i = 0
while i < len(inputmod):
    if "<css/>" in inputmod[i]:
        filenames = listdir("css/")
        inputmod.remove(inputmod[i])
        j = i
        difference = j + len(filenames)
        while j < difference:
            index = j - i
            if ".css" in filenames[index]:
                inputmod.insert(j, "\t\t<link rel='stylesheet' type='text/css' href='css/"+filenames[index]+"'>")
            j += 1
    elif "<javascript/>" in inputmod[i]:
        filenames = listdir("javascript/")
        inputmod.remove(inputmod[i])
        j = i
        difference = j + len(filenames)
        while j < difference:
            index = j - i
            if ".js" in filenames[index]:
                inputmod.insert(j, "\t\t<script src='javascript/"+filenames[index]+"'></script>")
            j += 1
    i += 1

output.write("\n".join(inputmod))

# Make sure you close files after use.
input.close()
output.close()