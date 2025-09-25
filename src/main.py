import asyncio
import discord
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.env import load_environment_variables
from .core.bot import MyBot
from .core.commands import MyCommands

DISCORD_TOKEN = load_environment_variables()

comms = MyCommands()
bot = MyBot()

app = FastAPI(
    title="Axion Server",
    version="1.0.0",
    description="Discord AI Agent Backend",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Slash command: /talk
# @comms.tree.command(name="talk", description="Chat casually with Axion")
# async def talk(interaction: discord.Interaction, message: str):
#     print("Casual Mode Activated")
#     query = bot.casual_chat(message=message)
#     await interaction.response.send_message(query[:1999])


# Slash command: /define
@comms.tree.command(
    name="define", description="Get information about any topic worldwide"
)
async def define(interaction: discord.Interaction, message: str):
    print("Info Mode Activated")
    query = bot.informative(message=message)
    await interaction.response.send_message(query[:1999])


# Slash command: /g-code
@comms.tree.command(name="g-code", description="Generate code snippets with Axion")
async def g_code(interaction: discord.Interaction, message: str):
    print("Code Mode Activated")

    # Prevent timeout (acknowledge immediately)
    await interaction.response.defer()

    try:
        # Call your Axion coding function
        query = bot.coding(message=message)

        # Send follow-up (safely under 2000 chars for Discord)
        await interaction.followup.send(query[:1900])
    except Exception as e:
        # Always reply, even on error
        await interaction.followup.send(f"❌ Error: {str(e)}")


@comms.event
async def on_ready():
    print(f"✅ Logged in as {comms.user}")


@comms.event
async def on_message(message):
    print(message.author)
    if message.author == comms.user:
        return

    if message.content.startswith("!summon"):
        query = message.content.replace("!summon", "").strip()
        if not query:
            await message.channel.send(
                "❓ Please provide a question, e.g. `!summon What is AI?`"
            )
            return

        await message.channel.send("💡 Thinking...")
        reply = bot.generalized(query, user=message.author.name)
        await message.channel.send(reply[:1999])  # type: ignore  # Discord message limit ~2000 chars
        print("✅ Response sent.")


# Run Discord comms in FastAPI's lifecycle
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(comms.start(DISCORD_TOKEN))  # type: ignore


@app.get("/")
async def read_root():
    return {"Hello": "World"}
