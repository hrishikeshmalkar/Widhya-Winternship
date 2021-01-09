from telegram.ext import CommandHandler, Updater
from telegram import *
import os
import logging
import requests
import json

class Syntaxdb():
	def __init__(self, choice=0, search_query="",language=""):
		'''
		# choice = 0 => It indicates concepts in any language
		# choice = 1 => it indicates all concepts of particular language
		'''

		if(choice == 0):
			self.url = "https://syntaxdb.com/api/v1/concepts/search?q="+search_query
		else:
			self.url = "https://syntaxdb.com/api/v1/languages/"+language+"/concepts"

	def getResponse(self):
		'''This function will returns the reponse got from the url'''
		return requests.get(self.url)

	def getJson(self,response):
		'''This fuction pass in the requests reponse and returns the json data'''
		return response.json()

	def getContent(self):
		'''This function pass the json data and returns list'''
		'''
			if choice is 'concept', the summary will have only one item in list
			if choice is is '1', the summary will have multiple items in list
		'''
		response = self.getResponse()
		json_response = self.getJson(response)
		summary = []
		for data in json_response:
			concept = data['concept_search']
			syntax = data['syntax']
			description = data['description']
			notes = data['notes']
			example = data['example']
			summary+=["\nCONCEPT\n"+concept+"\n\nSYNTAX\n"+syntax+"\n\nDESCRIPTION\n"+ description+"\n\nNOTES\n"+notes+"\n\nEXAMPLE\n"+example]
		return summary

	def getAllConcepts(self):
		'''This function pass the langauge and a list of all concepts are returned'''
		response = self.getResponse()
		json_response = self.getJson(response)
		return self.getContent(json_response)



def start(bot, update):
	'''Function for Welcome Message'''
	bot.sendChatAction(chat_id = update.message.chat_id, action = ChatAction.TYPING)
	
	bot.sendMessage(chat_id = update.message.chat_id, text = '''
		Hey %s %s! Welcome to Monster Bot! Type /help for more information regarding the functionalities of this particular bot.
	''' %(update.message.from_user.first_name,update.message.from_user.last_name))

def search(bot, update, args):
	''' Search Query Function '''
	topic = ""
	i = 0
	count = 0
	if(len(args) == 0):
		bot.sendChatAction(chat_id = update.message.chat_id, action = ChatAction.TYPING)
		bot.sendMessage(chat_id = update.message.chat_id, text = '''
			Please make sure that you enter a valid search query for me to help you.
		''')
	for arg in args:
		if(i < (len(args) - 1)):
			topic += arg + " "
		else:
			topic += arg
		i += 1
	print("\""+ topic + "\"")
	syntax = syntaxdb.Syntaxdb(choice = 0, search_query = topic, language = "")
	content = syntax.getContent()
	
	for i in range(0,len(content)):
		print("here")
		count += 1
		bot.sendChatAction(chat_id = update.message.chat_id, action = ChatAction.TYPING)
		bot.sendMessage(chat_id = update.message.chat_id, text = content[i])

	if(count==0):
		bot.sendChatAction(chat_id = update.message.chat_id, action = ChatAction.TYPING)
		bot.sendMessage(chat_id = update.message.chat_id, text =  '''
		There are no related searches to the topic you entered! Make sure your search query was right and try again! Check for spelling mistakes and follow the format in /help
		''')



def help(bot, update):
	'''Help Function which show options'''
	bot.sendChatAction(chat_id = update.message.chat_id, action = ChatAction.TYPING)
	bot.sendMessage(chat_id = update.message.chat_id, text = '''
		To use this bot, look at the format below!
		/search <concept_name> <language>
		Example : Suppose you want to use how to use the concept for in java,
		/search for in java
	''')


if __name__=='__main__':
	TOKEN = 'ENTER YOUR TOKEN HERE'
	PORT = int(os.environ.get('PORT', '8443'))

	updater = Updater(TOKEN)

  	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	logger = logging.getLogger(__name__)


	updater = Updater(token=TOKEN)
	
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler('start',start))

	dispatcher.add_handler(CommandHandler('help',help))

	dispatcher.add_handler(CommandHandler('search', search, pass_args = True))

	updater.start_polling()