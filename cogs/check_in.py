import typing
import csv
import json
from dataclasses import dataclass, asdict

import discord
from discord.ext import commands


@dataclass()
class BotConfig:
    csv: bytes
    listen_channel: str
    column: int
    add_roles: typing.List[str]
    discard_roles: typing.List[str]
    goto_channel: str

FILE = 'file.csv'
FILE_CONTENTS = None

try:
    with open(FILE, 'rb') as f:
        FILE_CONTENTS = f.read()
except FileNotFoundError:
    FILE_CONTENTS = None

default_config = BotConfig(FILE_CONTENTS, 'check-in', 0, ['noauth'], ['no-check'], 'codigo-de-conducta')


class CheckIn(commands.Cog):

    def __init__(self, client, config: BotConfig = default_config):
        self.client = client
        self.emails = set()
        self.config = config

        if self.config.csv:
            self.refresh()

    def refresh(self):
        reader = csv.reader(self.config.csv.decode("utf-8").split('\n'))

        # Ignore first line, containing headers.
        reader.__next__()

        for row in reader:
            if len(row) > self.config.column:
                self.emails.add(row[self.config.column].lower().strip())

    @commands.command()
    async def start(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("Solo los administradores pueden ejecutar este comando.")
            return

        if not self.config.csv:
            await ctx.send(f"Es necesario subir un CSV para que el bot pueda trabajar.")
            return

        self.refresh()
        await ctx.send(f"Se ha (re)iniciado el bot.")

    @commands.command()
    async def new_csv(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("Solo los administradores pueden ejecutar este comando.")
            return

        if len(ctx.message.attachments) > 1:
            await ctx.send(f"¡Error! Debes mandar un solo archivo CSV.")

        self.config.csv = await ctx.message.attachments[0].read()

        with open(FILE, 'wb') as f:
            f.write(self.config.csv)

        await ctx.send(f"Archivo recibido exitosamente.")

    @commands.command()
    async def set_config(self, ctx, key: str, *values: typing.Union[discord.Role, discord.TextChannel, int]):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("Solo los administradores pueden ejecutar este comando.")
            return

        if key == 'listen_channel':
            self.config.listen_channel = values[0].name
        elif key == 'column':
            self.config.column = values[0]
        elif key == 'add_roles':
            self.config.add_roles = [role.name for role in values]
        elif key == 'discard_roles':
            self.config.discard_roles = [role.name for role in values]
        elif key == 'goto_channel':
            self.config.listen_channel = values[0].name
        else:
            await ctx.send(f"Configuración inválida.")

        format_str = ','.join([str(v) for v in values])
        await ctx.send(f"Se ha redefinido la configuración, con llave {key} y valor {format_str}")

    @commands.command()
    async def view_config(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("Solo los administradores pueden ejecutar este comando.")
            return

        temp_config = asdict(self.config)
        del temp_config['csv']

        json_config = json.dumps(temp_config)
        await ctx.send(f"La configuración es:\n{json_config}")

    @commands.command()
    async def check(self, ctx, email: str):
        # Preconditions
        if ctx.channel.name != self.config.listen_channel:
            return

        await ctx.message.delete()
        email = email.strip()

        if email == '':
            await ctx.send(f"No ingresaste un correo válido, {ctx.author.mention}")
            return

        # Contract
        if email.lower() in self.emails:
            new_roles  = [discord.utils.get(ctx.guild.roles, name=r) for r in self.config.add_roles]
            past_roles = [discord.utils.get(ctx.guild.roles, name=r) for r in self.config.discard_roles]

            for role in new_roles:
                await ctx.message.author.add_roles(role)

            for role in past_roles:
                await ctx.message.author.remove_roles(role)

            channel = discord.utils.get(ctx.guild.channels, name=self.config.goto_channel)
            await ctx.send(f"¡Bienvenid@ {ctx.message.author.mention}! Por favor, dirígete al canal {channel.mention}.")

        else:
            await ctx.send(f"{ctx.author.mention}, el email que ingresaste no está registrado. Vuelve a intentarlo, o contacta a un administrador.")
