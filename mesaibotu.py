import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import pandas as pd
import sqlite3
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
DB_NAME = "mesai.db"
aktif_mesailer = {} 

def db_kur():
   
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS mesailer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_ad TEXT,
                kullanici_id INTEGER,
                tarih TEXT,
                giris_saati TEXT,
                cikis_saati TEXT,
                toplam_sure TEXT
            )
        ''')
        conn.commit()

db_kur()

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')

@bot.command()
@commands.has_permissions(administrator=True) 
async def panel(ctx):
    embed = discord.Embed(
        title="Kurumsal Mesai Takip",
        description="Mesaiye başlamak için ✅, bitirmek için ❌ emojisine tıklayın.",
        color=0xffd700 
    )
    embed.set_footer(text="Admin: !excel, !temizle")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    
    
    try:
        msg = await channel.fetch_message(payload.message_id)
        await msg.remove_reaction(payload.emoji, member)
    except:
        pass

    emoji = str(payload.emoji)

    if emoji == "✅":
        if payload.user_id not in aktif_mesailer:
            now = datetime.now()
            aktif_mesailer[payload.user_id] = now
            m = await channel.send(f"🟢 {member.mention} mesaiye başladı ({now.strftime('%H:%M:%S')})")
            await asyncio.sleep(5)
            await m.delete()
        else:
            await channel.send(f"⚠️ {member.mention} zaten aktif bir mesain var.", delete_after=5)

    elif emoji == "❌":
        if payload.user_id in aktif_mesailer:
            baslangic = aktif_mesailer.pop(payload.user_id)
            bitis = datetime.now()
            sure = bitis - baslangic
            
            saniye = int(sure.total_seconds())
            saat, kalan = divmod(saniye, 3600)
            dakika, sn = divmod(kalan, 60)
            sure_str = f"{saat:02d}:{dakika:02d}:{sn:02d}"

            
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute('''
                    INSERT INTO mesailer (kullanici_ad, kullanici_id, tarih, giris_saati, cikis_saati, toplam_sure)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (member.display_name, member.id, baslangic.strftime("%d.%m.%Y"), 
                      baslangic.strftime("%H:%M:%S"), bitis.strftime("%H:%M:%S"), sure_str))
                conn.commit()

            embed = discord.Embed(title="Mesai Bitti", color=0x00ff00)
            embed.add_field(name="Giriş", value=baslangic.strftime("%H:%M:%S"))
            embed.add_field(name="Çıkış", value=bitis.strftime("%H:%M:%S"))
            embed.add_field(name="Süre", value=f"**{sure_str}**", inline=False)
            await channel.send(embed=embed)
        else:
            await channel.send(f"❓ {member.mention} önce mesai başlatmalısın.", delete_after=5)

@bot.command()
@commands.has_permissions(administrator=True)
async def excel(ctx):
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("SELECT * FROM mesailer", conn)

    if df.empty:
        await ctx.send("Kayıtlı veri bulunamadı.")
        return

    dosya = "rapor.xlsx"
    df.to_excel(dosya, index=False)
    await ctx.send(f"{ctx.author.mention} rapor ektedir:", file=discord.File(dosya))
    os.remove(dosya)

@bot.command()
@commands.has_permissions(administrator=True)
async def temizle(ctx):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM mesailer")
        conn.commit()
    await ctx.send("Veritabanı temizlendi.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Bunu yapmak için yetkin yok {ctx.author.mention}", delete_after=5)


bot.run('your_token')