import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import dotenv_values
from time import sleep

config = dotenv_values(".env")

client = MongoClient(config["MONGO_URI"])
db = client[config["DB_NAME"]]

data = list(db["botdatas"].find())
print(data)


tarif = None
while tarif == None:
  try:
    # res = requests.get("https://collecte.io/votre-collecte-18813/")
    res = requests.get("https://collecte.io/quadrabang-2023-3137005/fr")
    soup = BeautifulSoup(res.text, 'html.parser')
    tarif = list(soup.find("select", id="val5").children)[-1].get_text()
  except:
    print("La page est indisponible")
    sleep(1)
    pass

print(tarif)

# TODO: Faire les requêtes en parallèle au lieu de les faire en séquentiel
# Pour un échantillon pas trop immense de personnes c'est pas trop grave mais
# c'est horriblement pas optimisé
while len(data) > 0:
  user = data.pop()
  params = {
    # "slug": "votre-collecte-18813",
    "slug": "quadrabang-2023-3137005",
    "customdata[val1]": user["lastName"],
    "customdata[val2]": user["firstName"],
    "customdata[val3]": user["phone"],
    "customdata[val4]": user["email"],
    "customdata[val5]": tarif,
    # "price": 20,
    "price": 17,
    "payment_method": "lydia"
  }
  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest"
  }
  res = requests.post("https://collecte.io/createrequest?", headers=headers, data=params)
  if ("error_message" in res.json()):
    data.insert(0, user)
    print("Erreur lors de l'envoi des données")
    continue
  db["botdatas"].delete_one({"_id": user["_id"]})

print("Données supprimées")