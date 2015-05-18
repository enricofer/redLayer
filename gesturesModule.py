__author__ = 'ferregutie'

from qgis.core import *
from qgis.utils import *
from qgis.gui import *

class gestures:

    def __init__(self):
        self.idx = 0
        self.allGestures = {}
        self.index = QgsSpatialIndex()
        self.sketchLayer = QgsVectorLayer("LineString?crs="+self.iface.mapCanvas().mapRenderer().destinationCrs().toWkt(), "Sketch Layer", "memory")
        #self.sketchLayer.setCrs(self.iface.mapCanvas().mapRenderer().destinationCrs())
        self.sketchLayer.addAttribute(QgsField("note",QVariant.String))
        self.sketchLayer.addAttribute(QgsField("color",QVariant.String))
        self.sketchLayer.addAttribute(QgsField("width",QVariant.Double))
        self.sketchLayer.addAttribute(QgsField("transparency",QVariant.Double))
        self.sketchLayer.loadNamedStyle(os.path.join(self.plugin_dir,"sketchLayerStyle.qml"))
        QgsMapLayerRegistry.instance().addMapLayer(self.sketchLayer)
        self.iface = iface
        self.interval = self.iface.mapCanvas().mapUnitsPerPixel()*5
        self.currentWidth = QColor("#aa0000")
        self.currentColor = 5
        self.editingGesture = None

    def currentColor(self,currentColor):
        self.currentColor = currentWidth

    def setCurrentStyle(self,currentWidth,currentColor,currentTransparency):
        self.currentWidth = currentColor
        self.currentColor = currentWidth
        self.currentTransparency = currentTransparency

    def setCurrentStyle(self,currentWidth,currentColor,currentTransparency):
        self.currentWidth = currentColor
        self.currentColor = currentWidth
        self.currentTransparency = currentTransparency

    def initGesture(self):
        self.idx += 1
        self.allGestures[idx] = sketchGesture(self,self.idx)
        self.editingGesture = True
        return self.allGestures[idx]

    def break_gestures(self,point):
        self.erasePoint = point
        intervalRect = QgsRectangle(point.x()+self.interval,point.y()+self.interval,point.x()-self.interval,point.y()-self.interval)
        indexedGestures = self.index.intersects(intervalRect)
        result = []
        for featId in indexedGestures:
            self.breakGesture(self.sketchLayer.getFeature(QgsFeatureRequest(featId)).next(),point,self.interval)


    def __del__(self):
        QgsMapLayerRegistry.instance().removeMapLayer(self.sketchLayer.id())


class sketchGesture:
    def __init__(self,parent,idx)
        self.id = idx
        self.parent = parent
        self.sketch=QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
        self.sketch.setWidth(self.parent.currentWidth)
        self.sketch.setColor(self.parent.currentColor)

    def addPoint(self,point):
        self.sketch.addPoint(point)

    def commitGesture(self,note = None):
        if note:
            noteTxt = note
        else:
            noteTxt = ""
        self.feat = QgsFeature()
        self.feat.setGeometry(self.sketch.asGeometry())
        self.feat.setAttributes([note,self.parent.currentColor.name(),self.parent.currentWidth/3.5,self.parent.currentTransparency])
        self.parent.sketchLayer.startEditing()
        self.parent.sketchLayersketchLayer.addFeatures(self.feat)
        self.parent.index.insertFeature(self.feat)
        self.parent.sketchLayersketchLayer.commitChanges()
        self.sketch.reset()

    def breakGesture(self,point,buffer):
        pointNearest = None
        afterVertex = None
        leftOf = 0
        #self.feat.geometry().closestSegmentWithContext(point, pointNearest, afterVertex, leftOf)
        bufferCursor = QgsGeometry.fromPoint(point).buffer(buffer,10)
        diffGeom = self.feat.geometry().difference(bufferCursor)


