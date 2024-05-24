import os
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import pi_value
from utils import isfloat
import math
import requests
from alive import keep_alive
import urllib.parse
from database import scrape
import pymongo
import time

API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

ostrich = Client("ostrich", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@ostrich.on_message(filters.command(["start"]))
async def start(client, message):

    await message.reply_text(text=f'''
**Hi {message.from_user.mention}!**

Having trouble do a math problem?

Don't worry I have a interesting collection of tools to help you solve it.
''',
                             disable_web_page_preview=True,
                             reply_markup=InlineKeyboardMarkup([[
                                 InlineKeyboardButton("HELP",
                                                      callback_data="getHELP"),
                             ]]),
                             reply_to_message_id=message.id)
    scrape(message)

@ostrich.on_message(filters.command(["help"]))
async def assist(client, message):

    await message.reply_text(
        text=f'''
**Here is an detailed guide on using me.**

**Available Commands:**
/start : Check if I am alive!
/help : Send you this text

/calculator : Open Calculator
/fact : Get random fact

/simplify : Simplifies an expression
/factor : Find factors
/derive : Derive expression
/integrate : Integrate an equation
/zeroes : Find zeroes of polynomial

/about : About me
/donate : Donate us

**Constants:** 
     - [ `/pi`, `/e`, `/tau` ]
**Others:**   
     - `/ceil`, `/acos`, `/asin`, `/acosh`, `/asinh`, `/atanh`, `/sin`, `/cos`, `/tan`, `/degrees`, `/erf`, `/erfc`, `/sqrt`, `/log`



        ''',
                  disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("SUPPORT GROUP", url="https://t.me/ostrichdiscussion"),
                ]
            ]
        ),
        reply_to_message_id=message.id
    )

@ostrich.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            InlineKeyboardButton("➰Channel", url="t.me/theostrich"),
            InlineKeyboardButton("👥Support Group",
                                 url="t.me/ostrichdiscussion"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        "\nI will help you with math problems."
        "\n\n<b>About Me :</b>"
        "\n\n  - <b>Name</b>        : Mailable"
        "\n\n  - <b>Creator</b>      : @theostrich"
        "\n\n  - <b>Language</b>  : Python 3"
        "\n\n  - <b>Library</b>       : <a href=\"https://docs.pyrogram.org/\">Pyrogram</a>"
        "\n\nIf you enjoy using me and want to help me survive, do donate with /donate command - my creator will be very grateful! Doesn't have to be much - every little helps! Thanks for reading :)",
        reply_markup=reply_markup,
        disable_web_page_preview=True)

@ostrich.on_message(filters.command(["donate"]))
async def donate(client, message):
    keyboard = [
        [
            InlineKeyboardButton("Contribute",
                                 url="https://github.com/theostrich"),
            InlineKeyboardButton("Paypal Us",
                                 url="https://paypal.me/donateostrich"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(
        "Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive.",
        reply_markup=reply_markup)



@ostrich.on_message(filters.command(["calculator"]))
async def calculator(client,message):
    buttons = [

                    [
                      InlineKeyboardButton("(",callback_data="("),
                      InlineKeyboardButton(")",callback_data=")"),
                      InlineKeyboardButton("DEL",callback_data="DEL"),
                      InlineKeyboardButton("AC",callback_data="clear")
                    ],
                    [
                      InlineKeyboardButton("7",callback_data="7"),
                      InlineKeyboardButton("8",callback_data="8"),
                      InlineKeyboardButton("9",callback_data="9"),
                      InlineKeyboardButton("/",callback_data="/")
                    ],
                    [
                      InlineKeyboardButton("4",callback_data="4"),
                      InlineKeyboardButton("5",callback_data="5"),
                      InlineKeyboardButton("6",callback_data="6"),
                      InlineKeyboardButton("*",callback_data="*")
                    ],
                    [
                      InlineKeyboardButton("1",callback_data="1"),
                      InlineKeyboardButton("2",callback_data="2"),
                      InlineKeyboardButton("3",callback_data="3"),
                      InlineKeyboardButton("-",callback_data="-")
                    ],
                    [
                      InlineKeyboardButton(".",callback_data="."),
                      InlineKeyboardButton("0",callback_data="0"),
                      InlineKeyboardButton("%",callback_data="%"),
                      InlineKeyboardButton("+",callback_data="+"),

                    ],
                    [
                      InlineKeyboardButton("CALCULATE",callback_data="=")],           
                     [InlineKeyboardButton("CLOSE",callback_data="close")
                      
                    ]

              ]
    await message.reply_text(text=f'''Calculator:''',
                             disable_web_page_preview=True,
                             reply_markup=InlineKeyboardMarkup(buttons),
                             reply_to_message_id=message.id)


@ostrich.on_callback_query()
async def cb_handler(client, query):
  if query.data == "close":
        await query.message.delete()
        await query.answer(
        "Closed"
    )
  elif query.data == "redo":
        await query.message.delete()
        await calculator(client,query.message.reply_to_message)
  elif query.data == "getHELP":
        await query.message.delete()
        await assist(client,query.message.reply_to_message)    
  elif query.data == "clear":
    await query.message.edit_text("Calculator:",reply_markup=query.message.reply_markup)
  elif query.data == "DEL":
    text = query.message.text[:-1]
    if text == "":
      text = "Calculator:"
    await query.message.edit_text(text,reply_markup=query.message.reply_markup)
  elif query.data == "=":
    try:
      answer = eval(query.message.text, {"__builtins__": {}}, {})
      text   = f"**{query.message.text} =** \n`{answer}`"
    except:
      text = "**Something went wrong!\nContact @ostrichdiscussion**" 
    await query.message.edit_text(text,reply_markup=InlineKeyboardMarkup([              [
                      InlineKeyboardButton("Calculate Again",callback_data="redo"),

                    ]]))
  else:
    if query.message.text == "Calculator:":
      text = query.data
    else:
      text = query.message.text + query.data
    await query.message.edit_text(text,reply_markup=query.message.reply_markup)


@ostrich.on_message(filters.command(["pi"]))
async def pi(client,message):
     args = get_args(message)
     digit = 16 
     if len(args) > 1:
       if args[1].isdigit():
         digit = int(args[1])
     if not 5 <= digit <= 4000:
       await message.reply_text("Provide digits between 5 and 4000.")
       return 
     print(digit)
     await message.reply_text(f"`{pi_value[0:digit]}`")


@ostrich.on_message(filters.command(["ceil"]))
async def ceil(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any number\nEx:** `/ceil 28`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any number\nEx:** `/ceil 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     await message.reply_text(f"`{math.ceil(float(args[1]))}`")

@ostrich.on_message(filters.command(["e"]))
async def e(client,message):
  await message.reply_text(f"`{math.e}`")               
                          
@ostrich.on_message(filters.command(["fact"]))
async def fact(client,message):
  r = requests.get("http://numbersapi.com/random?json") 
  await message.reply_text(f"`{r.json()['text']}`") 

@ostrich.on_message(filters.command(["simplify"]))
async def simplify(client,message):
  args = get_args(message)
  if len(args) == 1:
       await message.reply_text("**Provide any expression\nEx:** `/simplify 2^2+2(2)`")
       return 
  exp =  f"{message.text.split(' ',1)[1]}"
  safe_string = urllib.parse.quote_plus(exp)

  try:
    r = requests.get(f"https://newton.vercel.app/api/v2/simplify/{safe_string}").json()
    text = f'''
**Operation  :** {r['operation']}
**Expression :** {r['expression']}

**Result     :** `{r['result']}`
'''
  except:
    text = "**Something went wrong!\nContact @ostrichdiscussion**"


  await message.reply_text(f"{text}") 

@ostrich.on_message(filters.command(["factor"]))
async def factor(client,message):
  args = get_args(message)
  if len(args) == 1:
       await message.reply_text("**Provide any expression\nEx:** `/factor x^2 + 2x`")
       return 
  exp =  f"{message.text.split(' ',1)[1]}"
  safe_string = urllib.parse.quote_plus(exp)


  try:
    r = requests.get(f"https://newton.vercel.app/api/v2/factor/{safe_string}").json()
    text = f'''
**Operation  :** {r['operation']}
**Expression :** {r['expression']}

**Result     :** `{r['result']}`
'''
  except:
    text = "**Something went wrong!\nContact @ostrichdiscussion**"


  await message.reply_text(f"{text}") 

@ostrich.on_message(filters.command(["derive"]))
async def derive(client,message):
  args = get_args(message)
  if len(args) == 1:
       await message.reply_text("**Provide any expression\nEx:** `/derive x^2+2x`")
       return 
  exp =  f"{message.text.split(' ',1)[1]}"
  safe_string = urllib.parse.quote_plus(exp)


  try:
    r = requests.get(f"https://newton.vercel.app/api/v2/derive/{safe_string}").json()
    text = f'''
**Operation  :** {r['operation']}
**Expression :** {r['expression']}

**Result     :** `{r['result']}`
'''
  except:
    text = "**Something went wrong!\nContact @ostrichdiscussion**"


  await message.reply_text(f"{text}") 

@ostrich.on_message(filters.command(["zeroes"]))
async def zeroes(client,message):
  args = get_args(message)
  if len(args) == 1:
       await message.reply_text("**Provide any expression\nEx:** `/zeroes x^2+2x`")
       return 
  exp =  f"{message.text.split(' ',1)[1]}"
  safe_string = urllib.parse.quote_plus(exp)

  try:
    r = requests.get(f"https://newton.vercel.app/api/v2/zeroes/{safe_string}").json()
    text = f'''
**Operation  :** {r['operation']}
**Expression :** {r['expression']}

**Result     :** `{r['result']}`
'''
  except:
    text = "**Something went wrong!\nContact @ostrichdiscussion**"


  await message.reply_text(f"{text}") 


@ostrich.on_message(filters.command(["tau"]))
async def tau(client,message):
  await message.reply_text(f"`{math.tau}`")               



def get_args(m):
    args = []
    if m.text:
       args = m.text.split(" ")
    return args

@ostrich.on_message(filters.command(["acos"]))
async def acos(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any number\nEx:** `/acos 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any number\nEx:** `/acos 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     if not -1 <= num <= 1:
       await message.reply_text("**Value must between `-1` and `1`**")
       return 
     print(num)
     await message.reply_text(f"`{math.acos(num)}`")

@ostrich.on_message(filters.command(["asin"]))
async def asin(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any number\nEx:** `/asin 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any number\nEx**: `/asin 0`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     if not -1 <= num <= 1:
       await message.reply_text("**Value must between `-1` and `1`**")
       return 
     print(num)
     await message.reply_text(f"`{math.asin(num)}`")


@ostrich.on_message(filters.command(["acosh"]))
async def acosh(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any number\nEx:** `/acosh 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any number\nEx:** `/acosh 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     if not num >= 1:
       await message.reply_text("**Value must greater than or equal to `1`**")
       return 
     print(num)
     await message.reply_text(f"`{math.acosh(num)}`")

@ostrich.on_message(filters.command(["sqrt"]))
async def sqrt(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any number\nEx:** `/sqrt 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any number\nEx:** `/sqrt 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     if not num >= 0:
       await message.reply_text("**Value must greater than or equal to `0`**")
       return 
     print(num)
     await message.reply_text(f"`{math.sqrt(num)}`")


@ostrich.on_message(filters.command(["asinh"]))
async def asinh(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/asinh 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx**: `/asinh 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.asinh(num)}`")

@ostrich.on_message(filters.command(["atanh"]))
async def atanh(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/atanh 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/atanh 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
     if not -0.99 < num < 0.99:
       await message.reply_text("**Value must between `-0.99` and `0.99`**")
       return 
     print(num)
     await message.reply_text(f"`{math.atanh(num)}`")


@ostrich.on_message(filters.command(["cos"]))
async def cos(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/cos 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/cos 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.cos(num)}`")
@ostrich.on_message(filters.command(["sin"]))
async def sin(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/sin 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/sin 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.sin(num)}`")
@ostrich.on_message(filters.command(["tan"]))
async def tan(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/tan 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/tan 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.tan(num)}`")
@ostrich.on_message(filters.command(["degrees"]))
async def degrees(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/degrees 45`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/degrees 50`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.degrees(num)}`")

@ostrich.on_message(filters.command(["log"]))
async def log(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/log 45`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/log 50`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.log(num)}`")
@ostrich.on_message(filters.command(["factorial"]))
async def factorial(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/factorial 45`")
       return 
     if not args[1].isdigit():
       await message.reply_text("**Provide any value\nEx:** `/factorial 50`")
       return


     num = int(args[1])

    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.factorial(num)}`")

@ostrich.on_message(filters.command(["erf"]))
async def erf(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx** `/erf 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/erf 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.erf(num)}`")

@ostrich.on_message(filters.command(["erfc"]))
async def erfc(client,message):
     args = get_args(message)
     if len(args) == 1:
       await message.reply_text("**Provide any value\nEx:** `/erfc 0.5`")
       return 
     if not isfloat(args[1]):
       await message.reply_text("**Provide any value\nEx:** `/erfc 28.6`")
       return

     if args[1].isdigit():
       num = int(args[1])
     else:
       num =  float(args[1])
    # if not num >= 1:
     #  await message.reply_text("Provide value must greater than or equal to 1.")
      # return 
     print(num)
     await message.reply_text(f"`{math.erfc(num)}`")

myclient = pymongo.MongoClient(
        os.environ['mongouri'])
db = myclient['calcus']
collection = db["usercache"]

@ostrich.on_message(filters.command(["broadcast"]))
async def broadcast(client, message):
      chat_id = message.chat.id
      botOwnerID = [1775541139 ,1520625615]
      if chat_id in botOwnerID:
        await message.reply_text("Broadcasting...")
        chat = (collection.find({}, {'userid': 1, '_id': 0}))
        chats = [sub['userid'] for sub in chat]
        failed = 0
        for chat in chats:
          try:
              await message.reply_to_message.copy(chat)
              time.sleep(2)
          except:
                failed += 1
                print("Couldn't send broadcast to %s, group name %s", chat)
        await message.reply_text("Broadcast complete. {} users failed to receive the message, probably due to being kicked.".format(failed))
      else:
        await client.send_message(1520625615,f"Someone tried to access broadcast command,{chat_id}")


keep_alive()
ostrich.run()