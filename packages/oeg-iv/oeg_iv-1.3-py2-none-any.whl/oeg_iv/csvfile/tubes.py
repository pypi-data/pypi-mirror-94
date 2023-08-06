"""Tubes iterator interface for InspectionViewer export csv file."""
from .. import Error


class Tube:
    """Represent one pipe."""

    def __init__(self, dist, stream):
        """Construct new tube object at dist with given data stream state."""
        self.dist = int(dist)
        self.stream = stream

        self.typ = None
        self.length = None
        self.thick = None
        self.category = None

        self.is_thick_change = False
        self.is_category_change = False

        self.seams = []
        self.lineobjects = []
        self.defects = []
        self.categories = []
        self.thicks = []

    def finalize(self, dist, _warns):
        """Finalize tube data at given dist."""
        self.length = int(dist) - self.dist

    def add_object(self, row):
        """Add data to tube from IV csv row."""
        if row.is_defect:
            self.defects.append(row)
        elif row.is_lineobj:
            self.lineobjects.append(row)
        elif row.is_seam:
            self.seams.append(row)
        elif row.is_category:
            self.categories.append(row)
        elif row.is_thick:
            self.thicks.append(row)

        else:
            raise Error("Tube at dist {} has wrong row: {}".format(self.dist, str(row)))
