from pyrogram import Client, filters
Import yt_dlp
from youtube_search import YoutubeSearch
import requests
import os
import time
import asyncio
from config import Config
from pyrogram.types import InlineKeyboardMarkup


@Client.on_message(filters.command('s',))

def a(client, message):

    query = ''

    for i in message.command[1:]:

        query += ' ' + str(i)

    print(query)

    m = message.reply_text('🎵 Processing')

    ydl_opts = {"format": "bestaudio[ext=m4a]"}

    try:

        results = []

        count = 0

        while len(results) == 0 and count < 6:

            if count>0:

                time.sleep(1)

            results = YoutubeSearch(query, max_results=1).to_dict()

            count += 1

        # results = YoutubeSearch(query, max_results=1).to_dict()

        try:

            link = f"https://youtube.com{results[0]['url_suffix']}"

            # print(results)

            title = results[0]["title"]

            thumbnail = results[0]["thumbnails"][0]

            duration = results[0]["duration"]

            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS

            # if time_to_seconds(duration) >= 1800:  # duration limit

            #     m.edit("Exceeded 30mins cap")

            #     return

            performer = f"✯Rᴇᴀʟ Mᴜsɪᴄ ✯" 

            thumb_name = f'thumb{message.message_id}.jpg'

            thumb = requests.get(thumbnail, allow_redirects=True)

            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:

            print(e)

            m.edit('**Please use the proper format for request a song☹️**')

            return

    except Exception as e:

        m.edit(

            "**ᴇɴᴛᴇʀ sᴏɴɢ ɴᴀᴍᴇ ᴡɪᴛʜ /song ᴄᴏᴍᴍᴀɴᴅ**"

        )

        print(str(e))

        return

    m.edit("<code>⏫ Uploading...</code>")

    message.reply_chat_action("upload_audio")

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info_dict = ydl.extract_info(link, download=False)

            audio_file = ydl.prepare_filename(info_dict)

            ydl.process_info(info_dict)

        rep = f'⍟:<code>{title}</code>\n\n⍟ 𝑽𝒊𝒆𝒘𝒔:{views}\n\n⍟ 𝑫𝒖𝒓𝒂𝒕𝒊𝒐𝒏: {duration}\n\n⍟<b>ᴜᴘʟᴏᴀᴅ Bʏ</b>: <a href=https://t.me/realmusicworldgroup>Rᴇᴀʟᴍᴜsɪᴄ</a>\n\n❍ᶜᵒᵐᵐᵉⁿᵗㅤ    ⎙ˢᵃᵛᵉㅤ  ⌲ˢʰᵃʳᵉ'

        secmul, dur, dur_arr = 1, 0, duration.split(':')

        for i in range(len(dur_arr)-1, -1, -1):

            dur += (int(dur_arr[i]) * secmul)

            secmul *= 60

        message.reply_audio(audio_file, caption=rep, parse_mode='HTML', title=title, duration=dur, performer=performer, thumb=thumb_name)

        m.delete()

    except Exception as e:

        m.edit('𝗗𝗼𝘄𝗹𝗼𝗮𝗱 𝗙𝗮𝗶𝗹𝗱 𝗬𝗧𝗗𝗟𝗣')

        print(e)

    try:

        os.remove(audio_file)

        os.remove(thumb_name)

    except Exception as e:

        print(e)
