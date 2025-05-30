from mmpy_bot import Bot, Settings, Plugin, listen_to
import re
import json
from datetime import datetime

class MyPlugin(Plugin):
    @listen_to("hi")
    async def hello(self, message):
        self.driver.create_post(
            channel_id=message.channel_id,
            message="Hi I bot!"
        )

    @listen_to(".*error.*", re.IGNORECASE)
    async def send_error(self, message, *args):
        try:
            if isinstance(message.body, str):
                msg_data = json.loads(message.body)
            else:
                msg_data = message.body

            user_message = msg_data['data']['post']['message']
            username = msg_data['data']['sender_name'].replace('@', '')

            create_at = msg_data['data']['post']['create_at'] / 1000
            error_date = datetime.fromtimestamp(create_at).strftime('%Y-%m-%d %H:%M:%S')

            ERROR_CHANNEL_ID = ""

            error_report = (
                f"Error from @{username}\n"
                f"{error_date}\n"
                f"<Message: {user_message}"
            )

            self.driver.create_post(
                channel_id=ERROR_CHANNEL_ID,
                message=error_report
            )

            self.driver.create_post(
                channel_id=message.channel_id,
                message="Your message send"
            )

        except Exception as e:
            print(f"Error send message: {str(e)}")
            self.driver.create_post(
                channel_id=message.channel_id,
                message="Error was happend"
            )

bot = Bot(
    settings=Settings(
	    MATTERMOST_URL="",
        BOT_TOKEN="",
        SSL_VERIFY=True,
    ),
    plugins=[MyPlugin()],
)
bot.run()
