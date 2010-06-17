from compositeImage import CompositeImageGenerator

print("start")
print("get images")
dirname="frames"
cigen=CompositeImageGenerator(dirname, 50, (10,0,10,0), (16,0,16,0))

composite=cigen.createCompositeImage(cigen.getImgOffsets(True))
composite.show()
composite.save("results.jpg")

print("end")
