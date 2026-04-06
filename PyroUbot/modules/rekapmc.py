import pytz
from datetime import datetime
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from PyroUbot import *

# ==========================================
# ⚙️ KONFIGURASI DATABASE MONGODB
# ==========================================
MONGO_URL = "mongodb+srv://lelap25058_db_user:1taMgotHVbyz6mf9@cluster0.duzukqu.mongodb.net/?appName=Cluster0"
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["iqbalubot"] 
rekap_collection = db["rekap_mc_grup"] 

# ==========================================
# 📖 FORMAT BANTUAN MODULE
# ==========================================
__MODULE__ = "ʀᴇᴋᴀᴘ"
__HELP__ = """
<blockquote><b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴋᴀᴘ ᴍᴄ ⦫</b>

<b>⎆ ᴘᴇʀɪɴᴛᴀʜ :</b>
ᚗ <code>{0}resetmc</code>
⊷ ᴍᴇʀᴇsᴇᴛ / ᴍᴇɴɢʜᴀᴘᴜs ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ ʜᴀʀɪ ɪɴɪ.

ᚗ <code>{0}rekapmc</code>
⊷ ᴍᴇʟɪʜᴀᴛ ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ ʜᴀʀɪ ɪɴɪ.

ᚗ <code>{0}rekapmc list</code>
⊷ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ᴛᴀɴɢɢᴀʟ ʀᴇᴋᴀᴘ ᴍᴄ ʏᴀɴɢ ᴛᴇʀsᴇᴅɪᴀ.

ᚗ <code>{0}rekapmc (tanggal)</code>
⊷ ᴍᴇʟɪʜᴀᴛ ᴅᴀғᴛᴀʀ ɢʀᴜᴘ ʙᴇʀᴅᴀsᴀʀᴋᴀɴ ᴛᴀɴɢɢᴀʟ.
<i>(ᴄᴏɴᴛᴏʜ: <code>{0}rekapmc 28/03/2026</code>)</i>

💡 <i><b>ɴᴏᴛᴇ:</b> ᴍᴏᴅᴜʟᴇ ɪɴɪ ᴀᴋᴀɴ ᴏᴛᴏᴍᴀᴛɪs ᴍᴇɴᴄᴀᴛᴀᴛ ɢʀᴜᴘ ᴊɪᴋᴀ ᴜʙᴏᴛ ʙᴇʀʜᴀsɪʟ ᴊᴏɪɴ ᴀᴛᴀᴜ ᴅɪᴜɴᴅᴀɴɢ (ɪɴᴠɪᴛᴇᴅ) ᴋᴇ ɢʀᴜᴘ ᴍᴄ.</i></blockquote>
"""

# ==========================================
# 🤖 AUTO DETECTOR (Deteksi otomatis saat join/diundang)
# ==========================================
@Client.on_message(filters.group & filters.new_chat_members, group=5)
async def deteksi_join_mc(client: Client, message):
    try:
        # Cek apakah userbot (kita sendiri) ada di daftar member yang baru masuk
        me = await client.get_me()
        if me.id in [user.id for user in message.new_chat_members]:
            nama_grup = message.chat.title
            tz = pytz.timezone('Asia/Jakarta')
            hari_ini = datetime.now(tz).strftime("%d/%m/%Y")
            
            # Cek database hari ini
            data = await rekap_collection.find_one({"tanggal": hari_ini})
            
            if data:
                # Kalau grup belum ada di list hari ini, tambahin
                if nama_grup not in data["grup"]:
                    await rekap_collection.update_one(
                        {"tanggal": hari_ini},
                        {"$push": {"grup": nama_grup}}
                    )
            else:
                # Bikin dokumen baru buat hari ini
                await rekap_collection.insert_one(
                    {"tanggal": hari_ini, "grup": [nama_grup]}
                )
    except Exception as e:
        print(f"Error Deteksi AutoJoin: {e}")

# ==========================================
# 🚀 HANDLER COMMANDS
# ==========================================

@PY.UBOT("resetmc")
@PY.TOP_CMD
async def cmd_reset_mc(c, m):
    prs_emo = await EMO.PROSES(c)
    sks_emo = await EMO.BERHASIL(c)
    ggl_emo = await EMO.GAGAL(c)
    
    msg = await m.reply(f"<blockquote><b>{prs_emo} ᴍᴇʀᴇsᴇᴛ ᴅᴀᴛᴀ ʀᴇᴋᴀᴘ ʜᴀʀɪ ɪɴɪ...</b></blockquote>")
    
    tz = pytz.timezone('Asia/Jakarta')
    hari_ini = datetime.now(tz).strftime("%d/%m/%Y")
    
    try:
        hasil = await rekap_collection.delete_one({"tanggal": hari_ini})
        
        if hasil.deleted_count > 0:
            await msg.edit(f"<blockquote><b>{sks_emo} ʙᴇʀʜᴀsɪʟ!</b>\nᴅᴀᴛᴀ ʀᴇᴋᴀᴘ ᴍᴄ ᴜɴᴛᴜᴋ ʜᴀʀɪ ɪɴɪ (<code>{hari_ini}</code>) ᴛᴇʟᴀʜ ᴅɪ-ʀᴇsᴇᴛ.</blockquote>")
        else:
            await msg.edit(f"<blockquote><b>{ggl_emo} ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀᴛᴀ.</b>\nʙᴇʟᴜᴍ ᴀᴅᴀ ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ ᴜɴᴛᴜᴋ ʜᴀʀɪ ɪɴɪ (<code>{hari_ini}</code>).</blockquote>")
    except Exception as e:
        await msg.edit(f"<blockquote><b>{ggl_emo} ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:</b>\n<code>{str(e)}</code></blockquote>")

@PY.UBOT("rekapmc")
@PY.TOP_CMD
async def cmd_rekap_mc(c, m):
    prs_emo = await EMO.PROSES(c)
    sks_emo = await EMO.BERHASIL(c)
    ggl_emo = await EMO.GAGAL(c)
    
    msg = await m.reply(f"<blockquote><b>{prs_emo} ᴍᴇɴɢᴀᴍʙɪʟ ᴅᴀᴛᴀ ʀᴇᴋᴀᴘ...</b></blockquote>")
    
    args = m.text.split()
    tz = pytz.timezone('Asia/Jakarta')
    hari_ini = datetime.now(tz).strftime("%d/%m/%Y")

    try:
        # 1. COMMAND: rekapmc (Lihat rekap hari ini)
        if len(args) == 1:
            data = await rekap_collection.find_one({"tanggal": hari_ini})
            
            if not data or not data.get("grup"):
                return await msg.edit(f"<blockquote><b>{ggl_emo} ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ ʜᴀʀɪ ɪɴɪ</b>\n<b>📅 ᴛᴀɴɢɢᴀʟ:</b> <code>{hari_ini}</code>\n\n<i>ʙᴇʟᴜᴍ ᴀᴅᴀ ɢʀᴜᴘ ʏᴀɴɢ ᴅɪ-ᴊᴏɪɴ ʜᴀʀɪ ɪɴɪ.</i></blockquote>")
            
            teks = f"<blockquote><b>{sks_emo} ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ ʜᴀʀɪ ɪɴɪ</b>\n<b>📅 ᴛᴀɴɢɢᴀʟ:</b> <code>{hari_ini}</code>\n\n"
            for i, grup in enumerate(data["grup"], 1):
                teks += f"<b>{i}.</b> <code>{grup}</code>\n"
                
            teks += f"\n📊 <b>ᴛᴏᴛᴀʟ:</b> <code>{len(data['grup'])} ɢʀᴜᴘ ᴍᴄ</code>\n<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ :</b> ɪǫʙᴀʟ ᴜʙᴏᴛ</blockquote>"
            return await msg.edit(teks)

        # 2. COMMAND: rekapmc list (Lihat daftar tanggal)
        elif args[1].lower() == "list":
            cursor = rekap_collection.find({}, {"tanggal": 1, "_id": 0})
            dokumen = await cursor.to_list(length=None)
            
            if not dokumen:
                return await msg.edit(f"<blockquote><b>{ggl_emo} ᴅᴀғᴛᴀʀ ʀᴇᴋᴀᴘ ᴍᴄ</b>\n\n<i>ᴅᴀᴛᴀʙᴀsᴇ ʀᴇᴋᴀᴘ ᴍᴀsɪʜ ᴋᴏsᴏɴɢ.</i></blockquote>")
            
            teks = f"<blockquote><b>{sks_emo} ᴅᴀғᴛᴀʀ ᴛᴀɴɢɢᴀʟ ʀᴇᴋᴀᴘ ᴍᴄ</b>\n\n"
            for i, doc in enumerate(dokumen, 1):
                teks += f"<b>{i}.</b> <code>{doc['tanggal']}</code>\n"
                
            prefix_dipake = m.text[0]
            teks += f"\n💡 <i>ɢᴜɴᴀᴋᴀɴ <code>{prefix_dipake}rekapmc [ᴛᴀɴɢɢᴀʟ]</code> ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴅᴇᴛᴀɪʟ.</i>\n<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ :</b> ɪǫʙᴀʟ ᴜʙᴏᴛ</blockquote>"
            return await msg.edit(teks)

        # 3. COMMAND: rekapmc (tanggal) (Contoh: .rekapmc 28/03/2026)
        else:
            tanggal_dicari = args[1]
            data = await rekap_collection.find_one({"tanggal": tanggal_dicari})
            
            if not data or not data.get("grup"):
                return await msg.edit(f"<blockquote><b>{ggl_emo} ᴅᴀᴛᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>\nᴛɪᴅᴀᴋ ᴀᴅᴀ ʀᴇᴋᴀᴘ ᴍᴄ ᴜɴᴛᴜᴋ ᴛᴀɴɢɢᴀʟ <code>{tanggal_dicari}</code>.</blockquote>")
            
            teks = f"<blockquote><b>{sks_emo} ʀᴇᴋᴀᴘ ᴀᴜᴛᴏᴊᴏɪɴ</b>\n<b>📅 ᴛᴀɴɢɢᴀʟ:</b> <code>{tanggal_dicari}</code>\n\n"
            for i, grup in enumerate(data["grup"], 1):
                teks += f"<b>{i}.</b> <code>{grup}</code>\n"
                
            teks += f"\n📊 <b>ᴛᴏᴛᴀʟ:</b> <code>{len(data['grup'])} ɢʀᴜᴘ ᴍᴄ</code>\n<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ :</b>ᴜʙᴏᴛ</blockquote>"
            return await msg.edit(teks)

    except Exception as e:
        await msg.edit(f"<blockquote><b>{ggl_emo} ᴛᴇʀᴊᴀᴅɪ ᴋᴇsᴀʟᴀʜᴀɴ:</b>\n<code>{str(e)}</code></blockquote>")