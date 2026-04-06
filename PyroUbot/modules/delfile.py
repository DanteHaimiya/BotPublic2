import os
from PyroUbot import *
from pyrogram import filters

__MODULE__ = "DelFile"
__HELP__ = """
<blockquote><b>『 DELETE FILE 』</b>

<b>Perintah:</b>
• <code>.delfile</code> [nama_file.py]
• <code>.delfile</code> [reply ke file .py]

<b>Catatan:</b>
• Menghapus file dari folder modules.
</blockquote>
"""

@PY.UBOT("delfile")
async def del_file_cmd(client, message):
    file_name = ""
    
    # 1. Cek apakah ada reply file atau nama file di teks
    if message.reply_to_message and message.reply_to_message.document:
        file_name = message.reply_to_message.document.file_name
    elif len(message.command) > 1:
        file_name = message.command[1]
    else:
        return await message.edit("<b>❌ Berikan nama file atau reply ke filenya!</b>")

    # 2. Keamanan: Hanya izinkan hapus file .py di folder modules
    if not file_name.endswith(".py"):
        return await message.edit("<b>⚠️ Hanya bisa menghapus file berformat .py!</b>")

    path = f"PyroUbot/modules/{file_name}"

    # 3. Proses hapus
    if os.path.exists(path):
        try:
            os.remove(path)
            await message.edit(
                f"<b>✅ Berhasil Menghapus:</b> <code>{file_name}</code>\n"
                f"<i>Silahkan ketik <code>.restart</code> untuk memperbarui sistem.</i>"
            )
        except Exception as e:
            await message.edit(f"<b>❌ Gagal menghapus:</b> <code>{str(e)}</code>")
    else:
        await message.edit(f"<b>❌ File <code>{file_name}</code> tidak ditemukan.</b>")