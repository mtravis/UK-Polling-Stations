from data_collection.geo_utils import fix_bad_polygons
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "E08000033"
    districts_name = "europarl.2019-05-23/Version 1/Polling districts shp files/POLLING_DISTRICTS.shp"
    stations_name = "europarl.2019-05-23/Version 1/Polling stations shape files/POLLING_STATIONS.shp"
    elections = ["europarl.2019-05-23"]
    shp_encoding = "utf-8"

    def district_record_to_dict(self, record):
        code = record[0].strip()
        name = record[1].strip()
        return {"internal_council_id": code, "name": name, "polling_station_id": code}

    def station_record_to_dict(self, record):
        code = record[1].strip()
        address = record[0].strip()

        if code == "" and address == "":
            return None

        return {"internal_council_id": code, "address": address, "postcode": ""}

    def post_import(self):
        fix_bad_polygons()
