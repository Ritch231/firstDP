import logging
import time
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
# openai
import openai

# 报错全局变量
logging_error = False

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai.api_key = "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"


# 处理start命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# 模仿处理node命令
async def node(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="我是一个山寨机器人🤖️")


# 处理聊天信息
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 打印聊天id和信息
    print(f"id:{update._effective_chat.id}   {update.message.text}")
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="请稍等...")
    # 问题发到ChatGpt
    prompt = update.message.text
    message = ""
    # 向AI服务器发送5次提问
    for i in range(5):
        try:
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            message = "ChatGpt:\n" + completions.choices[0].text
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            print(message)
            time.sleep(5)
            break
        except Exception as e:
            # 根据出错次数返回结果
            if i == 4:
                message = f'🤦‍♀️AI累了,休息一会再提问吧... \n {e}'
            else:
                message = f'🤷‍♂️AI出错:{i + 1}/5,请稍等...'
                # AI服务器出错延迟5秒
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            time.sleep(5)

    # 别人说什么，bot回复什么

    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    # 引用chatgpt的回答


if __name__ == '__main__':
    application = ApplicationBuilder().token('2122878220:AAHVc1j3r3bfIPfb9Hmqtw3OZNFVUcbTMaw').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    node_handler = CommandHandler('node', node)
    application.add_handler(node_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(echo_handler)

    application.run_polling()
