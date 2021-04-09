import argparse
import asyncio
import json
import re
import uuid
import sys
from dataclasses import dataclass, asdict
from itertools import islice
from pathlib import Path
from typing import List

import aiohttp
from SPARQLWrapper import SPARQLWrapper2, JSON

@dataclass
class City:
    id: str
    name: str
    lat: float
    lon: float
    link: str

@dataclass
class Index:
    cities: List[City]


class MapboxService:

    BASE_URL = "https://api.mapbox.com"

    def __init__(self, token, map_style, sat_style, session):
        self.token = token
        self.map_style = map_style
        self.sat_style = sat_style
        self.session = session

    async def download_pair(self, city, data_dir):
        map_url = f"{MapboxService.BASE_URL}/styles/v1/{self.map_style}/static/{city.lon},{city.lat},15.25,0,0/1000x1000?access_token={self.token}"
        sat_url = f"{MapboxService.BASE_URL}/styles/v1/{self.sat_style}/static/{city.lon},{city.lat},15.25,0,0/1000x1000?access_token={self.token}"

        map_download = self.session.get(map_url)
        sat_download = self.session.get(sat_url)
        result_map, result_sat = await asyncio.gather(map_download, sat_download)

        chunk_size = 4096
        filename = data_dir / city.id
        with open(f"{filename}.png", "wb") as f:
            while True:
                chunk = await result_map.content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        with open(f"{filename}.jpg", "wb") as f:
            while True:
                chunk = await result_sat.content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

        return city
        


class WikidataService:

    BASE_URL = "https://query.wikidata.org/sparql"

    def __init__(self):
        self.sparql = SPARQLWrapper2(WikidataService.BASE_URL)
        self.geore = re.compile(r"Point\(([0-9.-]+) ([0-9.-]+)\)")

    def _convert_result(self, result):
        matches = self.geore.match(result["geo"].value)
        lon = float(matches.group(1))
        lat = float(matches.group(2))
        return City(uuid.uuid4().hex, result["name"].value, lat, lon, result["wikilink"].value)

    def get_cities(self):
        self.sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?name ?geo ?population ?wikilink
        WHERE {
            ?city wdt:P31 wd:Q515;
                  rdfs:label ?name;
                  wdt:P1082 ?population;
                  wdt:P625 ?geo.
            ?wikilink schema:about ?city;
                      schema:inLanguage "en";
                      schema:isPartOf <https://en.wikipedia.org/>.
            FILTER(?population > 50000)
            FILTER(lang(?name) = "en")
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        ORDER BY DESC (?population)
        """)
        return map(self._convert_result, self.sparql.query().bindings)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapbox-token", help="MapBox token", required=True)
    parser.add_argument("--mapbox-map-style", help="User and ID of flat map style (ex. aarroyoc/eryer233)", required=True)
    parser.add_argument("--mapbox-sat-style", help="User and ID of flat sat style (ex. aarroyoc/trew3267)", required=True)
    parser.add_argument("--max-number", help="Limit number of cities to download", type=int, default=10000)
    args = parser.parse_args()

    data_dir = Path.cwd() / "wizard-map-data"
    if data_dir.exists():
        print("Data folder already exists!")
        sys.exit(1)
    data_dir.mkdir()

    wikidata = WikidataService()
    cities = wikidata.get_cities()

    done_cities = list()
    async with aiohttp.ClientSession() as session:
        mapbox = MapboxService(args.mapbox_token, args.mapbox_map_style, args.mapbox_sat_style, session)

        def download(city):
            return mapbox.download_pair(city, data_dir)

        downloads = islice(map(download, cities), args.max_number)
        
        for task in asyncio.as_completed(downloads):
            try:
                city = await task
                done_cities.append(city)
            except:
                pass
    index = Index(done_cities)
    with open(data_dir / "index.json", "w") as f:
        json.dump(asdict(index), f)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())