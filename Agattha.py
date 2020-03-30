 import discord
import typing
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

burp = commands.Bot(command_prefix="$")
my_token = "NjkxNDIwOTQxNzU4MjM0NzI1.Xnfulg.bdBclc9sp7NP4-w9m9OQywW5jME"
burp.remove_command("help")


@burp.event
async def on_ready():
	await burp.change_presence(status=discord.Status.idle, activity=discord.Game("Meu prefixo é $"))
	print(f"Id do bot: {burp.user.id}")
	print(f"Nome do bot: {burp.user.name}")
	print("-"*30)


@burp.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não há este comando em minha programação, caso esteja com dificuldades use o comando help")


@burp.event
async def on_member_join(member):
	await burp.get_channel(689527314089771016).send(f"{member.mention} entrou no servidor.")


@burp.event
async def on_member_remove(member):
	await burp.get_channel(689527314089771016).send(f"{member.mention} saiu do servidor.")


@burp.command(aliases=["purge", "limpar", "clean"])
@has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
	if amount == 0:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém eu não consigo limpar o chat sem uma certa quantidade de mensagens desejadas para limpar.")
		
	elif amount <= 1:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, mas eu só limpo de 2 a 100 mensagens")
	
	elif amount >= 101:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, mas eu só limpo de 2 a 100 mensagens")
		
	else:
		await ctx.channel.purge(limit=amount+1)
		await ctx.send(f"{ctx.author.mention} limpou o chat")
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser limpar este chat, você precisará da permissão ``Gerenciar mensagens``")


@burp.command(aliases=["hackban", "forceban", "banir"])
@has_permissions(ban_members=True)
async def ban(ctx, member: typing.Union[discord.Member, int]=None, *, reason=None):
	if type(member) == discord.Member:
		await member.ban(reason=f"{ctx.author} baniu com o motivo {reason}")
		teste=discord.Embed(title="Usuário punido com sucesso", color=0x690FC3)
		teste.add_field(name="Usuário punido", value=f"```{member}```")
		teste.add_field(name="Punido por", value=f"```{ctx.author.name}```")
		teste.add_field(name="Motivo", value=f"```{reason}```")
		teste.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=teste)
	
	elif member == None:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível banir alguém sem mencioná-la ou por o id dela no comando")
	
	else:
		banned_users = await ctx.guild.bans()
		for banned_member in banned_users:
			user = banned_member.user
			if user.id == member:
				await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível banir este membro no momento porque ele já está banido deste server, cheque os batimentos deste server")
				return
		await ctx.message.guild.ban(discord.Object(id=member))
		teste=discord.Embed(title="Usuário punido com sucesso", color=0x690FC3)
		teste.add_field(name="Id do usuário", value=f"```{member}```")
		teste.add_field(name="Punido por", value=f"```{ctx.author.name}```")
		teste.add_field(name="Motivo", value=f"```{reason}```")
		teste.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=teste)
@ban.error
async def ban_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser banir este membro, você precisará da permissão ``banir membros``")


@burp.command()
async def avatar(ctx, member: discord.Member=None):
	
	if member == None:
		avatar_embed = discord.Embed(
			title = "Aqui está seu avatar",
			color = 0x690FC3
		)
		avatar_embed.set_image(url=ctx.author.avatar_url)
		avatar_embed.set_author(name="Que foto linda")
		
		await ctx.send(embed=avatar_embed)
	else:
		embed = discord.Embed(
			title = f"Avatar de {member}",
			color = 0x690FC3
		)
		embed.set_image(url=member.avatar_url)
		embed.set_author(name="Que foto linda")
		
		await ctx.send(embed=embed)


@burp.command()
async def userinfo(ctx, member: discord.Member=None):
	
	if member == None:
		member = ctx.author
		
		roles = [role for role in member.roles]
	
		roles = []
		for role in member.roles:
			roles.append(role)
		
		embed = discord.Embed(
			title = f"<:emoji_16:690961915228323931> Informações de {member.name}",
			color = 0x690FC3,
			timestamp = ctx.message.created_at
		)
	
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"Convocado por {ctx.author}", icon_url=ctx.author.avatar_url)
	
		embed.add_field(name="💻 ID:", value=f"``{member.id}``")
		embed.add_field(name="📖 Nome e discriminator:", value=f"``{member}``")
	
		embed.add_field(name="📅 Conta criada em:", value=member.created_at.date())
		embed.add_field(name="📆 Entrou em:", value=member.joined_at.date())
	
		embed.add_field(name=f"💼 Cargos ({len(roles)})", value=" ".join(role.mention for role in roles))
		embed.add_field(name="💼 Maior cargo:", value=member.top_role.mention)
	
		embed.add_field(name="🤖 Bot?", value=member.bot)
		await ctx.send(embed=embed)
	
	else:
		embed = discord.Embed(
			title = f"<:emoji_16:690961915228323931> Informações de {member.name}",
			color = 0x690FC3,
			timestamp = ctx.message.created_at
		)
	
		roles = [role for role in member.roles]
	
		roles = []
		for role in member.roles:
			roles.append(role)
	
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"Convocado por {ctx.author}", icon_url=ctx.author.avatar_url)
	
		embed.add_field(name="💻 ID:", value=f"``{member.id}``")
		embed.add_field(name="📖 Nome e discriminator:", value=f"``{member}``")
	
		embed.add_field(name="📅 Conta criada em:", value=member.created_at.date())
		embed.add_field(name="📆 Entrou em:", value=member.joined_at.date())
	
		embed.add_field(name=f"💼 Cargos ({len(roles)})", value=" ".join(role.mention for role in roles))
		embed.add_field(name="💼 Maior cargo:", value=member.top_role.mention)
	
		embed.add_field(name="🤖 Bot?", value=member.bot)
		await ctx.send(embed=embed)


@burp.command()
async def ping(ctx):
	embed = discord.Embed(
		title="Meu ping",
		color=0x690FC3
	)
	embed.set_footer(text=f"{round(burp.latency * 1000)}ms")
	await ctx.send(embed=embed)


@burp.command(aliases=["falar"])
async def say(ctx, *, words):
	await ctx.send(words)
@say.error
async def user_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém você precisa digitar algo para que eu possa falar")


@burp.command(aliases=["serverinfo"])
async def server_info(ctx):
	
	online = 0
	for i in ctx.guild.members:
		if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
			online += 1
			all_users = []
			for user in ctx.guild.members:
				all_users.append('{}#{}'.format(user.name, user.discriminator))
				all_users.sort()
				all = '\n'.join(all_users)
	channel_count = len([x for x in ctx.guild.channels if type(x) == discord.channel.TextChannel])
	channel_count2 = len([x for x in ctx.guild.channels if type(x) == discord.channel.VoiceChannel])
	total_canal = channel_count + channel_count2
	
	members = set(ctx.guild.members)
	bots = filter(lambda m: m.bot, members)
	bots = set(bots)
	users = members - bots
	

	
	
	embed = discord.Embed(
		title = f"<:emoji_15:690961050094534678> {ctx.guild.name}",
		color = 0x690FC3
	)
	embed.add_field(name = "💻 ID", value=f"``{ctx.guild.id}``")
	embed.add_field(name = "👑 Dono", value=f"``{ctx.guild.owner}`` ({ctx.guild.owner.id})")
	embed.add_field(name = "🌎 região", value=f"``{ctx.guild.region}``")
	embed.add_field(name = f"💬 Canais ({total_canal})", value=f"📄 ``Canais de texto {channel_count}``\n🔈`` Canais de voz {channel_count2}``")
	embed.add_field(name = "📅 Criado em", value=f"{ctx.guild.created_at.date()}")
	embed.add_field(name = "📆 Você entrou em", value=f"{ctx.author.joined_at.date()}")
	embed.add_field(name = f"👥 Membros ({ctx.guild.member_count})", value=f"<:emoji_11:690804302939160577> Online {online}")
	embed.set_thumbnail(url = ctx.guild.icon_url)
	
	await ctx.send(embed=embed)


@burp.command(aliases=["desbanir"])
async def unban(ctx, id: int, reason=None):
	user = await burp.fetch_user(id)
	await ctx.guild.unban(user, reason=f"{ctx.author} desbaniu com o motivo {reason}")
	unban_embed = discord.Embed(
		title = "Usuário desbanido com sucesso",
		color = 0x690FC3,
		timestamp = ctx.message.created_at
	)
	unban_embed.add_field(name="ID do usuário", value=f"```{user}```")
	unban_embed.add_field(name="Desbanido por", value=f"```{ctx.author}```")
	unban_embed.add_field(name="Motivo", value=f"```{reason}```")
	unban_embed.set_thumbnail(url=ctx.author.avatar_url)
			
	await ctx.send(embed=unban_embed)
@unban.error
async def unban_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser desbanir este membro, você precisará da permissão ``banir membros``")


@burp.command()
async def youtube(ctx, *, search):
	search_q = search.replace(' ', '%20')
	
	youtube = discord.Embed(
		title = "Pesquisa no Youtube",
		color = 0x690FC3,
		timestamp = ctx.message.created_at
	)
	youtube.set_author(name="Youtube", icon_url="https://i.imgur.com/RBJyzue.png")
	youtube.set_footer(text=f"Pesquisa do {ctx.author.name}", icon_url=ctx.author.avatar_url)
	
	youtube.add_field(name="Pesquisa", value="https://www.youtube.com/search?q=" + search_q)
	youtube.add_field(name="Pesquisado por", value=f"{ctx.author.name}")
	
	await ctx.send(embed=youtube)
@youtube.error
async def youtube_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível pesquisar algo sem digitar do que se trata a pesquisa")


@burp.command()
async def google(ctx, *, search):
	search_q = search.replace(' ', '%20')
	
	google = discord.Embed(
		title = "Pesquisa no google",
		color = 0x690FC3,
		timestamp = ctx.message.created_at
	)
	google.set_author(name="Google", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/2000px-Google_%22G%22_Logo.svg.png")
	google.set_footer(text=f"Pesquisa do {ctx.author.name}", icon_url=ctx.author.avatar_url)
	
	google.add_field(name="Pesquisa", value="https://www.google.com/search?q=" + search_q)
	google.add_field(name="Pesquisado por", value=f"{ctx.author.name}")
	
	await ctx.send(embed=google)
@google.error
async def google_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível pesquisar algo sem digitar do que se trata a pesquisa")


@burp.command(aliases=["expulsar"])
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
	if member == None:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível expulsar alguém sem mencioná-la.")
		
	else:
		await member.kick(reason=f"{ctx.author} o expulsou com o motivo {reason}")
		kick_embed = discord.Embed(
			title = "Usuário punido com sucesso",
			color = 0x690FC3
		)
		kick_embed.add_field(name="Usuário punido", value=f"```{member}```")
		kick_embed.add_field(name="Punido por", value=f"```{ctx.author}```")
		kick_embed.add_field(name="Motivo", value=f"```{reason}```")
		kick_embed.set_thumbnail(url=ctx.author.avatar_url)
		
		await ctx.send(embed=kick_embed)
@kick.error
async def kick_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser expulsar este membro, você precisará da permissão ``expulsar membros``")


@burp.command(aliases=["help"])
async def ajuda(ctx):
	await ctx.send("""```Administração
   ban 📌
   clear 📌
   kick 📌
   unban 📌
   mute 📌
   unmute 📌
   lock 📌
   unlock 📌
   softban 📌
Utilitários
   exemplo
   avatar
   userinfo
   serverinfo
   ping
   google 📌
   youtube 📌

Caso você esteja com dificuldade com alguns comando e precisa de exemplos, use $exemplo <nome dos comandos que estão com 📌>```""")

@burp.command(aliases=["mutar"])
@has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member=None, *, reason=None):
	
	role = discord.utils.get(ctx.guild.roles, name = "Muted")

	if role == None:
		
		role = await ctx.guild.create_role(name = "Muted", reason = "Bot Muted Role")
		
	elif member == None:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível mutar alguém sem mencioná-la")
	
	await member.add_roles(role)
	
	mute_embed = discord.Embed(
		title = "Usuário punido com sucesso",
		color = 0x690FC3
	)
	mute_embed.set_thumbnail(url=ctx.author.avatar_url)
	mute_embed.add_field(name="Usuário punido", value=f"```{member.name}```")
	mute_embed.add_field(name="Punido por", value=f"```{ctx.author.name}```")
	mute_embed.add_field(name="Motivo", value=f"```{reason}```")
	
	await ctx.send(embed=mute_embed)
			
	for channel in ctx.guild.channels:
		
		await channel.set_permissions(role, send_messages = False)
@mute.error
async def mute_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser mutar este membro, você precisará da permissão ``Gerenciar cargos``")


@burp.command(aliases=["desmutar"])
@has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member=None, reason=None):
	role = discord.utils.get(ctx.guild.roles, name = "Muted")
	
	if member == None:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível desmutar alguém sem mencioná-la")
	
	await member.remove_roles(role)
	mute_embed = discord.Embed(
		title = "Usuário desmutado com sucesso",
		color = 0x690FC3
	)
	mute_embed.set_thumbnail(url=ctx.author.avatar_url)
	mute_embed.add_field(name="Usuário desmutado", value=f"```{member.name}```")
	mute_embed.add_field(name="Desmutado por", value=f"```{ctx.author.name}```")
	mute_embed.add_field(name="Motivo", value=f"{reason}")
	await ctx.send(embed=mute_embed)
@unmute.error
async def unmute_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser desmutar este membro, você precisará da permissão ``Gerenciar cargos``")

	
@burp.command()
@has_permissions(manage_channels=True)
async def lock(ctx):
	
	role = discord.utils.get(ctx.guild.roles, name = "@everyone")
	
	for channel in ctx.guild.channels:
		
		await ctx.message.channel.set_permissions(role, send_messages=False)
	
	await ctx.send(f"🐻 | {ctx.author.mention} O canal foi bloqueado com sucesso. Caso queira desbloquea-lo use !unlock")
@lock.error
async def lock_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser bloquear este canal, você precisará da permissão ``Gerenciar canais``")


@burp.command()
@has_permissions(manage_channels=True)
async def unlock(ctx):
	
	role = discord.utils.get(ctx.guild.roles, name = "@everyone")
	
	for channel in ctx.guild.channels:
		
		await ctx.message.channel.set_permissions(role, send_messages=True)
	
	await ctx.send(f"🐻 | {ctx.author.mention} o canal foi desbloqueado com sucesso. Caso queira bloquear use !lock")
@unlock.error
async def unlock_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser bloquear este canal, você precisará da permissão ``Gerenciar canais``")


@burp.command()
@has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member=None, *, reason=None):
	if member == None:
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém não é possível usar softban em alguém sem mencioná-la no comando")
		
	try:
		await member.ban(reason=f"{ctx.author} baniu e com o motivo {reason}")
		await member.unban(reason=f"{ctx.author} desbaniu com o motivo {reason}")
		soft_embed = discord.Embed(
			title = "Usuário punido com sucesso",
			color = 0x690FC3
		)
		soft_embed.add_field(name="Usuário punido", value=f"```{member}```")
		soft_embed.add_field(name="Punido por", value=f"```{ctx.author}```")
		soft_embed.add_field(name="Motivo", value=f"```{reason}```")
		soft_embed.set_thumbnail(url=ctx.author.avatar_url)
		
		await ctx.send(embed=soft_embed)
		
	except discord.Forbidden:
		await ctx.send("Forbidden")
@softban.error
async def softban_error(ctx, error):
	if isinstance(error, MissingPermissions):
		await ctx.send(f"❌ | {ctx.author.mention} Desculpe-me, porém se quiser usar softban neste membro, você precisará da permissão ``Banir membros``")


@burp.command(aliases=["exemplo"])
async def ex(ctx, *, suggest):
	
	if suggest == "Ban" or "ban" and "BAN".strip():
		embed = discord.Embed(
			title = "🐻``$ban``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$hackban, $forceban, $banir__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$ban 691420941758234725``\n``$ban 691420941758234725 um motivo aleatória para o banir``\n``$ban @user um outro motivo``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não estiver dando ban em alguém, certifique-se que meu cargo não é menor do que o usuário a banir ou se eu tenho permissão para ``banir membros``\n🐻Caso você não tenha permissão para ``banir membros`` eu não irei banir o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "kick" or "Kick" and "KICK".strip():
		embed = discord.Embed(
			title = "🐻``$kick``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$expulsar__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$kick @user``\n``$kick @user um motivo aleatória para o expulsar``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não estiver expulsando alguém, certifique-se que meu cargo não é menor do que o usuário a expulsar ou se eu tenho permissão para ``expulsar membros``\n🐻Caso você não tenha permissão para ``expulsar membros`` eu não irei expulsar o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "clear" or "Clear" and "CLEAR".strip():
		embed = discord.Embed(
			title = "🐻``$clear``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$purge, $clean, $limpar__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$clear 45``\n``$clear 50``\n``$clear 100``\n``$clear 38``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não estiver limpando o chat, certifique-se que eu tenha permissão para ``Gerenciar mensagens``\n🐻Caso você não tenha permissão para ``gerenciar mensagens`` eu não irei limpar o chat")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "unban" or "Unban" and "UNBAN".strip():
		embed = discord.Embed(
			title = "🐻``$unban``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$desbanir__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$unban 691420941758234725``\n``$unban 691420941758234725 um motivo para retirar o ban``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não desbanir o usuário, certifique-se que eu tenha permissão para ``banir membros``\n🐻Caso você não tenha permissão para ``banir membros`` eu não irei banir o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "mute" or "Mute" and "MUTE".strip():
		embed = discord.Embed(
			title = "🐻``$mute``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$mutar__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$mute @user``\n``$mute @user um motivo para mutar``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não mutar o usuário, certifique-se de que eu tenha o cargo maior do que o dele e permissão para ``gerenciar cargo``\n🐻Caso você não tenha permissão para ``gerenciar cargos`` eu não irei mutar o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "unmute" or "Unmute" and "UNMUTE".strip():
		embed = discord.Embed(
			title = "🐻``$unmute``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__$desmutar__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$unmute @user``\n``$unmute @user um motivo para mutar``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não desmutar o usuário, certifique-se de que eu tenha o cargo mais alto do que o usuário e permissão para ``gerenciar cargos``\n🐻Caso você não tenha permissão para ``gerenciar cargos`` eu não irei desmutar o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	elif suggest == "softban" or "Softban" and "SOFTBAN".strip():
		embed = discord.Embed(
			title = "🐻``$softban``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__NENHUM ALIASES__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$softban @user``\n``$softban @user um motivo para banir e desbanir``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não banir e desbanir o usuário, certifique-se de que eu tenha o cargo maior do que o dele e permissão para ``banir membros``\n🐻Caso você não tenha permissão para ``banir membros`` eu não irei banir e desbanir o membro")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	elif suggest == "lock" or "Lock" and "LOCK".strip():
		embed = discord.Embed(
			title = "🐻``$lock``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__NENHUM ALIASE__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$lock``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não estiver bloqueando o chat, certifique-se de que eu tenha permissão para ``gerenciar canais``\n🐻Caso você não tenha permissão para ``gerenciar canais`` eu não irei bloquear o chat")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "unlock" or "Unlock" and "UNLOCK".strip():
		embed = discord.Embed(
			title = "🐻``$unlock``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__NENHUM ALIASE__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$unlock``")
		embed.add_field(name="🙅🏻‍♀️Possibilidade de pequenos erros", value="🙋🏻‍♀️ Se eu não desbloquear o canal, certifique-se de que eu tenha permissão para ``gerenciar canais``\n🐻Caso você não tenha permissão para ``gerenciar canais`` eu não irei desbloquear o chat")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)	
	
	elif suggest == "google" or "Google" and "GOOGLE".strip():
		embed = discord.Embed(
			title = "🐻``$google``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__NENHUM ALIASE__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$google facebook``")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	elif suggest == "youtube" or "Youtube" and "YOUTUBE".strip():
		embed = discord.Embed(
			title = "🐻``$youtube``",
			description = "Olá, está com dificuldades ou está confuso ao usar um comando? Este aqui te ajudará.",
			color = 0x690FC3
		)
		embed.add_field(name="📌Aliases", value="**__NENHUM ALIASE__**")
		embed.set_author(name="Agattha", icon_url="https://i.imgur.com/dj2G51b.jpg")
		embed.add_field(name="📝Exemplos", value="``$youtube ghostemane``")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
		
		await ctx.send(embed=embed)
	
	
	else:
		await ctx.send("Desculpe, porém não há exemplo deste comando")


@burp.command()
async def servericon(ctx):
	embed = discord.Embed(
		title = ctx.guild.name,
		color = 0x690FC3
	)
	embed.set_image(url=ctx.guild.icon_url)
	await ctx.send(embed=embed)


burp.run(my_token)
