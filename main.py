
import os
import datetime
from telegram import Update
from telegram.ext import *
import requests as rq


def startCommand(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id,"Gunakan tanda slash / Garis Miring ( / ) Untuk mulai command")
    
def helpCommand(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id,"Pilih Menu pada Tanda slash atau garis miring, kemudian klik")
    
def userKeyword(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id, update.message.text)
    context.bot.send_message(update.message.chat_id,"Tidak dapat mengenali perintah, silahkan pilih menu dibawah")

def sultengCovid(update: Update, context: CallbackContext):
    SULTENG_ENDPOINT = os.environ['SULTENG_ENDPOINT']
    response = rq.get(SULTENG_ENDPOINT)
    jsonParse = response.json()
    positif = str(jsonParse['data']['positif'])
    sembuh = str(jsonParse['data']['sembuh'])
    meninggal = str(jsonParse['data']['meninggal'])

    dateNow = datetime.datetime.now()
    context.bot.send_message(update.message.chat_id,f"""
    Total Kumulatif Covid-19 di Sulawesi Tengah
    Positif = {positif} Orang
    Sembuh = {sembuh} Orang
    Meninggal = {meninggal} Orang

    Update = {dateNow}
    """)

def indonesiaCovid(update: Update, context: CallbackContext):
    API_INDO = os.environ['API_INDO']
    response = rq.get(API_INDO)
    jsonParse = response.json()
    positif = str(jsonParse[0]['positif'])
    sembuh = str(jsonParse[0]['sembuh'])
    meninggal = str(jsonParse[0]['meninggal'])
    dateNow = datetime.datetime.now()
    context.bot.send_message(update.message.chat_id,f"""
    Total Kumulatif Covid-19 di Indonesia
    Positif = {positif} Orang
    Sembuh = {sembuh} Orang
    Meninggal = {meninggal} Orang

    Update = {dateNow}
    """)

def sultengDistrict(update: Update, context:CallbackContext):
    DISTRICT = os.environ['SULTENG_DISTRICT_ENDPOINT']
    response = rq.get(DISTRICT)
    jsonParse = response.json()
    data = jsonParse['data']
    for i in data:
        message = f"""
        Kabupaten/Kota {i['kabupaten']}
        Positif = {i['positif']} Orang
        Negatif = {i['negatif']} Orang
        Sembuh = {i['sembuh']} Orang
        Meninggal = {i['meninggal']} Orang
        """
        context.bot.send_message(update.message.chat_id,message)


def main():
    print("BOT RUNNING...")
    API_KEY = os.environ['API_KEY']

    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',startCommand))
    dp.add_handler(CommandHandler('help',helpCommand))
    dp.add_handler(CommandHandler('sulteng',sultengCovid))
    dp.add_handler(CommandHandler('kabupaten',sultengDistrict))
    dp.add_handler(CommandHandler('indonesia',indonesiaCovid))
    dp.add_handler(MessageHandler(Filters.text, userKeyword))
    #updater.start_webhook(listen='0.0.0.0',port=8443, url_path=API_KEY, webhook_url='https://covid19-sulteng.herokuapp.com/'+API_KEY)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

