import re
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pyrogram.errors import MessageNotModified
from PyroUbot import *

# ==========================================
# 🎨 UI DESIGN (LAYOUT UTAMA)
# ==========================================
async def get_main_text(name, user_id, count):
    # Mengambil prefix aktif dari database secara otomatis
    SH = await ubot.get_prefix(user_id)
    prfx = " ".join(SH) if SH else "."
    
    return (
        f"<blockquote><b>🎛️ Menu @{bot.me.username} : 8 Kategori</b></blockquote>\n"
        f"<blockquote><b>✋ Prefixes: {prfx}</b>\n"
        f"<b>🗄️ User: <a href=tg://user?id={user_id}>{name}</a></b></blockquote>"
    )

def get_main_buttons():
    # Layout 2 kolom (Grid) sesuai screenshot
    return [
        [
            InlineKeyboardButton("ℹ️ Info", callback_data="cat_info"),
            InlineKeyboardButton("☪️ Religy", callback_data="cat_religy")
        ],
        [
            InlineKeyboardButton("🎧 Streaming", callback_data="cat_streaming"),
            InlineKeyboardButton("🎨 Creative", callback_data="cat_creative")
        ],
        [
            InlineKeyboardButton("🎬 Media", callback_data="cat_media"),
            InlineKeyboardButton("👤 Private", callback_data="cat_private")
        ],
        [
            InlineKeyboardButton("👥 Group", callback_data="cat_group"),
            InlineKeyboardButton("📥 Download", callback_data="cat_download")
        ],
        [
            # Tombol untuk akses semua modul
            InlineKeyboardButton("📜 All Modules", callback_data="help_back")
        ],
        [
            InlineKeyboardButton("🤖 Userbot Here", url=f"https://t.me/{bot.me.username}")
        ],
        [
            InlineKeyboardButton("❌ Tutup", callback_data="close_user")
        ]
    ]

# ==========================================
# 📖 COMMAND HANDLER (.help)
# ==========================================
@PY.UBOT("help")
async def user_help(client, message):
    bot_username = bot.me.username 
    try:
        # Memanggil melalui Inline Bot agar tampilan tombol muncul
        x = await client.get_inline_bot_results(bot_username, "user_help")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception:
        # Backup jika inline gagal
        text = await get_main_text(message.from_user.first_name, message.from_user.id, len(HELP_COMMANDS))
        await message.reply(text, reply_markup=InlineKeyboardMarkup(get_main_buttons()))

# ==========================================
# 🔍 INLINE QUERY HANDLER
# ==========================================
@PY.INLINE("^user_help")
async def user_help_inline(client, inline_query):
    try:
        user = inline_query.from_user
        text = await get_main_text(user.first_name, user.id, len(HELP_COMMANDS))
        await client.answer_inline_query(
            inline_query.id, cache_time=1,
            results=[InlineQueryResultArticle(
                title="Help Menu",
                input_message_content=InputTextMessageContent(text),
                reply_markup=InlineKeyboardMarkup(get_main_buttons()),
            )]
        )
    except Exception:
        pass

# ==========================================
# 🔄 CALLBACK HANDLER (NAVIGASI & KATEGORI)
# ==========================================
@PY.CALLBACK("^(cat_|help_|back_to_main)")
async def all_help_callback(client, callback_query):
    data = callback_query.data
    user = callback_query.from_user
    
    # Deteksi prefix user untuk isi menu kategori
    SH = await ubot.get_prefix(user.id)
    prfx = SH[0] if SH else "."

    try:
        # 1. LOGIKA TOMBOL KATEGORI
        if data.startswith("cat_"):
            cat = data.split("_")[1]
            menu_map = {
                "info": f"<b>ℹ️ INFO MENU</b>\n\n• <code>{prfx}ping</code>\n• <code>{prfx}id</code>\n• <code>{prfx}info</code>",
                "religy": f"<b>☪️ RELIGY MENU</b>\n\n• <code>{prfx}jadwalsholat</code>\n• <code>{prfx}quran</code>",
                "streaming": f"<b>🎧 STREAMING MENU</b>\n\n• <code>{prfx}play</code>\n• <code>{prfx}song</code>",
                "creative": f"<b>🎨 CREATIVE MENU</b>\n\n• <code>{prfx}q</code>\n• <code>{prfx}stiker</code>",
                "media": f"<b>🎬 MEDIA MENU</b>\n\n• <code>{prfx}poto</code>\n• <code>{prfx}vido</code>",
                "private": f"<b>👤 PRIVATE MENU</b>\n\n• <code>{prfx}pmpermit</code>\n• <code>{prfx}pmlog</code>",
                "group": f"<b>👥 GROUP MENU</b>\n\n• <code>{prfx}kick</code>\n• <code>{prfx}ban</code>\n• <code>{prfx}promote</code>",
                "download": f"<b>📥 DOWNLOAD MENU</b>\n\n• <code>{prfx}sosmed</code>\n• <code>{prfx}ytmp3</code>",
            }

            res_text = menu_map.get(cat, "Menu belum dikonfigurasi.")
            return await callback_query.edit_message_text(
                text=res_text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")]])
            )

        # 2. KEMBALI KE HALAMAN UTAMA
        if data == "back_to_main":
            text = await get_main_text(user.first_name, user.id, len(HELP_COMMANDS))
            return await callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(get_main_buttons())
            )

        # 3. LOGIKA ALL MODULES
        if data == "help_back":
            return await callback_query.edit_message_text(
                text="<b>📜 TOTAL SEMUA MODULES : 315 </b>\n<i>Pilih modul untuk melihat bantuan:</i>",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELP_COMMANDS, "help") + 
                    [[InlineKeyboardButton("🏠 Menu Utama", callback_data="back_to_main")]]
                )
            )
        
        # Paginasi Next/Prev
        if "help_prev" in data or "help_next" in data:
            pg = int(re.search(r"\d+", data).group())
            if "help_prev" in data: pg -= 1
            else: pg += 1
            return await callback_query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(pg, HELP_COMMANDS, "help") +
                    [[InlineKeyboardButton("🏠 Menu Utama", callback_data="back_to_main")]]
                )
            )

        # Klik pada nama modul
        if "help_module" in data:
            mod_name = re.search(r"\((.+?)\)", data).group(1).replace(" ", "_")
            desc = HELP_COMMANDS[mod_name].__HELP__.format(prfx)
            return await callback_query.edit_message_text(
                text=f"<b>📦 MODULE: {mod_name.upper()}</b>\n\n<blockquote>{desc}</blockquote>",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="help_back")]])
            )

    except MessageNotModified:
        await callback_query.answer() 
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)

# ==========================================
# ❌ HANDLING CLOSE
# ==========================================
@PY.CALLBACK("^close_user")
async def close_usernya(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        pass