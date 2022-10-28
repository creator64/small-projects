import csv
from tabulate import tabulate

fields_to_show = ["herkomst", "doel", "e-nummer", "naam", "opmerkingen", "kleur", "soort"]
fields_to_show = ["naam", "e-nummer", "soort", "kleur"]

def get_records_from_input(a):
    records_found = []
    for record in data:
        for field in record:
            if a.lower() in record[field].lower():
                records_found.append(record)
    return records_found


file = open("db.csv", "r")
data = list(csv.DictReader(file))

while True:
    print("Zoek naar een E-Nummer")
    i = input()
    if len(i) < 2:
        print("zoek naar iets dat 2 letters of langer is\n\n")
        continue
    print(f"\nGevonden resultaten voor {i}:\n")
    records_found = get_records_from_input(i)
    for record in records_found:
        for field in fields_to_show:
            print(field + ":", record[field])
        print("---------------------------------")
        
    print("\n\n")
