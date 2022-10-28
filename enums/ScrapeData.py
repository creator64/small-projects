from urllib import request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import csv
import math
import copy

url = "https://www.ahealthylife.nl/lijst-van-e-nummers/"
csv_fields = ["herkomst", "doel", "e-nummer", "naam", "opmerkingen", "kleur", "soort"]
column_groups_in_site = [["herkomst", "doel", "e-nummer", "naam", "opmerkingen"], ["herkomst", "doel", "e-nummer", "naam"], ["doel", "e-nummer", "naam", "opmerkingen"]]
color_dict = {"#eba6a6": "ROOD", "#f3b691": "ORANJE", "#afebc4": "GROEN"}

type_dict = {
    100: "Kleurstoffen",
    200: "Conserveermiddelen / Voedingszuren",
    300: "Antioxidanten",
    400: "Emulgatoren",
    500: "Diverse additieven",
    600: "Smaakversterkers",
    700: "Conserveermiddelen",
    900: "Anti-schuimmiddelen, glansmiddelen, deegverbeteraars, zoetstoffen",
    1400: "Gemodificeerde zetmelen"
}

class Scraper:
    def __init__(self):
        self.request_site = Request(url, headers={"User-agent": "Mozilla/5.0"})
        self.html = urlopen(self.request_site).read()
        self.soup = bs(self.html, "html.parser")


    def scrape_data(self):
        self.current_columns_site = column_groups_in_site[0]
        
        with open("db.csv", "w") as file: # create the headers
            dict_writer = csv.DictWriter(file, delimiter=',', fieldnames=csv_fields)
            dict_writer.writeheader()

            for index, row in enumerate(self.soup.find_all("tr")): # go trough every row
                row_dict = {}
                row.contents = remove_all_of_a_certain_element(row.contents, '\n')

                row_list = []
                for cell in row.contents: # first we make a list of a row
                    if cell.string == '\n': continue # sth weird
                    if cell.string == None: # when there is no string in the cell
                        row_list.append("")
                    else:
                        row_list.append(cell.string.replace("′", "'")) # csv cant encode ′ so we have to replace it to '

                if (L := lower(row_list)) in column_groups_in_site: # then we check if this row is a header (like [Doel, E-nummer, Naam, Opmerkingen])
                    self.current_columns_site = L
                    print("current columns in site is the list", self.current_columns_site)
                    continue # we dont want the column list in our data

                for x, cellstring in enumerate(row_list): # if its not a header we make a row_dict {doel: blablabla, enummer: blablabla, naam: blabla, opmerkingen: blablablablabla
                    key = self.current_columns_site[x]
                    row_dict[key] = cellstring

                color = self.get_color(row);               row_dict["kleur"] = color_dict[color]
                type_num = self.get_type_num(row_dict);    row_dict["soort"] = type_dict[type_num]
                row_dict = self.add_missing_fields(row_dict)
                print(index, row_dict)
                dict_writer.writerow(row_dict)


    def add_missing_fields(self, row_dict: dict): # will add the missing fields in a certain row_dict
        fields_in_dict = list(row_dict.keys())
        for field in csv_fields:
            if field not in fields_in_dict:
                row_dict[field] = ""
        return row_dict


    def get_color(self, row) -> ["ROOD", "ORANJE", "GROEN"]:
        color = list(row.children)[1]["bgcolor"]
        return color

    def get_type_num(self, row_dict):
        n = get_number_from_enumber(row_dict["e-nummer"])
        type_num = math.floor(n/100) * 100
        return type_num



def remove_all_of_a_certain_element(l: list, element):
    try:
        while True:
            l.remove(element)
    except: return l # when all the elements are gone we cant remove it and well get an error

def get_number_from_enumber(enum: str) -> int:
    return_string = ""
    for char in enum:
        try:
            n = int(char) # add every character of the string that is a number to the string we want to return
            return_string += char
        except: continue
    if int(return_string) > 1400:
        return_string = return_string[0:3] # fix problems like E491-495
    return int(return_string) # when the string is the correct number make it an integer and return it

def lower(l: list): # will make all strings in a list lower
    list_to_modify = copy.copy(l)
    for n, string in enumerate(l):
        list_to_modify[n] = string.lower()
    return list_to_modify
    

scraper = Scraper()
#scraper.scrape_data() # this will get the data from the site
