# @z0nsk1 version 29.3.2021: backend fixed
# @z0nsk1 version 30.3.2021: temp, yee, oispakaliaa, lenny, virhekäsittely
# @z0nsk1 version 31.3.2021: temp: default Jyväskylä, argumentilla muun kaupungin sää. quote: argumentilla halutun
#                            henkilön quote. dice: argumenttina luku, joka toimii ylärajana. bingobangobongo
# @z0nsk1 version 8.2.2024: temp: uusi toteutus säätietojen hakemiseen, palveluna toimii open weather api.
#                           env: tokenien ja avaimien hakeminen .env-tiedostosta
# @z0nsk1 version 9.2.2024: temp: lataa nyt myös säähän liittyvän kuvan (tulee api-kutsun mukana)
# @z0nsk1 version 10.2.2024: kommentointia, members-komento toimii nyt

import urllib.request
import discord
import requests
from discord.ext import commands
import random
import datetime
import os
from dotenv import load_dotenv

versio = "08.02.2024"

# botti Discord -servereille

intents = discord.Intents.default()
intents.message_content = True
botti = commands.Bot(command_prefix='$', intents=intents, case_insensitive=True)
# client = discord.Client()

# kaupungit = []
quotet = []
helppi = ""

# Tokenien ja avainten haku .env tiedostosta
load_dotenv()
dirpath = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(dirpath, '.env.txt'))
bot_token = os.getenv('DISCORD_TOKEN')
weather_api_key = os.getenv('WEATHERAPI_KEY')
geo_api_key = os.getenv('GEOAPI_KEY')


def quotetiedosto():
    tied1 = "quotet.txt"
    with open(tied1, encoding='utf-8') as t:
        tiedosto = t.read().splitlines()

    for rivi in tiedosto:
        if rivi.startswith('"'):
            quotet.append(rivi)


def nonblank_lines(a):
    for li in a:
        rivi = li.rstrip()
        if rivi:
            yield rivi


"""
def kaupungittiedosto():
    tied1 = "suomenkaupungit.txt"
    with open(tied1, encoding='utf-8') as t:
        tiedosto = t.read().splitlines()

    for rivi in tiedosto:
        rivi = str(rivi).replace("(", "").replace(")", "").replace("'", "").replace(",", "").lower()
        kaupungit.append(rivi)
"""

tied = "help.txt"
with open(tied, encoding='utf-8') as f:
    for line in nonblank_lines(f):
        helppi = f.read()


# BOTIN TAPAHTUMAT


# Käynnistys
@botti.event
async def on_ready():
    print('Hyvät naiset ja herrat, botti on paikalla.')
    # kaupungittiedosto()
    quotetiedosto()  # Ladataan quote-tiedosto
    # Botin tila (näkyy discordissa nimen alla)
    await botti.change_presence(activity=discord.Game(name="Chilling | $apua"))


# Säätietojen haku
@botti.command(pass_context=True)
async def temp(ctx, *args):
    if args:
        # args tulee tuplena, poistetaan ylimääräiset merkit
        kaupunki = str(args).replace("(", "").replace(")", "").replace("'", "").replace(",", "").lower()
    else:
        kaupunki = "Jyväskylä"

    # Haetaan ensin kaupungin geotiedot (pituus- ja leveysasteet), jotka tarvitaan sää-apin kutsumiseen
    geourl = f"http://api.openweathermap.org/geo/1.0/direct?q={kaupunki}&limit={1}&appid={geo_api_key}"
    geoinfo = requests.get(geourl).json()  # Haetaan sisältö url:sta ja muutetaan se json-muotoiseksi
    print(geoinfo)
    # Jos kaupunkia ei löytynyt...
    if not geoinfo:
        await ctx.send("Kaupunkia ei ole!!")
        return

    # Otetaan pituus- ja leveysasteet haetusta datasta
    lat = geoinfo[0]["lat"]
    lon = geoinfo[0]["lon"]
    # Haetaan säätiedot
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}"
    wdata = requests.get(url).json()

    weatherid = wdata["weather"][0]["icon"]  # Otetaan datasta sääkuvan tunnus
    temperature = round(wdata["main"]["temp"])  # Otetaan datasta lämpötila
    # Haetaan vielä sääkuva tunnuksen perusteella (png-tiedosto)
    urllib.request.urlretrieve(f"https://openweathermap.org/img/wn/{weatherid}@2x.png", "icon.png")
    icon = open("icon.png", "rb")
    await ctx.send(f"{kaupunki.capitalize()} lämpötila klo {datetime.datetime.now().strftime('%H:%M')}"
                   f" {temperature} °C ", file=discord.File(icon))
    await ctx.send(f"\n\nSään tarjoaa OpenWeather API")


@botti.command(pass_context=True)
async def shtpost(ctx):
    x = random.randint(1, 18)  # Random-luku
    # TODO: voisi vielä laittaa automaattisesti laskemaan kuvien määrän, niin olisi helpompi lisätä kuvia
    await ctx.send(file=discord.File(f"kuvat/{x}.jpg"))


@botti.command(pass_context=True)
async def apua(ctx):
    await ctx.send(helppi)  # Lähetetään apua-tiedoston sisältö kanavalle


@botti.command(pass_context=True)
async def lenny(ctx):
    await ctx.send("( ͡° ͜ʖ ͡°)")


@botti.command(pass_context=True)
async def bingobangobongo(ctx):
    await ctx.send("Bish Bash Bosh!")


@botti.command(pass_context=True)
async def luikaus(ctx, *args):
    if args:
        args = str(args).replace("(", "").replace(")", "").replace("'", "").replace(",", "").capitalize()
        hquote = []
        for x in quotet:
            if args in x:  # Jos argumenttina tulleen henkilön löytyy quoteja...
                hquote.append(x)  # ...laitetaan ne hquote-taulukkoon
        await ctx.send(random.choice(hquote))  # ja lähetetään niistä satunnaisesti joku
    else:
        await ctx.send(random.choice(quotet))


@botti.command(pass_context=True)
async def pvm(ctx):
    pvmm = datetime.datetime.now()  # Nykyinen päivämäärä
    viikonpaiva = pvmm.weekday()  # Viikonpäivä (indeksinä)
    viikonpaivat = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai', 'Sunnuntai']
    muotoiltu = viikonpaivat[viikonpaiva] + pvmm.strftime(' %d.%m.%Y klo %H:%M viikko: ') + str(
        pvmm.isocalendar()[1])
    await ctx.send(muotoiltu)


@botti.command(pass_context=True)
async def dice(ctx, *args):
    if args:
        args = ''.join(args)
        if args.isdigit():  # Jos luku, lähetetään satunnainen luku 1 ja argumenttina annetun luvun väliltä
            luku = int(args)
            await ctx.send(random.randint(1, luku))
        else:
            await ctx.send("Ei tuo ole mikään luku, hölmö! :D")
            return
    else:
        await ctx.send(random.randint(1, 6))


# Serverin jäsenten määrä
@botti.command(pass_context=True)
async def members(ctx):
    membercount = ctx.guild.member_count
    await ctx.send(f"Kanavalla on jo {membercount} jäsentä!")


@botti.command(pass_context=True)
async def info(ctx):
    await ctx.send("Author: z0nsk1\nMade with Python\nVersion " + versio)


@botti.command(pass_context=True)
async def yee(ctx):
    await ctx.send(file=discord.File("kuvat/yee.jpg"))


# VIRHEKÄSITTELYT
@botti.event
async def on_command_error(cfx, error):
    if str(error).find("CommandNotFound"):
        await cfx.send("Komentoa ei ole olemassa.")
    else:
        pass

botti.run(bot_token)
# asyncio.run()

# TODO: Fingerpori komento
