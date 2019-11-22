import urllib.request as urllib
import json

with open('cardbank', "w", encoding="utf-8") as file:
    x = 1
    while (x < 13):
        url = "https://api.pokemontcg.io/v1/cards?pageSize=1000&page="+str(x)
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        req = urllib.Request(url, headers=hdr)
        data = json.loads( urllib.urlopen(req).read())

        i = 0
        if (x != 12):
            end = 1000
        else:
            end = 901
        while (i < end):
            # print(x)
            # print(i)
            if (data['cards'][i]['supertype'] == 'Pokémon'):
                if ('rarity' in data['cards'][i]):
                    file.write(data['cards'][i]['name'] + ", " +
                                data['cards'][i]['imageUrlHiRes'] + ", " +
                                data['cards'][i]['set'] + ", " +
                                data['cards'][i]['series'] + ", " +
                                data['cards'][i]['rarity'] + ", " +
                                data['cards'][i]['types'][0] + ", " +
                                data['cards'][i]['subtype'] + "\n")
                else:
                    file.write(data['cards'][i]['name'] + ", " +
                                data['cards'][i]['imageUrlHiRes'] + ", " +
                                data['cards'][i]['set'] + ", " +
                                data['cards'][i]['series'] + ", " +
                                "Common" + ", " +
                                data['cards'][i]['types'][0] + ", " +
                                data['cards'][i]['subtype'] + "\n")
            else:
                if ('rarity' in data['cards'][i]):
                    file.write(data['cards'][i]['name'] + ", " +
                                data['cards'][i]['imageUrlHiRes'] + ", " +
                                data['cards'][i]['set'] + ", " +
                                data['cards'][i]['series'] + ", " +
                                data['cards'][i]['rarity'] + ", " +
                                data['cards'][i]['subtype'] + "\n")
                else:
                    if ('subtype' in data['cards'][i]):
                        file.write(data['cards'][i]['name'] + ", " +
                                    data['cards'][i]['imageUrlHiRes'] + ", " +
                                    data['cards'][i]['set'] + ", " +
                                    data['cards'][i]['series'] + ", " +
                                    "Common" + ", " +
                                    data['cards'][i]['subtype'] + "\n")
                    else:
                        file.write(data['cards'][i]['name'] + ", " +
                                   data['cards'][i]['imageUrlHiRes'] + ", " +
                                   data['cards'][i]['set'] + ", " +
                                   data['cards'][i]['series'] + ", " +
                                   "Common" + ", " + "\n")
            i += 1
        x += 1
