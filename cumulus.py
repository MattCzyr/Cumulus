from wordcloud import WordCloud
import discord
import random
import os
import colors

client = discord.Client()

boringwords = ['the', 'a', 'an']
output = 'wordcloud.png'
randomarg = '`' + 'random' + '`'
token = open('token.txt', 'r')


def make_cloud(text, font, hues):
    global currenthues
    currenthues = hues
    words = clean_words(text)
    wordcloud = WordCloud(font_path=get_random_font(font), background_color='black', width=640, height=360, scale=1, color_func=generate_color)
    wordcloud.generate(' '.join(words))
    wordcloud.to_file(output)


def generate_color(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    return 'hsl(%s, %s%%, %s%%)' % (random.choice(currenthues), 100, random.randint(20, 80))


def get_random_font(category):
    return 'fonts/' + category + '/' + random.choice(os.listdir('fonts/' + category))


def clean_words(text):
    clean = to_words(text)
    for boring in boringwords:
        clean[:] = [word for word in clean if word != boring]
        clean = [x for x in clean if ':' not in x]
        clean = [x for x in clean if '@' not in x]
    return clean


def to_words(text):
    return text.lower().split()


def format_fonts():
    fonts = ''
    for font in os.listdir('fonts/'):
        fonts = fonts + '`' + font + '`' + ', '
    fonts += randomarg
    return fonts


def format_colors():
    validcolors = ''
    for color in colors.all:
        validcolors = validcolors + '`' + color.name + '`' + ', '
    validcolors += randomarg
    return validcolors


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!wordcloud'))


@client.event
async def on_message(message):
    if message.content.startswith('!wordcloud'):
        words = to_words(message.content)
        args = []
        for word in words:
            if word != '!wordcloud':
                args.append(word)
        if 'help' in args:
            doc = open('documentation.txt', 'r')
            await client.send_message(message.author, doc.read() % (format_colors(), format_fonts()))
            await client.send_message(message.channel, 'Documentation has been sent via DM.')
        else:
            generating = await client.send_message(message.channel, 'Generating word cloud...')
            font = ''
            hues = []
            unknownargs = []
            for arg in args:
                if colors.is_color(arg):
                    hues.append(colors.from_name(arg).hue)
                elif arg in os.listdir('fonts/'):
                    font = arg
                else:
                    unknownargs.append(arg)

            if len(unknownargs) > 0:
                formattedargs = ''
                for unknownarg in unknownargs:
                    formattedarg = '`' + unknownarg + '`'
                    if not formattedargs:
                        formattedargs += formattedarg
                    else:
                        formattedargs = formattedargs + ', ' + formattedarg
                await client.edit_message(generating, 'Unknown argument(s): ' + formattedargs +
                                          '\n\nAvailable colors: ' + format_colors() +
                                          '\nAvailable fonts: ' + format_fonts() +
                                          '\n\nUse `!wordcloud help` to receive full documentation.')
            else:
                if not font or font == 'random':
                    font = random.choice(os.listdir('fonts/'))

                if len(hues) < 1:
                    hues.append(random.choice(colors.all).hue)

                generatefrom = ''
                async for log in client.logs_from(message.channel, limit=1000):
                    generatefrom = generatefrom + ' ' + log.content
                make_cloud(generatefrom, font, hues)

                await client.send_file(message.channel, output)
                await client.delete_message(generating)

                os.remove(output)


client.run(token.read())
