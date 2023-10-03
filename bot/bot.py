import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import dotenv_values
from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
import json

class ShotgunBot():
  CHROMEDRIVER_PATH = "W:\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.188\\chromedriver-win32\\chromedriver.exe"


  def __init__(self, shotgun_url: str, timestamp: int, price: int):
    self.date = datetime.fromtimestamp(timestamp)  
    self.url = shotgun_url
    self.slug = shotgun_url.split("/")[-2]
    self.price = price

    print(f"Shotgun à l'addresse {self.url} pris en cible pour le {self.date.strftime('%d/%m')} à {self.date.strftime('%H:%M:%S')} pétantes")
    
    config = dotenv_values(".env")
    client = MongoClient(config["MONGO_URI"])
    self.db = client[config["DB_NAME"]]

    data = list(self.db["botdatas"].find())
    # self.data = json.load(open("./data.json", "r", encoding="utf-8"))

    self.data = []
    dataset = set()
    for user in data:
      if (user["phone"] not in dataset): self.data.append(user)
      dataset.add(user["phone"])

    print("Réservations à effectuer :", len(self.data))


  async def execute(self):
    # t_minus_10 = self.date - timedelta(minutes=10)
    t_minus_5 = self.date - timedelta(minutes=5)
    if (datetime.now() < t_minus_5):
      sleep((self.date - t_minus_5).total_seconds())
    self._get_tarif()
    fails = await self._sniper()

    target = len(self.data)
    result = target - len(fails)
    print(f"{result} places sur {target} ont été réservées !")
    if (len(fails) > 0):
      print("Les places suivantes n'ont pas été réservées :")
      for f in fails:
        print(f"{f['user']['firstName']} {f['user']['lastName']}")
    self.db["botdatas"].drop()


  def _get_tarif(self):
    self.tarif = None
    while self.tarif == None:
      try:
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        self.tarif = list(soup.find("select", id="val5").children)[-1].get_text()
      except:
        print("La page est indisponible")
        sleep(1)
        pass

    print("Elément tarif identifié :", self.tarif)


  async def _sniper(self):
    async with aiohttp.ClientSession() as session:
      ret = await asyncio.gather(*[self._send_request(session, u["firstName"], u["lastName"], u["phone"], u["email"]) for u in self.data])
    retries = 0
    while (not all([r == None for r in ret]) and retries < 5):
      sleep(3)
      retries += 1
      async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[self._send_request(session, r["user"]["firstName"], r["user"]["lastName"], r["user"]["phone"], r["user"]["email"]) for r in ret if r != None])
    return [r for r in ret if r != None]

  async def _send_request(self, session: aiohttp.ClientSession, firstName: str, lastName: str, phone: str, email: str):
  # params can't be a dict as they need to be hashed by asyncio
    try:
      req = self._prepare_request(firstName=firstName, lastName=lastName, phone=phone, email=email)

      res = await session.post(url="https://collecte.io/createrequest?", data=req["data"], headers=req["headers"])
      js = await res.json(content_type="text/html")
      if ("error_message" in js):
        raise Exception(js["error_message"])
      print(f"Place réservée pour {req['user']['firstName']} {req['user']['lastName']}")
    except Exception as e:
      print(f"Erreur dans l'obtention d'une place pour {req['user']['firstName']} {req['user']['lastName']}:", e.__class__, e)
      return req
    
    # res = requests.post("https://collecte.io/createrequest?", headers=headers, data=data)


  def _prepare_request(self, **user) -> dict:
    data = {
      "slug": self.slug,
      "customdata[val1]": user["lastName"],
      "customdata[val2]": user["firstName"],
      "customdata[val3]": user["phone"],
      "customdata[val4]": user["email"],
      "customdata[val5]": self.tarif,
      "price": self.price,
      "payment_method": "lydia"
    }
    headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Requested-With": "XMLHttpRequest"
    }
    return {
      "data": data,
      "headers": headers,
      "user": user
    }