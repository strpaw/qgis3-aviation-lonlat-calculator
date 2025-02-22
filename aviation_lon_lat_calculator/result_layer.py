"""Manage result layer (create, etc.)"""
from datetime import datetime

from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsField,
    QgsProject,
    QgsVectorLayer
)
from qgis.gui import QgisInterface


class ResultLayer:
    """Result layer handling"""

    def __init__(self, iface: QgisInterface):
        self._iface = iface
        self._name = None
        self._layer = None

    @property
    def name(self) -> str:
        """Return layer name"""
        return self._name

    def generate_name(self) -> None:
        """Generate name based in format: CalcPoints_<YYYY>_<MM>_<DD>_<HH><MM>"""
        timestamp = datetime.now()
        self._name = f'CalcPoints_{timestamp.strftime("%Y_%m_%d_%H%M")}'

    def create(self) -> None:
        """Create result layer as Point layer. Note this is memory layer so before closing QGIS save it on the disk
        to keep results.
        """
        self.generate_name()
        self._layer = QgsVectorLayer(
            path="Point?crs=epsg:4326",
            baseName=self._name,
            providerLib="memory"
        )
        self._layer.startEditing()
        prov = self._layer.dataProvider()
        prov.addAttributes(
            [
                QgsField(
                    name="point_id",
                    type=QVariant.String,
                    len=50
                ),
                QgsField(
                    name="lon",
                    type=QVariant.String,
                    len=50
                ),
                QgsField(
                    name="lat",
                    type=QVariant.String,
                    len=50
                ),
                QgsField(
                    name="definition",
                    type=QVariant.String,
                    len=200
                )
            ]
        )
        self._layer.commitChanges()

    def is_registered(self) -> bool:
        """Check if result layer is added to the layer list in the current project - layer was created
         and not removed from layers list in QGIS Project"""
        return bool(QgsProject.instance().mapLayersByName(self._name))

    def setup(self) -> None:
        """Prepare result layer for editing"""
        if not self._name or not self.is_registered():
            self.create()
            QgsProject.instance().addMapLayer(self._layer)

        self._iface.setActiveLayer(self._layer)
