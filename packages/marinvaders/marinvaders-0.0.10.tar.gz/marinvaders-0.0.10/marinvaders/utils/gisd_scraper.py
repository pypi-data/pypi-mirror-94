"""
Script do scrap GISD web page to find distribution of species.
The result is a json file.
"""

import datetime
import logging
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def remove_dots(obj):
    # Goes recursively through and removes any periods in dict keys
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            if isinstance(value, dict) or isinstance(value, list):
                obj[index] = remove_dots(value)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict) or isinstance(value, list):
                obj[key] = remove_dots(value)
            new_key = key.replace(".", "_")
            if new_key != key:
                obj[new_key] = obj[key]
                del obj[key]
    return obj


def parse_csv():
    # Getting and reading the available CSV file with all species, unfiltered
    r = requests.get("http://www.iucngisd.org/gisd/export_csv.php")

    # Parsing the CSV into a list of dicts
    lines = r.text.splitlines()
    firstline = [word.strip('"') for word in lines[0].split(";") if word != ""]
    species_plural = []
    for line in lines[1:]:
        line = [word.strip('"') for word in line.split(";") if word != ""]
        species_plural.append({firstline[i]: line[i]
                               for i in range(len(firstline))})

    # Filtering the list to include only certain systems
    species_plural = [{key: value for key, value in species.items()} for species in species_plural
                      if species["System"] in ["Marine", "Brackish", "Marine_freshwater_brackish"]]

    return species_plural


def process_species(species, retried=0):
    try:
        url = "http://www.iucngisd.org/gisd/speciesname/{}".format(
            species['Species'].replace(' ', '+'))
        species_page = requests.get(url)
        if species_page.status_code != 200:
            logging.warning("Bad HTTP response for {}: {}".format(
                species['Species'], species_page.status_code))
        else:
            soup = BeautifulSoup(species_page.text, "html.parser")

            general_impacts = ""
            try:
                for content in soup.find("div", id="spe-general-title").find_next_sibling("div").contents:
                    general_impacts += str(content)
            except:
                logging.info("No general impacts div for {}".format(
                    species['Species']))
            species["General_impacts"] = general_impacts

            native_range = []
            for nr in soup.find("div", id="nr-title").find_next_sibling("ul").find_all("li"):
                native_range.append(nr.string.strip())

            alien_range = []
            for ar in soup.find("div", id="ar-title").find_next_sibling("ul").find_all("li"):
                sc, nlc = ar["id"].split("*")
                loc_per_country = requests.get(
                    "http://www.iucngisd.org/gisd/function/species_location.php?sc={}&nlc={}".format(sc, nlc))
                for location in loc_per_country.json():
                    dc = location["distribution_code"]
                    payload = {"sc": sc, "dc": dc}
                    species_loc_main = requests.get("http://www.iucngisd.org/gisd/function/species_location_2.php",
                                                    params=payload).json()
                    species_loc_man = requests.get("http://www.iucngisd.org/gisd/function/species_location_3.php",
                                                   params=payload).json()
                    species_loc_imp = requests.get("http://www.iucngisd.org/gisd/function/species_location_4.php",
                                                   params=payload).json()
                    if len(species_loc_main) > 1 or len(species_loc_imp) > 1:
                        logging.warning("specie_loc returns for {} in {} are longer than 1".format(
                            species['Species'], location['location_name']))
                        logging.info(species_loc_main)
                        logging.info(species_loc_imp)

                    if species_loc_main and "name" in species_loc_main[0] and "location_name" in species_loc_main[0]:
                        alien_range.append(species_loc_main[0])
                        # country = species_loc_main[0]["name"].strip()
                        # location = species_loc_main[0]["location_name"].strip()
                        # if location not in alien_range:
                        #     alien_range[location] = {}
                        # alien_range[location] = {}
                        # species_loc = alien_range[location]
                        # species_loc["species_loc_main"] = species_loc_main[0]
                        # if species_loc_imp:
                        #     species_loc["species_loc_imp"] = species_loc_imp[0]
                        # species_loc["species_loc_man"] = species_loc_man
                    else:
                        logging.info(
                            "Insufficient information to save species_loc")

    except ConnectionError:
        if retried < 3:
            time.sleep(1)
            return process_species(species, retried=retried+1)
        else:
            logging.error("Too many retries")
    except Exception as e:
        logging.error(e)

    # return remove_dots(species)
    return general_impacts, native_range, alien_range


def main():
    logging.basicConfig(level=logging.WARNING)
    species_list = parse_csv()

    json_output = {}
    json_output['processing_timestamp'] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    gisd = []
    for species in species_list:
        general_impacts, native_range, alien_range = process_species(species)
        species['general_impacts'] = general_impacts
        species['native_range'] = native_range
        species['alien_range'] = alien_range

        gisd.append(species)

    df = pd.DataFrame(gisd)
    df.to_json('gisd.json')


if __name__ == "__main__":
    main()
