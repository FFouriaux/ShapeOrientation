# -*- coding: utf-8 -*-
"""
/***************************************************************************
Shape Orientation
								 A QGIS plugin
 A plugin for compute the orientation of major axis of polygons and draw
 rose diagram of polygons or lines orientations
							 -------------------
		begin                : 2017-07
		copyright            : 2017 F.Fouriaux - Eveha
		email                : francois.fouriaux@eveha.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#using Unicode for all strings
from __future__ import unicode_literals

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import *
from qgis.core import *
from qgis.gui import *
import ntpath
from ShapeOrientation_engine import *

localelang = QSettings().value('locale/userLocale')[0:2]

def selectLayer(layerName):
	layers=iface.legendInterface().layers()
	for l in layers:
		if l.name() == layerName:
			return l

def AjoutShpLayer(fileName):
	if os.name=='nt':
		fileName='/'+fileName
	nom= ntpath.basename(fileName)
	iface.addVectorLayer(fileName,nom,"ogr")

def AjoutCsvLayer(fileName):
	if os.name=='nt':
		fileName='/'+fileName
	nom= ntpath.basename(fileName)
	iface.addVectorLayer(fileName,nom,"delimitedtext")

class ShorientDialg(QDialog):
	def __init__(self):
		QDialog.__init__(self)
	
		
	 
	# list of layers polygons shp already charged in the interface   
	def layerPolyList(self):
		layers = iface.legendInterface().layers()
		layer_list = []
		self.cbox_PolyShp.clear()
		for layer in layers:
			if layer.providerType()=='ogr':
				if layer.dataProvider().storageType() == 'ESRI Shapefile' and layer.geometryType() == 2:
					layer_list.append(layer.name())
		
		self.cbox_PolyShp.addItems(layer_list)
		
		
	# list of lines shp already charged in the interface
	def layerLineList(self):
		layers = iface.legendInterface().layers()
		layer_list = []
		self.cbox_LineShp.clear()
		for layer in layers:
			if layer.providerType()=='ogr':
				if layer.dataProvider().storageType() == 'ESRI Shapefile' and layer.geometryType() == 1:
					layer_list.append(layer.name())
		
		self.cbox_LineShp.addItems(layer_list)


	def selectedLayerPoly(self):
	 
		if self.cbox_PolyShp.currentText():
			return selectLayer(self.cbox_PolyShp.currentText())



	def updateIDFieldPoly(self):
		self.cbox_PolyIdField.clear()
		layer = self.selectedLayerPoly()
		field_list=[]
		if layer is not None:            
			fields = layer.dataProvider().fields()
			for f in fields:
				name = f.name()
				field_list.append(name)
				
		self.cbox_PolyIdField.addItems(field_list)

	def selectedLayerLine(self):
	 
		if self.cbox_LineShp.currentText():
			return selectLayer(self.cbox_LineShp.currentText())



	def updateIDFieldLine(self):
		self.cbox_LineIdField.clear()
		layer = self.selectedLayerLine()
		field_list=[]
		if layer is not None:            
			fields = layer.dataProvider().fields()
			for f in fields:
				name = f.name()
				field_list.append(name)
				
		self.cbox_LineIdField.addItems(field_list)

   
	def selectDirectory(self):
		self.LineEdit_Output.setText(QFileDialog.getExistingDirectory(self))

	def OpenShp(self):
		filtre= 'Shapefiles (*.shp)'
		FileName= QFileDialog(filter=filtre)
		if FileName.exec_():
			fileName=FileName.selectedFiles()
		AjoutShpLayer(fileName[0]) 
		self.layerLineList()
		self.layerPolyList()
		
		
	def RunPoly (self): 
		while True:
			poly=self.cbox_PolyShp.currentText()
			export=self.LineEdit_Output.text()
			interval=self.doubleSpinBox.value()
			diagr=self.checkDiagram.isChecked()
			colorRamp=self.cbox_ColorRamp.currentText()
			Id=self.cbox_PolyIdField.currentText()
			if poly != '':
				pass
			else :
				iface.messageBar().pushMessage("Error", "No Layer Selected", level=QgsMessageBar.WARNING)
				break
			if export=='':
				iface.messageBar().pushMessage("Error", "No export folder selected", level=QgsMessageBar.WARNING)
				break
			elif os.path.exists(export):
				pass 
			else: 
				iface.messageBar().pushMessage("Error", "The export folder selected doesn't exists", level=QgsMessageBar.WARNING)
				break
			shpPath=''
			for layer in iface.legendInterface().layers():
				if layer.name() == poly:
					a= layer.publicSource()
					if a[0:5] =='file:':
						b=str(a.split('?')[0])
						shpPath=urllib.unquote(b)[7:]
						if os.name=='nt':
							shpPath=shpPath[1:]
					else:
						shpPath=a
						if os.name=='nt':
							shpPath=shpPath[1:]
			table=export+'/Orientation_'+poly+'.csv'
			DiagOrientPolyg (shpPath, interval, table, diagr,colorRamp,Id)
			AjoutCsvLayer(table)
			iface.messageBar().clearWidgets()
			iface.messageBar().pushMessage("ShapeOrientation", "Orientation Completed", level=QgsMessageBar.SUCCESS)
			break 
			
	def RunLine (self): 
		while True:
			line=self.cbox_LineShp.currentText()
			export=self.LineEdit_Output.text()
			interval=self.doubleSpinBox_2.value()
			diagr=self.checkDiagram.isChecked()
			colorRamp=self.cbox_ColorRamp.currentText()
			Id=self.cbox_LineIdField.currentText()
			if line != '':
				pass
			else :
				iface.messageBar().pushMessage("Error", "No Layer Selected", level=QgsMessageBar.WARNING)
				break
			if export=='':
				iface.messageBar().pushMessage("Error", "No export folder selected", level=QgsMessageBar.WARNING)
				break
			elif os.path.exists(export):
				pass 
			else: 
				iface.messageBar().pushMessage("Error", "The export folder selected doesn't exists", level=QgsMessageBar.WARNING)
				break
			shpPath=''
			for layer in iface.legendInterface().layers():
				if layer.name() == line:
					a= layer.publicSource()
					if a[0:5] =='file:':
						b=str(a.split('?')[0])
						shpPath=urllib.unquote(b)[7:]
						if os.name=='nt':
							shpPath=shpPath[1:]
					else:
						shpPath=a
						if os.name=='nt':
							shpPath=shpPath[1:]
			table=export+'/Orientation_'+line+'.csv'
			DiagOrientLine (shpPath, interval, table, diagr,colorRamp,Id)
			AjoutCsvLayer(table)
			iface.messageBar().clearWidgets()
			iface.messageBar().pushMessage("ShapeOrientation", "Orientation Completed", level=QgsMessageBar.SUCCESS)
			break 

   
