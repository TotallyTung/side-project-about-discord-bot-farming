# REQUIREMENT: discord.py-self, win10toast
import discord
from discord.ext import tasks
from win10toast import ToastNotifier

notifier = ToastNotifier()
captchaFilter = ["captcha", "resul​t i​n a​ ban", "ar​e yo​u a​ rea​l huma​n"]

class Farm(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.isfarm = False
		self.cid = None
	
	async def on_ready(self):
		print("Logged in as", self.user)
	
	@tasks.loop(seconds=15)
	async def farmTask(self, ctx):
		await ctx.send("owohunt")
		await ctx.send("owobattle")
		
	async def on_message(self, msg):
		ctx = msg.channel
		if msg.author.id == 408785106942164992 and msg.channel.id == self.cid:
			if any(check in msg.content for check in captchaFilter) and self.isfarm:
				self.farmTask.cancel()
				print("[!] Captcha detected!")
				r = await ctx.send(f"<@{str(self.user.id)}>")
				await r.unack()
				del r
				notifier.show_toast(title="OwO Farm", msg="Please verify the captcha and start again.", duration=20, threaded=True)
	
		if msg.author == self.user and msg.content.lower()[:2] == "b.":
			cmd=msg.content[2:].strip()
			cargs=cmd.split(" ")[1:]
			await msg.delete()
			match cmd:
				case "start":
					if not self.cid:
						await ctx.send("> **Use b.channel _<channel\_id>_ to set channel.**")
					elif not self.isfarm:
						print("[!] Started.")
						self.isfarm = True
						self.farmTask.start(self.get_channel(self.cid))
						await ctx.send("> **Started.**")
				case "stop":
					if self.isfarm:
						print("[!] Stopped")
						self.isfarm = False
						self.farmTask.cancel()
						await ctx.send("> **Stopped.**")
					else:
						await ctx.send("> **Bot is not running.**")
				case "channel":
					self.cid = int(cargs[0]) if cargs else msg.channel.id
					await ctx.send(f"> **Set channel to** <#{msg.channel.id}>")
				case "help":
					await ctx.send("""> # **LIST OF COMMANDS**
> ### **+)** `b.channel` _[channel\_id]_
> _Set current channel or channel in argument for farming._
> ### **+)** `b.start`
> _Start farming._
> ### **+)** `b.stop`
> _Stop farming._
> ### **+)** `b.help`
> _Help_""")

client = Farm()
client.run("token here")
