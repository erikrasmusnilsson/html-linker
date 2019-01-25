from os import listdir
from os import system
import time
import sys

sass = False

# Validate parameters
if len(sys.argv) < 3:
    print ("Feed me more parameters...")
    sys.exit()
elif sys.argv[1][-3:len(sys.argv[1])] != "pth":
    print ("I only accept .pth files to convert.")
elif sys.argv[2][-4:len(sys.argv[2])] != "html":
    print ("I can only generate .html files!")
elif len(sys.argv) > 3 and sys.argv[3] == "--sass":
    sass = True

CSS_PATH = "css/"
JS_PATH = "javascript/"

cssBefore = dict([(file, None) for file in listdir(CSS_PATH)])
jsBefore = dict([(file, None) for file in listdir(JS_PATH)])

def link():
    # Open/create files
    input = open(sys.argv[1], "r")
    output = open(sys.argv[2], "w")

    inputmod = input.read().split("\n")
    inputmod = list(filter(None, inputmod)) # filter out empty stuff to make for less loops

    i = 0
    while i < len(inputmod):
        if "<css/>" in inputmod[i]:
            filenames = listdir(CSS_PATH)
            inputmod.remove(inputmod[i])
            j = i
            difference = j + len(filenames)
            cursor = j
            while j < difference:
                index = j - i
                if sass:
                    sassfiles = listdir("sass/")
                    for file in sassfiles:
                        filename = file[0:file.find(".")]
                        system("sass sass/%s css/%s" % (filename + ".scss", filename + ".css"))
                if filenames[index][-4:len(filenames[index])] == ".css":
                    inputmod.insert(cursor, "\t\t<link rel='stylesheet' type='text/css' href='css/"+filenames[index]+"'>")
                j += 1
        elif "<javascript/>" in inputmod[i]:
            filenames = listdir(JS_PATH)
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

    # If sass option is true, watch the sass files
    if sass:
        system("sass --watch sass:css")

link() # do an initial linking before watching 
print ("linker.py is now active, ctrl+c to exit.")
while True:
    time.sleep(10)
    cssAfter = dict([(file, None) for file in listdir(CSS_PATH)])
    jsAfter = dict([(file, None) for file in listdir(JS_PATH)])
    if (cssBefore != cssAfter or jsBefore != jsAfter):
        link()