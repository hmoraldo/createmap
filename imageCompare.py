from PIL import Image
from PIL import ImageChops 
import time

quickmode=True

class ImageCompare:
	def __init__(self, tolerance, (maxLeftCheck, maxUpCheck, maxRightCheck, maxDownCheck)):
		self.maxLeftCheck=maxLeftCheck
		self.maxRightCheck=maxRightCheck
		self.maxUpCheck=maxUpCheck
		self.maxDownCheck=maxDownCheck
		self.tolerance=tolerance # from 0 to 255, around 10 is fine for tolerance

	def compareAt(self, img1, img2, xoffset, yoffset, debug):
		tmp=ImageChops.difference(ImageChops.offset(img1, xoffset, yoffset), img2)

		# remove the warped around parts of the image
		if xoffset>0:
			xoffl=xoffset
			xoffr=0
		else:
			xoffl=0
			xoffr=xoffset
		if yoffset>0:
			yofft=yoffset
			yoffd=0
		else:
			yofft=0
			yoffd=yoffset
		tmp=tmp.crop((xoffl, yofft, tmp.size[0]+xoffr, tmp.size[1]+yoffd))
		if debug: tmp.show()

		# compute error value
		counter=0

		if quickmode:
			tmp=tmp.convert("L")
			hi=tmp.histogram()
			for h in range(self.tolerance, len(hi)):
				counter=counter+hi[h]*h
		else:
			seq=tmp.getdata()
			for s in seq:
				if max(s)>self.tolerance:
					counter=counter+sum(s)

		error=float(counter)/(tmp.size[0]*tmp.size[1])

		return error


	def compare(self, img1, img2, debug):
		xcheck=range(-self.maxLeftCheck, self.maxRightCheck+1)
		ycheck=range(-self.maxUpCheck, self.maxDownCheck+1)
		errortable=[]

		t1=time.time()
		for xc in xcheck:
			for yc in ycheck:
				err=self.compareAt(img1, img2, xc, yc, False)
				errortable.append((xc, yc, err))
		t2=time.time()
		print "time "+str(t2-t1)
	
		minerror=min(errortable, key=lambda x: x[2])

		if debug:
			self.compareAt(img1, img2, minerror[0], minerror[1], True)

		return (minerror[0], minerror[1])

