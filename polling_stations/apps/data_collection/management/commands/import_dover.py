from django.contrib.gis.geos import MultiPoint
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = "E07000108"
    elections = ["local.2019-05-02"]
    scraper_name = "wdiv-scrapers/DC-PollingStations-Dover"
    geom_type = "geojson"

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid("districts"))
        code = record["district"].split("-")[0].strip()

        # PEX1 and PEX2 cover the exact same area
        # PSL1 and PSL2 cover the exact same area
        if code in ["PEX2", "PSL2"]:
            return None

        return {
            "internal_council_id": code,
            "name": record["district"],
            "area": poly,
            "polling_station_id": code,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record, self.geom_type, self.get_srid("stations")
        )
        if isinstance(location, MultiPoint) and len(location) == 1:
            location = location[0]

        address = "\n".join([record["NAME_OF_PO"], record["LOCATION"]])
        codes = record["POLLING_DI"].split("&")

        stations = []
        for code in codes:
            stations.append(
                {
                    "internal_council_id": code.strip(),
                    "postcode": record["POSTCODE"],
                    "address": address,
                    "location": location,
                }
            )
        return stations
