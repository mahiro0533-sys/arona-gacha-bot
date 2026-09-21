import os
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# --- ระบบเชื่อมต่อเว็บเซิร์ฟเวอร์สแตนด์บายสำหรับ Render ---
class AronaKeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Arona Gacha System is online and ready!")
        except Exception:
            pass

def launch_web_server():
    assigned_port = int(os.environ.get("PORT", 10000))
    try:
        web_server = HTTPServer(("0.0.0.0", assigned_port), AronaKeepAliveHandler)
        web_server.serve_forever()
    except Exception as err:
        print(f"Keep-Alive Server Alert: {err}")

background_worker = Thread(target=launch_web_server)
background_worker.daemon = True
background_worker.start()
# --------------------------------------------------------

import discord
from discord.ext import commands

# ฐานข้อมูลรายชื่อตัวละคร (ตัวอย่างโครงสร้าง สามารถเพิ่มรายชื่อตัวละครอื่นๆ เข้าไปได้อิสระ)
BA_DATABASE = {
    3: [
        {"name": "Hina (Swimsuit)", "icon": "https://static.wikia.nocookie.net/bluearchive/images/c/c8/Hina_%28Swimsuit%29.png"},
        {"name": "Shiroko (Riding)", "icon": "https://static.wikia.nocookie.net/bluearchive/images/9/98/Shiroko_%28Riding%29.png"},
        {"name": "Hoshino (Combat)", "icon": "https://static.wikia.nocookie.net/bluearchive/images/e/ef/Hoshino_%28Combat%29.png"},
    ],
    2: [
        {"name": "Serina", "icon": "https://static.wikia.nocookie.net/bluearchive/images/f/f6/Serina.png"},
        {"name": "Chise", "icon": "https://static.wikia.nocookie.net/bluearchive/images/7/7b/Chise.png"},
        {"name": "Akari", "icon": "https://static.wikia.nocookie.net/bluearchive/images/3/30/Akari.png"},
    ],
    1: [
        {"name": "Juri", "icon": "https://static.wikia.nocookie.net/bluearchive/images/1/1d/Juri.png"},
        {"name": "Kotama", "icon": "https://static.wikia.nocookie.net/bluearchive/images/5/52/Kotama.png"},
        {"name": "Pina", "icon": "https://static.wikia.nocookie.net/bluearchive/images/5/5a/Pina.png"},
    ]
}

# ฟังก์ชันสุ่มเรทกาชาเฉพาะตัวของระบบน้องอารานะ
def execute_gacha_roll():
    rate_check = random.random() * 100
    if rate_check < 3.0:
        return random.choice(BA_DATABASE[3]), 3
    elif rate_check < 21.5:
        return random.choice(BA_DATABASE[2]), 2
    else:
        return random.choice(BA_DATABASE[1]), 1

# --- ระบบปุ่มกดอินเตอร์แอคทีฟ (Arona Interactive View) ---
class AronaGachaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎲 เปิดตู้ 1 ครั้ง", style=discord.ButtonStyle.primary, custom_id="arona_pull_single")
    async def click_single_pull(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        status_msg = await interaction.followup.send("✨ (อารานะกำลังตระเตรียมซองจดหมายและตรวจเช็กเรทตู้ให้คุณพี่ค่ะ...)\nhttps://media.giphy.com/media/3o7TKSjRrfIPjeiOkM/giphy.gif")
        
        time.sleep(2)
        
        target_char, star_count = execute_gacha_roll()
        star_display = "⭐" * star_count
        
        result_embed = discord.Embed(
            title=f"🌸 ผลลัพธ์การสุ่ม (1 ครั้ง) - น้องอารานะจัดให้!",
            description=f"**{target_char['name']}** ({star_display})",
            color=0xFFD700 if star_count == 3 else (0xC0C0C0 if star_count == 2 else 0xCD7F32)
        )
        result_embed.set_thumbnail(url=target_char['icon'])
        result_embed.set_footer(text=f"ท่านผู้บัญชาการที่เปิดตู้: {interaction.user.name}")
        
        await status_msg.edit(content=None, embed=result_embed, view=self)

    @discord.ui.button(label="🎉 เปิดตู้ 10 ครั้งรวด", style=discord.ButtonStyle.success, custom_id="arona_pull_multi")
    async def click_multi_pull(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        status_msg = await interaction.followup.send("🌟 (อารานะกำลังเปิดแฟ้มชุดใหญ่ ลุ้นระทึกตื่นเต้นสุดๆ ไปเลยค่ะ!)\nhttps://media.giphy.com/media/3o7TKSjRrfIPjeiOkM/giphy.gif")
        
        time.sleep(2.5)
        
        batch_results = [execute_gacha_roll() for _ in range(10)]
        
        summary_desc = ""
        is_hit_three_star = False
        for target_char, star_count in batch_results:
            if star_count == 3:
                is_hit_three_star = True
                summary_desc += f"✨ **{target_char['name']}** ({'⭐'*star_count}) [ออกตัวท็อป!]\n"
            else:
                summary_desc += f"{target_char['name']} ({'⭐'*star_count})\n"

        result_embed = discord.Embed(
            title=f"🍀 ผลลัพธ์การสุ่ม (10 ครั้ง) ของ {interaction.user.name}",
            description=summary_desc,
            color=0xFF4500 if is_hit_three_star else 0x1E90FF
        )
        result_embed.set_footer(text="ระบบจำลองกาชา Blue Archive ฉบับพิเศษโดยอารานะ")
        
        await status_msg.edit(content=None, embed=result_embed, view=self)

bot_setup_intents = discord.Intents.default()
bot_setup_intents.message_content = True
arona_bot = commands.Bot(command_prefix="!", intents=bot_setup_intents)

@arona_bot.event
async def on_ready():
    print(f"🚀 น้องอารานะ บอทสุ่มกาชา เชื่อมต่อระบบสำเร็จเรียบร้อยแล้วจ้า! ({arona_bot.user})")

@arona_bot.command(name="gacha")
async def invoke_gacha_menu(context):
    panel_embed = discord.Embed(
        title="🎴 เมนูจำลองสุ่มตู้กาชา Blue Archive",
        description="กดปุ่มด้านล่างเพื่อเสี่ยงโชคเปิดตู้กับน้องอารานะได้เลยนะคะคุณพี่!",
        color=0x00BFFF
    )
    panel_embed.set_footer(text="ระบบเรทสุ่มมาตรฐาน ชวนลุ้นทุกการกด")
    await context.send(embed=panel_embed, view=AronaGachaView())

# ดึง Token ลับสำหรับบอทน้องอารานะ
BOT_SECRET_TOKEN = os.environ.get("DISCORD_TOKEN")
if BOT_SECRET_TOKEN:
    arona_bot.run(BOT_SECRET_TOKEN)
else:
    print("❌ Critical Error: ไม่พบค่า DISCORD_TOKEN ในระบบ Environment Variables โปรดตรวจสอบการตั้งค่าบน Render อีกครั้งครับ!")
