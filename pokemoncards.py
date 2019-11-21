import urllib.request as urllib
import json

file = open("cardbank","w")

u = urllib.urlopen("https://api.pokemontcg.io/v1/cards")
data = json.read(u)
print(data)

# for card in info:
#     file.write(info[cards][card][name]);
