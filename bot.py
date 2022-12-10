import json
import sqlite3
from PIL import Image
from table2ascii import table2ascii
import extcolors
import requests
import PIL
import os
import discord
from dotenv import load_dotenv
load_dotenv()
con = sqlite3.connect("bot_db.db")
cur = con.cursor()

intents = discord.Intents.default()
intents.message_content = True


def get_country_embed(pais):
    pais.lower()
    pais_raw = requests.get(
        f"https://restcountries.com/v3.1/name/{pais}")
    data_pais = pais_raw.json()
    clima_raw = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={data_pais[0]['latlng'][0]}&lon={data_pais[0]['latlng'][1]}&appid={'2cd4b906451c18a0484baf589f40dc4f'}&lang=es")
    data_clima = clima_raw.json()
    nombre_pais = data_pais[0]['name']['common']
    capital = data_pais[0]['capital'][0]
    region = data_pais[0]['region']
    population = data_pais[0]['population']
    weather = data_clima['weather'][0]['description']
    flag = data_pais[0]['flags']['png']
    image = PIL.Image.open(requests.get(flag, stream=True).raw)

    colors = extcolors.extract_from_image(image)
    color1 = colors[0][0][0][0]
    color2 = colors[0][0][0][1]
    color3 = colors[0][0][0][2]
    embed = discord.Embed(
        title=pais.capitalize(),
        description="Información del país",
        color=discord.Colour.from_rgb(color1, color2, color3)
    )

    embed.add_field(name="Capital", value=capital, inline=True)
    embed.add_field(name="Población",
                    value=f" {'{:,}'.format(population)}", inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.set_thumbnail(url=flag)
    embed.add_field(name="Clima", value=weather)
    embed.set_image(
        url=f"http://openweathermap.org/img/wn/{data_clima['weather'][0]['icon']}@2x.png")

    return embed


def get_team(team_name, equipos):
    for equipo in equipos:
        if equipo["name_en"] == team_name:
            return equipo


def get_matchs(name, teams):
    matchs = []
    for match in teams:
        if match['home_team_en'] == name:
            matchs.append(match)
        elif match['away_team_en'] == name:
            matchs.append(match)
    return matchs


def get_data(id, url):
    res = cur.execute("""
        SELECT token FROM users
        WHERE discord_id = ?
    """, [id])
    token = res.fetchone()[0]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response


client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/calc'):
        operacion = message.content.split(' ')[1]

        def calc():
            try:
                if operacion.__contains__("+"):
                    num1 = float(operacion.split("+")[0])
                    num2 = float(operacion.split("+")[1])
                    return num1 + num2
                elif operacion.__contains__("-"):
                    num1 = float(operacion.split("-")[0])
                    num2 = float(operacion.split("-")[1])
                    return num1 - num2
                elif operacion.__contains__("*"):
                    num1 = float(operacion.split("*")[0])
                    num2 = float(operacion.split("*")[1])
                    return num1 * num2
                elif operacion.__contains__("/"):
                    num1 = float(operacion.split("/")[0])
                    num2 = float(operacion.split("/")[1])
                    return num1 / num2
                else:
                    return "Datos invalidos"
            except ValueError:
                return "Numeros invalidos"

        resultado = calc()

        if isinstance(resultado, str):
            await message.channel.send(resultado)
        else:
            await message.channel.send(f"""
            El resultado es: {calc()}
            """)

    if message.content.startswith('/pais'):
        try:
            response_message = await message.channel.send("Cargando...")
            pais = str(message.content.split(' ')[1])
            embed = get_country_embed(pais)
            await response_message.delete()
            await message.channel.send(embed=embed)
        except IndexError:
            id = str(message.author.id)
            res = cur.execute("""
                SELECT country FROM users
                WHERE discord_id = ?
            """, [id])
            country = res.fetchone()[0]
            embed = get_country_embed(country)
            await response_message.delete()
            await message.channel.send(embed=embed)
        except:
            await response_message.delete()
            await message.channel.send("El pais no existe")

    if message.content.startswith('/registro'):
        try:
            id = message.author.id
            name = message.content.split(" ")[1]
            email = message.content.split(" ")[2]
            password = message.content.split(" ")[3]
            confirm_password = message.content.split(" ")[4]

            user = {
                "name": name,
                "email": email,
                "password": password,
                "passwordConfirm": confirm_password
            }
            json_body = json.dumps(user)
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(
                "http://api.cup2022.ir/api/v1/user", data=json_body, headers=headers)
            error = response.json()
            if str(error["message"]).__contains__("duplicate"):
                return await message.channel.send(f"<@{id}> ya estas registrado")
            elif str(error["message"]).__contains__("the minimum allowed length"):
                return await message.channel.send(f"<@{id}> contrasena")
            elif str(error["message"]).__contains__("valid email"):
                return await message.channel.send(f"<@{id}> email")
            cur.execute("""
                INSERT INTO users (discord_id, name, email, password) VALUES(?, ?, ?, ?)
            """, (id, name, email, password))
            con.commit()
            await message.channel.send(f"Registro satisfactorio! <@{id}>")
        except sqlite3.IntegrityError:
            await message.channel.send(f"<@{id}> tu usuario ya se encuentra registrado!")
        except:
            await message.channel.send(f"<@{id}> datos incompletos!")

    if message.content.lower().startswith('/usuario'):

        id = message.author.id
        # Buscar
        res = cur.execute("""
                SELECT name FROM users WHERE discord_id = ?
        """, [id])
        user = res.fetchone()[0]
        await message.channel.send(f"<@{id}>, tu usuario es ***{user}***")


    if message.content.startswith('/eliminar'):
        try:
            id = message.author.id
            # Buscar usuario
            res = cur.execute("""
                SELECT * FROM users WHERE discord_id = ?
            """, (id,))
            user = res.fetchone()[0]
            print(user)
            # Eliminar usuario
            cur.execute("""
                DELETE FROM users WHERE discord_id = ?
            """, (id,))
            con.commit()
            await message.channel.send(f"Usuario eliminado! <@{id}>")
        except:
            await message.channel.send(f"<@{id}> el usuario no existe!")

    if message.content.startswith('/iniciar'):
        id = message.author.id
        res = cur.execute("""
            SELECT email, password FROM users
            WHERE discord_id = ?
        """, [id])
        data = res.fetchone()
        credentials = {
            "email": data[0],
            "password": data[1]
        }
        json_body = json.dumps(credentials)
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(
            "http://api.cup2022.ir/api/v1/user/login", data=json_body, headers=headers).json()
        token = response["data"]["token"]
        cur.execute("""
            UPDATE users
            SET token = ?
            WHERE discord_id = ?
        """, (token, id))
        con.commit()
        await message.channel.send(f"<@{id}> iniciaste sesion. Puedes usar todas las funciones del bot")

    if message.content.startswith("/equipo"):
        try:
            pais = str(message.content.split(" ")[1]).capitalize()
            id = message.author.id
            response = get_data(id, "http://api.cup2022.ir/api/v1/team")
            equipos = response.json()["data"]
            info_equipo = get_team(pais, equipos)
            print(info_equipo)
            if info_equipo is None:
                await message.channel.send(f"<@{id}> {pais} no clasifico al mundial.")
            name = info_equipo["name_en"]
            flag = info_equipo["flag"]
            group = info_equipo["groups"]
            image = Image.open(requests.get(flag, stream=True).raw)

            colors = extcolors.extract_from_image(image)
            color1 = colors[0][0][0][0]
            color2 = colors[0][0][0][1]
            color3 = colors[0][0][0][2]

            embed = discord.Embed(
                title=name.capitalize(),
                description=f"GRUPO {group}",
                color=discord.Colour.from_rgb(color1, color2, color3)
            )
            embed.set_thumbnail(url=flag)
            await message.channel.send(embed=embed)
        except:
            await message.channel.send(f"<@{id}> tienes que colocar 1 pais.")

    if message.content.startswith("/partidos"):
        id = message.author.id
        pais = str(message.content.split(" ")[1]).capitalize()
        response = get_data(id, "http://api.cup2022.ir/api/v1/match")
        equipos = response.json()["data"]
        matchs = get_matchs(pais, equipos)
        if len(matchs) == 0:
            await message.channel.send(f"<@{id}> {pais} no clasifico al mundial.")
        for match in matchs:
            local_team = match['home_team_en']
            away_team = match['away_team_en']
            date = match['local_date']
            local_goals = match['home_score']
            away_goals = match['away_score']
            flag = match['home_flag']
            image = Image.open(requests.get(flag, stream=True).raw)

            colors = extcolors.extract_from_image(image)
            color1 = colors[0][0][0][0]
            color2 = colors[0][0][0][1]
            color3 = colors[0][0][0][2]

            embed = discord.Embed(
                title=f"{local_team} vs {away_team}",
                color=discord.Colour.from_rgb(color1, color2, color3)
            )
            embed.add_field(name='Casa', value=local_team)
            embed.add_field(name='Visitante', value=away_team)
            embed.add_field(name='Fecha', value=date)
            embed.add_field(name=f'Goles {local_team}', value=local_goals)
            embed.add_field(name=f'Goles {away_team}', value=away_goals)
            embed.set_thumbnail(url=flag)
            await message.channel.send(embed=embed)

    if message.content.startswith('/grupo'):
        id = message.author.id
        group_letter = str(message.content.split(" ")[1]).capitalize()

        if (group_letter == 'A' or group_letter == 'B' or group_letter == 'C' or group_letter == 'D' or group_letter == 'E' or group_letter == 'F' or group_letter == 'G' or group_letter == 'H'):
            response = get_data(
                id, f"http://api.cup2022.ir/api/v1/standings/{group_letter}")
            if response.status_code == 401:
                await message.channel.send("Tienes que volver a iniciar sesion. Corre el comando **!iniciar**.")
            teams = response.json()["data"][0]["teams"]
            outputArray = []

            for team in teams:
                teamArray = [team['name_en'], team['mp'],
                             team['w'], team['d'], team['l'], team['pts'],]
                outputArray.append(teamArray)
            output = table2ascii(
                header=["Equipos", "PJ", "PG", "PE", "PP", 'PTS'],
                body=outputArray,
            )

            return await message.channel.send(f'```{output}```')

        response = get_data(id, "http://api.cup2022.ir/api/v1/team/")

        if response.status_code == 401:
            await message.channel.send("Tienes que volver a iniciar sesion. Corre el comando **!iniciar**.")

        equipos = response.json()["data"]
        team = get_team(group_letter, equipos)
        group = team['groups']

        team_response = get_data(
            id, f'http://api.cup2022.ir/api/v1/standings/{group}')

        teams = team_response.json()['data'][0]['teams']
        outputArray = []

        for team in teams:
            teamArray = [team['name_en'], team['mp'],
                         team['w'], team['d'], team['l'], team['pts'],]
            outputArray.append(teamArray)
        output = table2ascii(
            header=["Equipos", "PJ", "PG", "PE", "PP", 'PTS'],
            body=outputArray,
        )
        return await message.channel.send(f'```{output}```')

    if message.content.startswith('/help'):
        await message.channel.send('''
        **Comandos**:
        \n**/calc**: Para realizar operaciones matematicas sencillas deberá colocar el primer conjunto de numeros seguido de el signo de la operación que desea realizar y por ultimo el segundo conjunto de números.
        \n**/pais**: Muestra información detallada del país que busque.
        \n**/registro**: Este comando sirve para registrar tu usuario y el orden es: 'Usuario' 'correo' 'contraseña' 'confirmar contraseña'.
        \n**/usuario**: Te mostrará el nombre de tu usuario.
        \n**/eliminar**: Escriba el nombre de usuario que desea eliminar.
        \n**/iniciar**: Luego de registrar tu usuario, este comando servira para poder utilizar todas las funciones del bot.
        \n**/equipo**: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Mostrará la información del equipo.
        \n**/partidos**: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Mostrará los siguientes 3 partidos del equipo.
        \n**/grupo**: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Muestra la información detallada del grupo.
        \n**/help**: Guía de uso del bot.
        ''')


client.run(os.environ['TOKEN'])
