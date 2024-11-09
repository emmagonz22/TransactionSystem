from . import extract_csv
from . import extract_json
from . import extract_xml
from . import extract_yml

def run_etl():
    extract_csv.load_promotions()
    extract_csv.load_transfer_csv()
    extract_xml.load_transactions()
    extract_yml.load_people_yaml()
    extract_json.load_people_json()