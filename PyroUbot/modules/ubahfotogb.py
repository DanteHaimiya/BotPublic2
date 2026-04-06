import os
from PyroUbot import *
from pyrogram import filters

__MODULE__ = "SetGPic"
__HELP__ = """
<blockquote><b>『 SET GROUP PHOTO 』</b>

<b>Perintah:</b>
• <code>.setgpic</code> [reply ke foto]

<b>Catatan:</b>
• Harus dilakukan di dalam grup.
• Akun kamu harus memiliki izin admin (Change Info).
</blockquote>
"""

@PY.UBOT("setgpic")
async def set_group_photo_cmd(client, message):
    # 1. Cek apakah ini di grup/channel
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
        return await message.edit("<b>❌ Perintah ini hanya bisa digunakan di dalam grup/channel!</b>")

    # 2. Cek apakah membalas ke foto
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.edit("<b>❌ Silahkan reply ke foto yang ingin dijadikan profil grup!</b>")

    proses = await message.edit("<code>🔄 Sedang memproses penggantian foto grup...</code>")

    try:
        # 3. Download foto yang direply
        photo = await client.download_media(message.reply_to_message)
        
        # 4. Set foto grup
        await client.set_chat_photo(chat_id=message.chat.id, photo=photo)
        
        await proses.edit("<b>✅ Berhasil mengubah foto profil grup!</b>")
        
        # 5. Hapus file sementara setelah selesai
        if os.path.exists(photo):
            os.remove(photo)
            
    except Exception as e:
        await proses.edit(f"<b>❌ Gagal mengubah foto:</b>\n<code>{str(e)}</code>")