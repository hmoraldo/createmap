from compositeImage import CompositeImageGenerator
import config
import sys

if len(sys.argv)<3:
	print "Error, more arguments needed."
	print "Usage:"
	print "python createmap.py [frames directory] [results file]"
	print "Also remember to adjust the configuration values in config.py before running this."
	exit()

print "Remember to adjust the configuration values in config.py before running this."

framesdir=sys.argv[1]
resultsfile=sys.argv[2]


print("- processing images")
dirname="frames"
cigen=CompositeImageGenerator(framesdir, config.colorTolerance, config.checkRange, config.imageBorders)

print("- composing image")
composite=cigen.createCompositeImage(cigen.getImgOffsets(True))
composite.show()
composite.save(resultsfile)

print("done")
