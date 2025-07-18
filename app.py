import discord
from discord import app_commands
from discord.ui import View, Select, Modal, TextInput
import os
import datetime

ultima_avaliacao = {}
LIMITE_DIAS = 30

class BotLds(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="/",
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print("O Bot{self.user} foi ligado com sucesso.")
    

bot = BotLds()

@bot.tree.command(name="lua_de_sangue",description="Lua de sangue ")
async def lua(interaction:discord.Interaction):
    await interaction.response.send_message(f"A lua será dia, {interaction.user.mention}")



# ----- FEEDBACK SELECT -----
class FeedbackSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="⭐ 1 Estrela", value="1"),
            discord.SelectOption(label="⭐⭐ 2 Estrelas", value="2"),
            discord.SelectOption(label="⭐⭐⭐ 3 Estrelas", value="3"),
            discord.SelectOption(label="⭐⭐⭐⭐ 4 Estrelas", value="4"),
            discord.SelectOption(label="⭐⭐⭐⭐⭐ 5 Estrelas", value="5"),
        ]
        super().__init__(placeholder="Escolha uma nota", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        rating = self.values[0]
        modal = FeedbackModal(rating)
        await interaction.response.send_modal(modal)

class FeedbackView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FeedbackSelect())

# ----- FEEDBACK MODAL -----
class FeedbackModal(Modal):
    def __init__(self, rating):
        super().__init__(title=f"Feedback ⭐ {rating} estrela(s)")
        self.rating = rating
        self.comment = TextInput(label="Comentário", required=True, style=discord.TextStyle.paragraph)
        self.add_item(self.comment)

    # TEMPO PARA VOTAR
async def on_submit(self, interaction: discord.Interaction):
    user_id = interaction.user.id
    agora = datetime.datetime.now()

    # Verifica se o usuário já enviou nos últimos 30 dias
    if user_id in ultima_avaliacao:
        ultima_data = ultima_avaliacao[user_id]
        dias_passados = (agora - ultima_data).days

        if dias_passados < LIMITE_DIAS:
            proxima_data = ultima_data + datetime.timedelta(days=LIMITE_DIAS)
            restante = (proxima_data - agora).days
            await interaction.response.send_message(
                f"❌ Você já enviou um feedback. Pode enviar outro em {restante} dia(s).",
                ephemeral=True
            )
            return

        canal_feedback = interaction.guild.get_channel(1395581701987766468)
        if canal_feedback:
            embed = discord.Embed(title="📝 Novo Feedback", color=discord.Color.blue())
            embed.add_field(name="Usuário", value=interaction.user.mention, inline=True)
            embed.add_field(name="Nota", value=f"{'⭐' * int(self.rating)} ({self.rating}/5)", inline=True)
            embed.add_field(name="Comentário", value=self.comment.value or "*Sem comentário*", inline=False)
            embed.set_footer(text="Feedback Lendários")
            await canal_feedback.send(embed=embed)

        await interaction.response.send_message(f"✅ Obrigado pelo seu feedback, {interaction.user.mention}!")


# ----- COMANDO SLASH -----
@bot.tree.command(name="feedback", description="Enviar feedback sobre o atendimento")
async def feedback(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Deixe sua avaliação",
        view=FeedbackView(),
         )

# Token do bot (use variável de ambiente)
bot.run(os.getenv('DISCORD_TOKEN'))
