from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000044"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019Portsmouth.tsv"
    )
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Portsmouth.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "PO4 099":
            rec["postcode"] = "PO4 0PL"

        if uprn in ["1775078308", "1775035998", "1775002824", "1775002823"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "3596":
            rec["location"] = Point(-1.059545, 50.7866578, srid=4326)

        return rec
