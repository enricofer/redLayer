# -*- coding: utf-8 -*-
"""
/***************************************************************************
 idtVen - class idtVen_albero
                                 A QGIS plugin
 compilazione assistita metadati regione veneto
                              -------------------
        begin                : 2014-12-04
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
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

#from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_note_dialog import Ui_noteDialog

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
# create the dialog for zoom to point


class sketchNoteDialog(QDialog, Ui_noteDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        print "note"
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.mkNote)
        self.buttonBox.rejected.connect(self.cancel)
        self.iface = iface

    def newPoint(self,p):
        self.point = p
        self.show()

    def cancel(self):
        #self.hide()
        pass

    def mkNote(self):
        TD =QTextDocument(self.sourceString.text())
        textItem = QgsTextAnnotationItem( self.iface.mapCanvas() )
        textItem.setMapPosition(self.point)
        textItem.setFrameSize(TD.size())
        textItem.setDocument(TD)
        textItem.update()
        self.sourceString.setText("")
