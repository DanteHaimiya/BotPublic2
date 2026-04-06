import os
from pyrogram import filters
from PyroUbot import *

__MODULE__ = "AddFile"
__HELP__ = """
<blockquote><b>『 ADD FILE 』</b>

<b>Perintah:</b>
• <code>.addfile</code> [reply ke file .py]
</blockquote>
"""

@PY.UBOT("addfile")
async def add_file_cmd(client, message):
    # 1. Cek apakah pesan itu reply ke sebuah dokumen
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.edit("<b>❌ Silahkan reply ke file .py yang ingin ditambahkan!</b>")

    doc = message.reply_to_message.document
    file_name = doc.file_name

    # 2. Cek apakah filenya berakhiran .py
    if not file_name.endswith(".py"):
        return await message.edit("<b>⚠️ Hanya file berformat .py yang diizinkan!</b>")

    await message.edit(f"<code>📥 Sedang mengunduh {file_name}...</code>")

    # 3. Tentukan folder tujuan (sesuaikan dengan ubotputra/ubotikal kamu)
    # Kita ambil folder modules secara dinamis
    current_path = os.getcwd()
    full_path = f"{current_path}/PyroUbot/modules/{file_name}"

    try:
        # 4. Download file ke folder modules
        await client.download_media(message.reply_to_message, file_name=full_path)
        
        await message.edit(
            f"<b>✅ Berhasil Menambahkan File!</b>\n\n"
            f"<b>Nama File:</b> <code>{file_name}</code>\n"
            f"<b>Lokasi:</b> <code>modules/</code>\n\n"
            f"<i>Silahkan ketik <code>/restart di bot</code> untuk mengaktifkan.</i>"
        )
    except Exception as e:
        await message.edit(f"<b>❌ Terjadi Kesalahan:</b>\n<code>{str(e)}</code>")