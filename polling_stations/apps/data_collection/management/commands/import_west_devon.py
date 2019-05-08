from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000047"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019WD.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019WD.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013755070":
            rec["postcode"] = "EX201FQ"

        if uprn in [
            "10001329690"  # EX201SQ -> EX201JJ : Beechwood, Upcott Hill, Okehampton, Devon
        ]:
            rec["accept_suggestion"] = False

        return rec
