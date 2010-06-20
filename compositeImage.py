from PIL import Image
import imageCompare
import os


def fileKey(filestr):# for simple natural ordering
	k=list(filestr)
	k.insert(0,len(filestr))
	return k


class CompositeImageGenerator:
	def __init__(self, directory, colorTolerance, checkRange, imageBorders):
		self.directory=directory
		self.ic=imageCompare.ImageCompare(colorTolerance, checkRange)
		self.framefiles=sorted(os.listdir(self.directory), key=fileKey)
		self.imageBorders=imageBorders

	def cropImage(self, image):
		cropRange=(0+self.imageBorders[0], 0+self.imageBorders[1],
			image.size[0]-self.imageBorders[2], image.size[1]-self.imageBorders[3])
		return image.crop(cropRange)

	def getImgOffsets(self, printStatus):
		img1=self.cropImage(Image.open(os.path.join(self.directory,self.framefiles[0])))
		self.framesize=img1.size

		lastpos=(0,0)
		imgpositions=[(lastpos[0], lastpos[1], self.framefiles[0])]
		self.framefiles.pop(0)

		for filename in self.framefiles:
			if printStatus:
				print "processing "+filename

			img2=self.cropImage(Image.open(os.path.join(self.directory,filename)))
			position=self.ic.compare(img1, img2, False)
			if printStatus:
				print " - offset: "+str((position[0],position[1]))
	
			lastpos=(lastpos[0]-position[0], lastpos[1]-position[1])
			imgpositions.append((lastpos[0], lastpos[1], filename))
			img1=img2

		return imgpositions

	def createCompositeImage(self, imgpositions):
		minx=min(imgpositions, key=lambda x: x[0])[0]
		miny=min(imgpositions, key=lambda x: x[1])[1]
		maxx=max(imgpositions, key=lambda x: x[0])[0]
		maxy=max(imgpositions, key=lambda x: x[1])[1]
		comsize=(self.framesize[0]+maxx-minx, self.framesize[1]+maxy-miny)

		compositeimg=Image.new("RGB", comsize, "white")
		for imgp in imgpositions:
			i2=self.cropImage(Image.open(os.path.join(self.directory,imgp[2])))
			w,h=i2.size
			compositeimg.paste(i2, (imgp[0]-minx, imgp[1]-miny, imgp[0]-minx+w, imgp[1]-miny+h))

		return compositeimg


