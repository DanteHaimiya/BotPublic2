import os
from motor.motor_asyncio import AsyncIOMotorClient
from PyroUbot import *
from pyrogram.types import Message

# Mengambil URL dari config atau environment
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://putraganareal28_db_user:INvoM3X6eqYl1orA@cluster0.cxzq5bk.mongodb.net/?appName=Cluster0")
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["PyroUbot"] # Nama database
collection = db["payment_list"] # Nama koleksi

async def get_payment_db(user_id):
    data = await collection.find_one({"user_id": user_id})
    return data.get("lists", []) if data else []

async def update_payment_db(user_id, lists):
    await collection.update_one(
        {"user_id": user_id},
        {"$set": {"lists": lists}},
        upsert=True
    )

@PY.UBOT("setpayment")
async def _(client, message: Message):
    args = get_arg(message)
    user_id = client.me.id
    
    # Fitur Reset
    if args and args[0].lower() == "reset":
        await update_payment_db(user_id, [])
        return await message.edit("✅ **Semua daftar payment di MongoDB telah direset!**")

    # Ambil list lama
    db_lists = await get_payment_db(user_id)

    # Logika Tambah Payment (Media atau Teks)
    content = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.photo:
            content = {"type": "photo", "file_id": reply.photo.file_id, "caption": reply.caption or ""}
        elif reply.video:
            content = {"type": "video", "file_id": reply.video.file_id, "caption": reply.caption or ""}
        else:
            content = {"type": "text", "value": reply.text or reply.caption}
    else:
        if not args:
            return await message.edit("❌ **Gunakan:** `.setpayment [teks]` atau reply ke media.")
        # Mengambil teks setelah command
        content = {"type": "text", "value": message.text.split(None, 1)[1]}

    db_lists.append(content)
    await update_payment_db(user_id, db_lists)
    await message.edit(f"✅ **Berhasil simpan ke MongoDB (Urutan {len(db_lists)})**")

@PY.UBOT("listpayment")
async def _(client, message: Message):
    user_id = client.me.id
    db_lists = await get_payment_db(user_id)
    
    if not db_lists:
        return await message.edit("📭 **Daftar payment di MongoDB kosong.**")

    res = "**📋 Daftar Payment (MongoDB):**\n\n"
    for i, item in enumerate(db_lists, 1):
        tipe = item['type'].upper()
        val = item.get('value') or item.get('caption') or "Media"
        preview = (val[:20] + "..") if len(val) > 20 else val
        res += f"**{i}.** `[{tipe}]` {preview}\n"
    
    await message.edit(res)

@PY.UBOT("delpayment")
async def _(client, message: Message):
    args = get_arg(message)
    user_id = client.me.id
    if not args:
        return await message.edit("❌ **Gunakan:** `.delpayment [nomor/all]`")

    db_lists = await get_payment_db(user_id)
    
    if args[0].lower() == "all":
        await update_payment_db(user_id, [])
        return await message.edit("🗑 **Semua data di MongoDB dihapus.**")

    try:
        index = int(args[0]) - 1
        if 0 <= index < len(db_lists):
            db_lists.pop(index)
            await update_payment_db(user_id, db_lists)
            await message.edit(f"✅ **Payment nomor {args[0]} dihapus.**")
        else:
            await message.edit("❌ **Nomor tidak ditemukan.**")
    except ValueError:
        await message.edit("❌ **Masukkan angka!**")

@PY.UBOT("pay")
async def _(client, message: Message):
    user_id = client.me.id
    db_lists = await get_payment_db(user_id)
    
    if not db_lists:
        return await message.edit("❌ **Belum ada payment.**")
    
    await message.delete()
    for item in db_lists:
        try:
            if item['type'] == "photo":
                await client.send_photo(message.chat.id, item['file_id'], caption=item['caption'])
            elif item['type'] == "video":
                await client.send_video(message.chat.id, item['file_id'], caption=item['caption'])
            else:
                await client.send_message(message.chat.id, item['value'])
        except Exception as e:
            await client.send_message(message.chat.id, f"❌ Gagal mengirim: {e}")