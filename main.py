import discord
import time
import os
import random
import yfinance as yf
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#########get news
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
def getdatestring(day):
    return str(day).split("-")
newslinks=[]
async def getnews(endday, company,message,numarticles):
    print("getting news from " + str(endday)[:10] + " and earlier")
    # get a range of days from start to a week
    # endday = datetime.date(2018,4,3)
    date = str(endday)[:10]
    #delta = datetime.timedelta(days=0)
    startday = endday
    endyear, endmonth, endday = getdatestring(endday)
    endday = endday.split(" ")[0]
    startyear, startmonth, startday = getdatestring(startday)
    startday = startday.split(" ")[0]
    page = 0
    exists = True
    print("day is " + endday)
    while exists == True and page < 1:
        print("making google search for page... " + str(page))
        site = requests.get(
            "https://www.google.com/search?q=" + company + "&safe=active&biw=1517&bih=643&source=lnt&tbs=cdr%3A1%2Ccd_min%3A" + startmonth + "%2F" + startday + "%2F" + startyear + "%2Ccd_max%3A" + endmonth + "%2F" + endday + "%2F" + endyear + "&tbm=nws",
            headers=headers)
        # extract links from the search
        soup = BS(site.content, 'html.parser')
        infocards = soup.find_all('g-card')
        if (len(infocards) == 0):
            exists = False
            print("no")
        for card in infocards[:int(numarticles)]:
            link = card.find('a').get('href')
            if (date + "," + link) not in newslinks:
                newslinks.append(date + "," + link)
                await message.channel.send(link)
        page += 1
        time.sleep(1)
###############################

######################## recover deleted messages
lastdeletedmessage = ""
ldauthor = None  
@client.event
async def on_message_delete(message):
  global lastdeletedmessage 
  global ldauthor
  lastdeletedmessage = message.content
  ldauthor = message.author.name
################################################

############ recover edited messages
editrecoverthing ="Nothing was edited recently"
@client.event
async def on_message_edit(before, after):
  global editrecoverthing
  editrecoverthing = before.author.name+" edited '"+before.content+"' to say, '"+after.content+"'"
#####################

##########detect and chastize swearers
swears = ["fuck","cunt","shit","bitch","whore","slut","asshole","cock","pussy","dick"]
async def punishswear(message):
  print("cursed!")
  responses = ["\*shoves soap in "+message.author.name+"'s mouth*","\*beats "+message.author.name+" for swearing*","Cleanse your mind, "+message.author.name,"smh my head, "+message.author.name,"You've got a sick mind, "+message.author.name]
  await message.channel.send(random.choice(responses))
######################################

########object for nicknames
class namechange:
  def __init__(self, user, name,ogm):
    self.member = user
    self.ogm = ogm
    self.name = name
    self.votes =0
    self.voters = []
namechanges = []
####################################
class farm:
  def __init__(self):
    self.troops = []
    self.level = 1
    self.xp = 0
    self.bal = 0
    self.debt = 15000
empires = []
class basictroop:
  def __init__(self):
    self.attack = 1
    self.level = 1
    self.xp = 0
class heavytroop:
  def __init__(self):
    self.attack = 3
    self.level = 1
    self.xp = 0
class scientist:
  def __init__(self):
    self.level = 1
    self.xp = 0
##########handle reactions
@client.event
async def on_reaction_add(reaction, user):
  if (reaction.message.content.startswith("pp")):
    await processmessage(reaction.message,user)
#########################

############handle messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #a few fun things and inside jokes   
    for swear in swears:
      if (swear in message.content):
        await punishswear(message)
    if ("robin" in message.content):
      pass
      #await message.channel.send("mmm, robin")
    if ("gay" in  message.content):
      await message.channel.send("is a perfectly valid sexual orientation!")
    if ("isef" in  message.content.lower()):
      await message.channel.send("HEY I KNOW A GUY WHO DID ISEF AND HAS AN ISEF GIRL")
    if ("dosa" in  message.content.lower()):
      pass
      #await message.channel.send("huh, weirdly close to dosi")
    if ("anubhav" in  message.content.lower()):
      pass
      #await message.channel.send("**MOOOOOAAAAAAAANNNNNN**")
    if ("sing" in  message.content.lower()):
      await message.channel.send("Have you met the great singer, Atharve?")
    if ("yash" in  message.content.lower()):
      pass
      #await message.channel.send("EVERYBODY IS A STINKER!!!1!!!!")
    if ("sasha" in message.content):
      await message.channel.send("NO SIMPING FOR SASHA")
    if 'happy birthday' in message.content.lower():
      await message.channel.send('Happy Birthday! 🎈🎉')
    ######receive commands
    if message.content.startswith("pp"):
        #await message.channel.send('Hello!')
        await processmessage(message)
    
########################################################################
async def processmessage(message,reacter=None):
  print("got this: "+message.content)
  command = message.content.split(" ",2)[1]
  argument = "none"

  #has an argument
  if (len(message.content.split(" ",2))>2):
    argument = message.content.split(" ",2)[2]
  
  #recover edits
  if (command == "er"):
    await message.channel.send(editrecoverthing)
  
  #recover deletes
  if (command == "r"):
    await message.channel.send("I recovered this message: '"+lastdeletedmessage+"', from "+ldauthor)

  #random number gen  
  if (command == "rng"):
    mini = 0
    maxi = 10
    mini,maxi = argument.split(" ",1)
    num = random.randint(int(mini),int(maxi))
    await message.channel.send("Here's a random number between "+mini+" and "+maxi+": "+str(num))
  
  #name change voter
  if (command == "cn"):
    print("name change time!")
    if (argument != "none"):

      #process stuff
      print("this the argument: "+argument)
      name = argument.split(" ",1)[1]
      user = message.mentions[0]
      found = False;
      print("There are "+str(len(namechanges))+" pending changes!")

      #look for an existing name
      if (len(namechanges)>0):
        for change in namechanges:
          print("User: " +change.member.name+" Name: "+change.name)
          for voter in  change.voters:
            print(voter.name)
          if (change.member == user and change.name == name and reacter != None and reacter in change.voters):
            await message.channel.send("You already voted for this name change!")
            found = True
          if (change.member == user and change.name == name and reacter != None and reacter not in change.voters):
            change.votes += 1
            change.voters.append(reacter)
            await message.channel.send("The request to change "+user.name+"'s name to "+name+" has "+str(change.votes)+" vote(s)! "+str(3-change.votes)+" more vote(s) needed!")
            found = True
          if (change.votes >= 3):
            found = True
            await message.channel.send("Changing "+user.name+"'s name to "+name+"!")
            await user.edit(nick = name)
            namechanges.remove(change)
      
      #tis a new name change      
      if (found == False):
        print("new name change!")
        chng = namechange(user,name,message)
        chng.votes = 0 
        #chng.voters.append(message.author)
        await message.channel.send("The request to change "+user.name+"'s name to "+name+" has "+str(chng.votes)+" vote(s)! "+str(3-chng.votes)+" more vote(s) needed! \nReact to the command from "+message.author.name+" with a :thumbsup: to vote!")
        #await message.add_reaction('\N{THUMBS UP SIGN}')
        namechanges.append(chng)
        print("There are "+str(len(namechanges))+" pending changes!")

  #stocks
  if (command == "stock"):
    ticker = "APPL"
    startdate = "2020-09-01"
    enddate = "2020-09-11"
    ticker,startdate,enddate = argument.split(" ",2)
    print(argument.split(" ",2))
    tickerData = yf.Ticker(ticker)
    # get the historical prices for this tickern
    # tickerDf = tickerData.history(period='1d', start='2017-1-01', end='2017-12-25')
    tickerDf = tickerData.history(period='1d', start=str(startdate), end=str(enddate))
    #plt.plot(tickerDf["Close"])
    tickerDf.plot(y="Close")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Stock Price of "+ticker+" from "+startdate+" to "+enddate)
    plt.savefig('foo.png', bbox_inches='tight')
    await message.channel.send(file=discord.File('foo.png'))

  #news
  if (command == "news"):
    print("news!")
    subject = "coronavirus"
    day = str(datetime.date.today())
    articles = 3
    try:
      subject = argument.split(" ",2)[0]
      articles = argument.split(" ",2)[1]
      day = argument.split(" ",2)[2]
    except:
      pass
    await getnews(day,subject,message,articles)
  
  #rps
  if (command == "rps"):
    channel = message.channel
    user = message.author
    await message.channel.send("Starting a rock, paper, scissors match against "+message.author.name)
    choices = ["rock","paper","scissors"]
    ended = False
    botwins = 0
    playerwins = 0
    def check(m):
      return m.content in choices and m.channel == channel and m.author == user
    while not ended:
        msg = await client.wait_for('message', check=check)
        botpick = random.choice(choices)
        score = "  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins)
        if (botpick == msg.content):
          await message.channel.send("We both picked the same thing!"+score)

        if (botpick == "rock" and msg.content == "paper"):
          playerwins +=1
          await message.channel.send("You won against Rock!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))

        if (botpick == "paper" and msg.content == "rock"):
          botwins +=1
          await message.channel.send("You lost against Paper!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))

        if (botpick == "rock" and msg.content == "scissors"):
          botwins +=1
          await message.channel.send("You lost against Rock!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))
         
        if (botpick == "scissors" and msg.content == "rock"):
          playerwins +=1
          await message.channel.send("You won against Scissors!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))

        if (botpick == "paper" and msg.content == "scissors"):
          playerwins +=1
          await message.channel.send("You won against Paper!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))

        if (botpick == "scissors" and msg.content == "paper"):
          botwins +=1
          await message.channel.send("You lost against Scissors!"+"  ||  Score: Me: "+str(botwins)+" | "+user.name+": "+str(playerwins))
          
        if (botwins == 3):
          await message.channel.send("You weren't good enough, "+message.author.name)
          ended = True
        if (playerwins == 3):
          await message.channel.send("Good game, "+message.author.name+"!")
          ended = True
    pass

  #clash royale kind of thing
  if (command == "empire"):
    empires.append(farm())
  if(command == "poll"):
    #pp poll (question) (options, separated by commas) (max time)
    pass
client.run(os.getenv('TOKEN'))