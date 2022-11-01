import json


def main():
    with open("oceania_2.geojson") as f:
        geo = json.load(f)
    features = geo["features"]
    for feature in features:
        coordinates = feature["geometry"]["coordinates"]
        geo_type = feature["geometry"]["type"]
        for c1 in coordinates:
            for c2 in c1:
                if geo_type == "Polygon":
                    if c2[0] < 0:
                        c2[0] += 360
                else:
                    for c3 in c2:
                        if c3[0] < 0:
                            c3[0] += 360
    with open("oceania_3.geojson", "w") as f:
        json.dump(geo, f)


if __name__ == "__main__":
    main()
