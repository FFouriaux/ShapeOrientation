##Polygones=vector polygon
##Interval_Angle= number
##Export=output directory

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.gui import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


# F.Fouriaux juillet 2017


# # # # Fonctions # # # #
# F Gisement(point1, point2) --> Return Gisement
def Gisement (a,b):
	deltax=a[0]-b[0]
	signex=deltax/abs(deltax)
	deltay=a[1]-b[1]
	if deltay == 0:
		theta=pi+(pi/2*signex)
	else: 
		theta=atan(deltax/deltay)
		
	if deltax<=0 and deltay<=0:
		gis=theta
	elif deltax>=0 and deltay<=0:
		gis=theta
	else:
		gis=theta + pi
		
	if gis<0:
		gis=2*pi+gis
		
	return gis

# F MinRect(polygone,point)  --> Return Polygon minimum, rectangle minimum,  orientation of the great axis
def MinRect(hull,centre) :
	n=len(hull.asPolygon()[0])
	aires=[]
	gisement=0.0
	rotation=0.0
	orient=0.0
	for i in range(n-1) :
		gisement=Gisement(hull.asPolygon()[0][i],hull.asPolygon()[0][i+1])      # azimuth computation
		rotation= rotation+gisement                                             # Record the rotations
		hull.rotate(-1*180*gisement/pi,centre)                                  # inverse rotation of the azimuth
		bboxrect=hull.boundingBox()                                             # creation of the bounding box
		airebbox=bboxrect.width()*bboxrect.height()                             # computation of the area of the bbox
		aires.append(airebbox)                                                  # append this area in a list for comparaison
		if airebbox == min(aires):
			if bboxrect.xMaximum()-bboxrect.xMinimum()<=bboxrect.yMaximum()-bboxrect.yMinimum():
				orient=rotation                                                 # selection of the major axis
			else:
				orient=rotation+(pi/2)

			if orient>=2*pi:                                                    # Angle between 0 and 360 degree
				n=int(orient/(2*pi))
				orient=orient-(n*2*pi)
			if orient > pi: 
				orient=orient-pi                                                # Azimut between 0 and 180 deg cause we can't know the direction

	return orient

# F DiagGenerator (angles,interval) --> Show a matplotlib rose diagram of orientation
def DiagGenerator (angles,inter,theta,interval, colorRamp):
	#progress bar initialisation
	iface.messageBar().clearWidgets()
	progressMessageBar=iface.messageBar().createMessage("Creation of the diagram ...")
	progress= QProgressBar()
	progress.setMaximum(100)
	progressMessageBar.layout().addWidget(progress)
	iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
	
	#frequency
	histo=hist(angles,inter)[0]
	r=histo.tolist()
	
	# fake plot to get the color bar
	plot = plt.scatter(r, r, c = r, cmap = colorRamp+'_r')
	plt.clf()
	#colorRamp
	cr=cm.get_cmap(name=colorRamp+'_r')
	# diagram
	ax = plt.subplot(111, projection='polar')
	colors= cr(histo/float(max(histo)))
	larg=interval*pi/180
	
	ax.bar(theta,r,width=larg,color=colors,align='center',edgecolor='black')
	ax.set_rmax(max(r))
	ticks=np.arange(0,max(r),max(r)/4)
	ax.set_rticks(ticks)  # less radial ticks
	ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
	ax.set_theta_direction(-1)
	ax.set_theta_zero_location("N")
	ax.grid(True)

	plt.colorbar(plot)
	ax.set_title("Frequence des orientations", va='bottom')
	progress.setValue (100)
	
	plt.show() 

def DiagOrientPolyg (poly, interval, table, diagr, colorRamp, Id):
	
	polygones= QgsVectorLayer(poly,"polygones","ogr")
	poly_prov= polygones.dataProvider()
	# Csv File for orientation record
	Exrap= open(table,'w')
	firstline='Id,Orientation\n'
	Exrap.write(firstline)


	fPolyg=polygones.getFeatures()
	angles=[]
	# intervals on the circle
	inter=np.arange(0,361,interval)
	inter=[i*pi/180 for i in inter]
	theta=inter[0:-1]
	
	#number of iteration for progress bar
	ntot=polygones.featureCount()
	ni=0
	
	#progress bar initialisation
	iface.messageBar().clearWidgets()
	progressMessageBar=iface.messageBar().createMessage("Computation of directions ...")
	progress= QProgressBar()
	progress.setMaximum(100)
	progressMessageBar.layout().addWidget(progress)
	iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
	# Loop on geometries
	for f in fPolyg:
		ni+=1
		progress.setValue(ni/ntot*100)
		geomPolyg= f.geometry() 
		Aire=geomPolyg.area()
		Idf=str(f.attribute(Id))

	# ConvexHull and centroid of the polygon
		
		hullPolyg=geomPolyg.convexHull()
		centroidPolyg=geomPolyg.centroid().asPoint()

		gist= MinRect(hullPolyg,centroidPolyg)
		csvline='%s,%f\n' %(Idf,gist*180/pi)
		Exrap.write (csvline)
		angles.append(gist)

	Exrap.close()
	if diagr == True:
		DiagGenerator(angles,inter,theta,interval, colorRamp)

def DiagOrientLine (line, interval, table, diagr, colorRamp,Id):
	
	lines= QgsVectorLayer(line,"lines","ogr")
	lines_prov= lines.dataProvider()

	# Csv File for orientation record
	Exrap= open(table,'w')
	firstline='Id,Orientation\n'
	Exrap.write(firstline)


	fLine=lines.getFeatures()
	angles=[]
	# intervals on the circle
	inter=np.arange(0,361,interval)
	inter=[i*pi/180 for i in inter]
	theta=inter[0:-1]


	# Loop on geometries
	for f in fLine:

		geomLine= f.geometry() 
		Idf=str(f.attribute(Id))
		geomL=geomLine.geometry()
		a=QgsPoint(geomL.startPoint().x(),geomL.startPoint().y())
		b=QgsPoint(geomL.endPoint().x(),geomL.endPoint().y())

	# Azimuth of the line

		gist= Gisement(a,b)
		csvline='%s,%f\n' %(Idf,gist*180/pi)
		Exrap.write (csvline)
		angles.append(gist)

	Exrap.close()
	if diagr == True:
		DiagGenerator(angles,inter,theta,interval,colorRamp)
