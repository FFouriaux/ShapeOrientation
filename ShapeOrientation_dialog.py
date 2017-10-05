# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShapeOrientationDialog
								 A QGIS plugin
 This plugin calculate a diagrame of the major orientations of polygons 
							 -------------------
		begin                : 2017-07-24
		git sha              : $Format:%H$
		copyright            : (C) 2017 by FFouriaux Eveha
		email                : francois.fouriaux@eveha.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ShapeOrientationDialog import *
from ShapeOrientation_engine import *

image=os.path.join(os.path.dirname(__file__),"images")

FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'ShapeOrientation_dialog_base.ui'))


class ShapeOrientationDialog(ShorientDialg, FORM_CLASS):
	def __init__(self, parent=None):
		"""Constructor."""
		ShorientDialg.__init__(self)
		# Set up the user interface from Designer.
		# After setupUI you can access any designer object by doing
		# self.<objectname>, and you can use autoconnect slots - see
		# http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
		# #widgets-and-dialogs-with-auto-connect
		self.setupUi(self)
		self.layerPolyList()
		self.layerLineList()
		self.cbox_ColorRamp.addItem(QIcon(os.path.join(image,"AutomnRamp.png")),"autumn")
		self.cbox_ColorRamp.addItem(QIcon(os.path.join(image,"WinterRamp.png")),"winter")
		self.cbox_ColorRamp.addItem(QIcon(os.path.join(image,"SummerRamp.png")),"summer")
		self.cbox_ColorRamp.addItem(QIcon(os.path.join(image,"BoneRamp.png")),"bone")
		self.cbox_ColorRamp.addItem(QIcon(os.path.join(image,"GreyRamp.png")),"gray")
		QObject.connect(self.pushButton_Output, SIGNAL('clicked()'),self.selectDirectory)
		QObject.connect(self.pushButton_1, SIGNAL('clicked()'),self.OpenShp)
		QObject.connect(self.pushButton_2, SIGNAL('clicked()'),self.OpenShp)
		QObject.connect(self.cbox_PolyShp, SIGNAL('currentIndexChanged(QString)'), self.updateIDFieldPoly)
		QObject.connect(self.cbox_LineShp, SIGNAL('currentIndexChanged(QString)'), self.updateIDFieldLine)
		QObject.connect(self.pushButton_Poly, SIGNAL('clicked()'),self.RunPoly)
		QObject.connect(self.pushButton_Line, SIGNAL('clicked()'),self.RunLine)
