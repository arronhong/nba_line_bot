import os

from flask import Flask, request, abort, current_app
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    FlexSendMessage
)

from daily import get_daily_carousel


app = Flask(__name__)
sess = requests.Session()
sess.headers.update({'User-Agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
app.extensions['http_client'] = sess
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', ''))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', ''))


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
        current_app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text != '今日比分':
        return

    try:
        contents = get_daily_carousel()
    except Exception:
        current_app.logger.exception('there are something wrong')
        abort(500)

    line_bot_api.reply_message(event.reply_token,
                               FlexSendMessage('Daily', contents))


if __name__ == "__main__":
    app.run(debug=True)
