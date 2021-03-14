import discord
import os
import time
from datetime import datetime
from discord.ext import tasks

#commands
from discord.ext import commands
from discord.ext.commands import Bot

bot = commands.Bot(command_prefix='$')

def log(message): #define logging function to prevent repeated code
		currentTime = str(datetime.now().time())
		print("["+currentTime+"] "+message)

def write(file,data): #function to write to file
	with open(file, 'w') as content: #save save slot
		content.write(str(data))
		return True

def read(file,backup):#read file function
	try: #load slot
		with open(file) as content: #save save slot
			return content.read()
	except OSError:
		write(file,backup)
		return backup

def isDigit(string):
	try:
		int(string)
		return True
	except:
		return False

number=read("number.txt",0)

log("started!")

@bot.command(pass_context=True,breif="reset count (only for admins)")
@commands.has_permissions(administrator=True)
async def reset(ctx):
	log("command resetted count")
	write("number.txt",1)
	await ctx.send("admin resetted count")

@bot.command(pass_context=True,breif="change count (only for admins)")
@commands.has_permissions(administrator=True)
async def changeNumber(ctx,number):
	log("command changed count")
	write("number.txt",number)
	await ctx.send("Admin changed count to "+str(number))

@bot.event
async def on_ready():
	log('We have logged in as {0.user}'.format(bot))
	log("current number is "+read("number.txt",0))

@bot.event
async def on_message(message):
	if message.author == bot.user: #makesure its not receiving own message 
		pass
	else:
		if isDigit(str(message.content)) and (message.channel.id==820158541310328883 or message.channel.id==819056076174655501):
			number=int(message.content)
			oldAuthor=read("oldAuthor.txt",None)
			if number==int(read("number.txt",0)):
				if str(message.author)==str(oldAuthor):
					write("number.txt",1)
					await message.channel.send("Aiyo! Greedy person send twice!! We are back at 1 leh!")
					oldAuthor=write("oldAuthor.txt",message.author)
					emoji = "\U0001F621"
					await message.add_reaction(emoji)
					log("greedy person sent twice, count reset to 1")
					write("oldAuthor.txt","")
					log("oldAuthor reset")
					return
				else:
					log("person "+str(message.author)+" entered correct number")
					write("oldAuthor.txt",message.author)
					log("author written "+str(message.author))
					emoji = "\U00002611"
					await message.add_reaction(emoji)
					log("next number:  "+str(number+1))
					write("number.txt",number+1)
					log("wrote number")
			else:
				write("number.txt",1)
				await message.channel.send("Aiyo! Wrong number! We are back at 1 leh!")
				emoji = "\U0001F621"
				await message.add_reaction(emoji)
				log("wrong number! reset number to 1")
		else:
			log("non-number detected")
		await bot.process_commands(message)
    
bot.run('insert token')
