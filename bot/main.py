from bot import ShotgunBot
import asyncio

# url = "https://collecte.io/quadrabang-2023-3137005/fr"
url = "https://collecte.io/votre-collecte-18813/"
date = 1696371281
price = 20

bot = ShotgunBot(url, date, price)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(bot.execute())