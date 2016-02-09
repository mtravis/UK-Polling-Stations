"""
Imports COUNCIL
"""
import sys

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter

class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from COUNCIL
    """
    council_id     = 'COUNCIL_UD'
    districts_name = 'DISTRICT_FILE.kmz'
    stations_name  = 'STATION_FILE.csv'


    def district_record_to_dict(self, record):
        print('District', record)
        sys.exit(1)
        geojson = self.strip_z_values(record.geom.geojson)
        # Th SRID for the KML is 4326 but the CSV is 2770 so we
        # set it each time we create the polygon.
        # We could probably do with a more elegant way of doing
        # this longer term, but as this is the frist KML importer
        # we're weiting to abstract it
        self._srid = self.srid
        self.srid = 4326
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.srid))
        self.srid = self._srid
        return {
            'internal_council_id': record['Name'].value,
            'name'               : record['Name'].value,
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        print('Station', record)
        sys.exit(1)
        try:
            location = Point(int(record.point_x), int(record.point_y), srid=self.srid)
        except ValueError:
            location = Point(float(record.point_x), float(record.point_y), srid=self.srid)
        return {
            'internal_council_id': record.polling_di,
            'postcode': '(no postcode)',
            'address': "\n".join([record.building, record.road, record.town_villa]),
            'location': location
        }