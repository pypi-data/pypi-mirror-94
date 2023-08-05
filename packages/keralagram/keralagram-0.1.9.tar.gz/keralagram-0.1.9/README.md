# KeralaGram

A python telegram asynchronous bot api made using [aiohttp](https://github.com/aio-libs/aiohttp).
This lib was earlier binded with [httpx](https://pypi.org/project/httpx/). But after the initial release we found it much slower than aiohttp.
So we switched to aiohttp


## Getting started.

* Installation using pip:

```
$ pip install keralagram
```

* While the API is production-ready, it is still under development, and it has regular updates, do not forget to update it regularly by calling `pip install keralagram --upgrade`

## Writing your first bot

### Prerequisites

[Get an API token via @BotFather](https://core.telegram.org/bots#botfather). We will call this token `TOKEN`.
Furthermore, you have basic knowledge of the Python programming language and more importantly [the Telegram Bot API](https://core.telegram.org/bots/api).

### A simple command bot

```python
from keralagram import KeralaGram, Dispatcher
from keralagram.types import Message

bot = KeralaGram("TOKEN")
dp = Dispatcher(bot)

# you can use a list of prefixes or a single one 
# Also if the prefixes value is none defaults to "/"
@dp.on_command("start", prefixes=["!", "/"])
async def start(c: KeralaGram, m: Message):
    await m.reply_text("hello")

if __name__ == '__main__':
    dp.run()
```

## The Telegram Chat Group

Get help. Discuss. Chat.

* Join the [Kerala Telegram Chat Group](https://telegram.me/keralasbot)
* We now have a Telegram Channel as well! Keep yourself up to date with API changes, and [join it](https://telegram.me/keralasbotnews).

## More examples

WILL BE SOON PUBLISHED
