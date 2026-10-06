import discord
from discord.ext import commands
import random

# ตั้งค่า Intent ของบอท
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# รวมฐานข้อมูลตัวละครไว้ในไฟล์นี้ไฟล์เดียวจบ!
# ==========================================
char_data = {
    "three_stars": [
        { "name": "Arona", "rarity": 3, "image": "https://i.imgur.com/example1.png" },
        { "name": "Shiroko", "rarity": 3, "image": "https://i.imgur.com/example2.png" },
        { "name": "Hoshino", "rarity": 3, "image": "https://i.imgur.com/example3.png" }
    ],
    "two_stars": [
        { "name": "Serina", "rarity": 2, "image": "https://i.imgur.com/example4.png" },
        { "name": "Suzumi", "rarity": 2, "image": "https://i.imgur.com/example5.png" }
    ],
    "one_stars": [
        { "name": "Juri", "rarity": 1, "image": "https://i.imgur.com/example6.png" }
    ]
}

# ฟังก์ชันสุ่มตัวละคร 1 ตัว (3 ดาว 3%, 2 ดาว 20%, 1 ดาว 77%)
def roll_character():
    roll = random.random()
    if roll < 0.03 and char_data["three_stars"]:
        return random.choice(char_data["three_stars"]), 3
    elif roll < 0.23 and char_data["two_stars"]:
        return random.choice(char_data["two_stars"]), 2
    else:
        if char_data["one_stars"]:
            return random.choice(char_data["one_stars"]), 1
        else:
            return random.choice(char_data["two_stars"]), 2

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (Arona Gacha System Ready!)')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# คำสั่งเปิดกาชา: พิมพ์ /gacha แล้วเลือก 1 หรือ 10 ครั้ง
@bot.tree.command(name="gacha", description="สุ่มตู้กาชาอาโรน่า (เลือก 1 หรือ 10 ครั้ง)")
async def gacha(interaction: discord.Interaction, count: int):
    if count not in [1, 10]:
        await interaction.response.send_message("พี่คะ! เลือกสุ่มได้แค่แบบ **1 ครั้ง** หรือ **10 ครั้ง** เท่านั้นนะคะ!", ephemeral=True)
        return

    await interaction.response.defer() # รอประมวลผล

    results = []
    has_rainbow = False

    for _ in range(count):
        char, rarity = roll_character()
        results.append(char)
        if rarity == 3:
            has_rainbow = True

    # สร้าง Embed แสดงผลลัพธ์
    if has_rainbow:
        embed_color = 0xFFD700 # สีทอง/รุ้งเมื่อออก 3 ดาว
        title_text = "✨ [Rainbow Envelope] แฟ้มสีรุ้งออกแล้วค่ะพี่!"
    else:
        embed_color = 0x3498DB # สีฟ้าปกติ
        title_text = "📦 ผลการสุ่มกาชาจากอาโรน่าค่ะ!"

    embed = discord.Embed(title=title_text, color=embed_color)
    
    description_list = []
    for idx, c in enumerate(results, 1):
        stars = "⭐" * c["rarity"]
        description_list.append(f"**{idx}. {c['name']}** ({stars})")

    embed.description = "\n".join(description_list)
    embed.set_footer(text=f"ผู้สุ่ม: {interaction.user.name} | ระบบกาชาอาโรน่า")

    # ถ้ารูปแบบสุ่ม 1 ครั้งแล้วได้ตัว 3 ดาว ให้ดึงรูปมาโชว์ด้วย
    if count == 1 and results[0]["rarity"] == 3:
        embed.set_image(url=results[0]["image"])
        embed.set_thumbnail(url=results[0]["image"])

    await interaction.followup.send(embed=embed)

# อย่าลืมใส่ Token ของบอทในช่อง Environment Variables บน Render นะครับ
# bot.run("YOUR_BOT_TOKEN")
