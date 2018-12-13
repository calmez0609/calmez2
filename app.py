from flask import Flask, request, abort
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('x9I42/HXzVLQQ3HLWVmxCf7z5jLAtEf44gpdKmlnGCkzXw9+y+LuKjA8WIklR29p4cXtdgCmV1CCD3woIswyRrOkphjpeubSVLIgWlBtMnI4mcAWYjkHuV48A4C9q3JIhV8GauV4tRmfKDmmZwwSoQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3d7644d429a491ed618d3b2b2fec3b2d') 
#監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def KeyWord(text):
    KeyWordlist={"李英才":"你叫也沒有用","李伯母":"讓英才占點便宜","李伯父":"你在叫就拿菸頭燙你"}
    for k in KeyWordlist.keys():
        if text.find(k) != -1:
            return [True,KeyWordlist[k]]
    return [False]

def Reply(event):
    Ktemp = KeyWord(event.message.text)
    if Ktemp[0]:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = Ktemp[1]))
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text = event.message.text))

def button(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackTemplateAction(
                    label='postback',
                    data='還沒'
                ),
                MessageTemplateAction(
                    label='message',
                    text='message text'
                ),
                URITemplateAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        button(event)
        #Reply(event)
    except Exception as e:
         line_bot_api.reply_message(event.reply_token,
           TextSendMessage(text=str(e)))
@handler.add(PostbackEvent)
def handle_postback(event):
        command=event.postback.data.split(",")
        if command[0]=="還沒":
            line_bot.api.reply_message(event.reply_token,
                TextSendMessage(text="還沒就趕快去練習~~~~"))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
