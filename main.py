import discord
from discord import ui, app_commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ====================== YOUR SCHEMATICS ======================
SCHEMATICS = {
    "Charcoal Farms": {
        "CoalBonker V1 Fixed": "schematics/Charcoal Farms/CoalBonker V1 Fixed.litematic",
        "Knoster_Charcoal_V1_1": "schematics/Charcoal Farms/Knoster_Charcoal_V1_1.litematic",
        "Mauschu_s_Charcoal_smelter": "schematics/Charcoal Farms/Mauschu_s_Charcoal_smelter.litematic",
        "Becksters Charcoal Farm": "schematics/Charcoal Farms/Becksters Charcoal Farm.litematic",
    },
    "Zarz's Farms": {
        "Zarz's Tnt Minecart META v1": "schematics/Zarz's Farms/Zarz's Tnt Minecart META v1.litematic",
    },
}

@client.event
async def on_ready():
    print(f'✅ Bot is online as {client.user}')
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@tree.command(name="vault", description="Open the Schematics Vault")
async def vault(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🟠 Becksters Hood Schematics — Schematics Vault",
        description="**Grab a schematic**\nEverything you need to build  farms, ready to import in one click.",
        color=0xFF7F00
    )
    embed.add_field(
        name="How to use:",
        value="1️⃣ Pick a category in the menu below\n"
              "2️⃣ Pick a schematic from that category\n"
              "3️⃣ Get the file instantly, sent privately to you",
        inline=False
    )
    embed.set_footer(text="Becksters Hood • Schematics Vault")
    
    await interaction.response.send_message(embed=embed, view=CategoryView())

class CategoryView(ui.View):
    @ui.select(
        placeholder="Select Category",
        options=[
            discord.SelectOption(label="Charcoal Farms", value="Charcoal Farms", emoji="⚫"),
            discord.SelectOption(label="Zarz's Farms", value="Zarz's Farms", emoji="🎲"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: ui.Select):
        category = select.values[0]
        options = [discord.SelectOption(label=name, value=name) for name in SCHEMATICS[category].keys()]
        
        embed = discord.Embed(
            title=f"📁 {category}",
            description="Choose a schematic to download",
            color=0xFF7F00
        )
        
        dm_msg = await interaction.user.send(embed=embed, view=SchematicView(category, options))
        await interaction.response.send_message("✅ Check your DMs!", ephemeral=True)
        
        asyncio.create_task(auto_delete(dm_msg, 60))

class SchematicView(ui.View):
    def __init__(self, category: str, options: list):
        super().__init__()
        self.category = category
        self.select_schematic.options = options

    @ui.select(placeholder="Choose a schematic to download")
    async def select_schematic(self, interaction: discord.Interaction, select: ui.Select):
        schematic_name = select.values[0]
        file_path = SCHEMATICS[self.category][schematic_name]

        if os.path.exists(file_path):
            file = discord.File(file_path, filename=os.path.basename(file_path))
            download_msg = await interaction.user.send(f"**{schematic_name}** - Download:", file=file)
            
            await interaction.response.send_message("✅ Sent! (Auto-deletes in 60s)", ephemeral=True)
            
            asyncio.create_task(auto_delete(download_msg, 60))
        else:
            await interaction.response.send_message("❌ File not found.", ephemeral=True)

async def auto_delete(message, seconds: int):
    await asyncio.sleep(seconds)
    try:
        await message.delete()
    except:
        pass

# ====================== RUN THE BOT ======================
token = os.getenv("TOKEN")
if not token:
    token = "MTUyNTc2Mzc0ODI5NDI5OTY1OA.G_hvr9.Z-LpYzrtBp9aKmax8BwrrK5ha5G2GicIWEoyLw"
if token:
    client.run(token)
else:
    print("❌ TOKEN environment variable not found!")
