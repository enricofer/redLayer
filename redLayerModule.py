# -*- coding: utf-8 -*-
"""
/***************************************************************************
 redLayer
                                 A QGIS plugin
 fast georeferenced annotation
                              -------------------
        begin                : 2015-03-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Enrico Ferreguti
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import uic
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog

from qgis.core import *
from qgis.utils import *
from qgis.gui import *

#from redLayerModule_dialog import redLayerDialog
import os.path
import json


class redLayer(QgsMapTool):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'redLayer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        #self.dlg = redLayerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Red Layer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'redLayer')
        self.toolbar.setObjectName(u'redLayer')
        QgsMapTool.__init__(self, self.canvas)
        self.iface.projectRead.connect(self.projectReadAction)
        self.iface.newProjectCreated.connect(self.newProjectCreatedAction)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('redLayer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        if callback:
            action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.add_action(
            ':/plugins/redLayer/icons/sketch.png',
            text=self.tr(u'Sketch'),
            callback=self.sketchAction,
            parent=self.iface.mainWindow())
        #self.add_action(
        #    ':/plugins/redLayer/icons/pen.png',
        #    text=self.tr(u'Pen'),
        #    callback=self.penAction,
        #    parent=self.iface.mainWindow())
        canvasButton = self.add_action(
            ':/plugins/redLayer/icons/canvas.png',
            text=self.tr(u'Color canvas'),
            callback=None,
            parent=self.iface.mainWindow())
        self.add_action(
            ':/plugins/redLayer/icons/erase.png',
            text=self.tr(u'Erase'),
            callback=self.eraseAction,
            parent=self.iface.mainWindow())
        self.add_action(
            ':/plugins/redLayer/icons/remove.png',
            text=self.tr(u'remove sketches from map'),
            callback=self.removeSketchesAction,
            parent=self.iface.mainWindow())
        self.noteButton = self.add_action(
            ':/plugins/redLayer/icons/toLayer.png',
            text=self.tr(u'export sketches to Memory layer'),
            callback=None,
            parent=self.iface.mainWindow())
        canvasButton.setMenu(self.canvasMenu())
        self.noteButton.setCheckable (True)
        self.geoSketches = []
        self.dumLayer = QgsVectorLayer("Point?crs=EPSG:4326", "temporary_points", "memory")
        self.pressed=None
        self.currentColor = QColor("#FF0000")
        self.currentWidth = 5

    def canvasMenu(self):
        contextMenu = QMenu()
        self.colorRedAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","colorRed.png")),"")
        self.colorRedAction.triggered.connect(self.colorRedFunc)
        self.colorGreenAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","colorGreen.png")),"")
        self.colorGreenAction.triggered.connect(self.colorGreenFunc)
        self.colorBlueAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","colorBlue.png")),"")
        self.colorBlueAction.triggered.connect(self.colorBlueFunc)
        self.colorBlackAction = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","colorBlack.png")),"")
        self.colorBlackAction.triggered.connect(self.colorBlackFunc)
        self.width2Action = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","width2.png")),"")
        self.width2Action.triggered.connect(self.width2Func)
        self.width4Action = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","width4.png")),"")
        self.width4Action.triggered.connect(self.width4Func)
        self.width8Action = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","width8.png")),"")
        self.width8Action.triggered.connect(self.width8Func)
        self.width16Action = contextMenu.addAction(QIcon(os.path.join(self.plugin_dir,"icons","width16.png")),"")
        self.width16Action.triggered.connect(self.width16Func)
        return contextMenu

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.removeSketchesAction()
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Red Layer'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar


    def sketchAction(self):
        """Run method that performs all the real work"""
        gsvMessage="Click on map to draw geo sketches"
        self.iface.mainWindow().statusBar().showMessage(gsvMessage)
        self.dumLayer.setCrs(self.iface.mapCanvas().mapRenderer().destinationCrs())
        self.canvas.setMapTool(self)
        self.canvasAction = "sketch"
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #pass

    def penAction(self):
        pass

    def canvasAction(self):
        pass

    def colorRedFunc(self):
        self.currentColor = QColor("#FF0000")

    def colorGreenFunc(self):
        self.currentColor = QColor("#00FF00")

    def colorBlueFunc(self):
        self.currentColor = QColor("#0000FF")

    def colorBlackFunc(self):
        self.currentColor = QColor("#FFFFFF")

    def width2Func(self):
        self.currentWidth = 2

    def width4Func(self):
        self.currentWidth = 4

    def width8Func(self):
        self.currentWidth = 8

    def width16Func(self):
        self.currentWidth = 16

    def eraseAction(self):
        gsvMessage="Click on map to erase geo sketches"
        self.iface.mainWindow().statusBar().showMessage(gsvMessage)
        self.dumLayer.setCrs(self.iface.mapCanvas().mapRenderer().destinationCrs())
        self.canvas.setMapTool(self)
        self.canvasAction = "erase"

    def exportAction(self):
        pass

    def removeSketchesAction(self):
        for sketch in self.geoSketches:
            sketch[2].reset()
        self.geoSketches = []


    def canvasPressEvent(self, event):
        # Press event handler inherited from QgsMapTool used to store the given location in WGS84 long/lat
        self.pressed=True
        self.px = event.pos().x()
        self.py = event.pos().y()
        self.pressedPoint = self.canvas.getCoordinateTransform().toMapCoordinates(self.px, self.py)
        #print self.PressedPoint.x(),self.PressedPoint.y()
        #self.pointWgs84 = self.transformToWGS84(self.PressedPoint)
        if self.canvasAction == "sketch_":
            self.sketch=QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
            self.sketch.setWidth(self.currentWidth)
            self.sketch.setColor(self.currentColor)
            self.sketch.addPoint(self.pressedPoint)

    def canvasMoveEvent(self, event):
        # Moved event handler inherited from QgsMapTool needed to highlight the direction that is giving by the user
        if self.pressed:
            #print "canvasMoveEvent"
            x = event.pos().x()
            y = event.pos().y()
            movedPoint = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            if self.canvasAction == "sketch":
                if abs(x-self.px)>3 or abs(y-self.py)>3:
                    sketch=QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
                    sketch.setWidth(self.currentWidth)
                    sketch.setColor(self.currentColor)
                    sketch.addPoint(self.pressedPoint)
                    sketch.addPoint(movedPoint)
                    self.pressedPoint = movedPoint
                    self.geoSketches.append([self.currentColor.name(),str(self.currentWidth),sketch,""])
                    self.px = x; self.py = y
            if self.canvasAction == "erase":
                cursor = QgsRectangle (self.canvas.getCoordinateTransform().toMapCoordinates(x-7,y-7),self.canvas.getCoordinateTransform().toMapCoordinates(x+7,y+7))
                for sketch in self.geoSketches:
                    if sketch[2].asGeometry() and sketch[2].asGeometry().boundingBox().intersects(cursor):
                        sketch[2].reset()


    def canvasReleaseEvent(self, event):
        #self.geoSketches.append(self.sketch)
        self.pressed=None
        if self.canvasAction == "sketch" and self.noteButton.isChecked():
            textItem = QgsTextAnnotationItem( self.iface.mapCanvas() )
            textItem.setMapPosition(self.pressedPoint)
            textItem.setFrameSize(QSizeF(200,100))
            txt = "Red Layer Note"
            textItem.setDocument(QTextDocument(txt))
            self.geoSketches[-1][3]=txt
            textItem.update()


    def newProjectCreatedAction(self):
        #remove current sketches
        self.removeSketchesAction()

    def projectReadAction(self):
        #remove current sketches
        self.removeSketchesAction()
        #connect to signal to save sketches along with project file
        QgsProject.instance().projectSaved.connect(self.saveSketches)
        #load project.sketch if file exists
        self.loadSketches()

    def saveSketches(self):
        sketchFileInfo = QFileInfo(QgsProject.instance().fileName())
        outfile = open(os.path.join(sketchFileInfo.path(),sketchFileInfo.baseName()+'.sketch'), 'w')
        for sketch in self.geoSketches:
            if sketch[2].asGeometry():
                outfile.write(sketch[0]+'|'+sketch[1]+'|'+sketch[2].asGeometry().exportToWkt()+'\n'+"|"+sketch[3])
        outfile.close()

    def loadSketches(self):
        projectFileInfo = QFileInfo(QgsProject.instance().fileName())
        sketchFileInfo = QFileInfo(os.path.join(projectFileInfo.path(),projectFileInfo.baseName()+'.sketch'))
        if sketchFileInfo.exists():
            infile = open(sketchFileInfo.filePath(), 'r')
            canvas = self.iface.mapCanvas()
            mapRenderer = canvas.mapRenderer()
            srs=mapRenderer.destinationCrs()
            dumLayer = QgsVectorLayer("Line?crs="+str(srs.authid()), "temporary_lines", "memory")
            self.geoSketches = []
            for line in infile:
                #print line
                inline = line.split("|")
                sketch=QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
                sketch.setWidth( int(inline[1]) )
                sketch.setColor(QColor(inline[0]))
                sketch.setToGeometry(QgsGeometry.fromWkt(inline[2]),dumLayer)
                self.geoSketches.append([inline[0],inline[1],sketch])
                if inline[3] != "":
                    pass
            infile.close()

