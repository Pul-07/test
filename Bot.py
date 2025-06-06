from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from sympy import expand, symbols, pretty, solve, sympify, factor, Eq
import math
import os
TOKEN = "TELEGRAM_BOT_TOKEN"

cles = {
    "RW5V4-9QKD3-KL7MA-8HT3P-3G9UQ": {"type": "standard", "date": None},
    "N3FQK-VJ9TU-XZL1C-BPTQM-5J7D2": {"type": "standard", "date": None},
    "MLCX9-FKTZV-7B42W-GAVYH-R81NQ": {"type": "standard", "date": None},
    "T2B8W-KRZ3Y-HM4CE-PL7VA-UX96T": {"type": "standard", "date": None},
    "X5HYL-MU3ZT-DFK89-BPN3C-0VLEA": {"type": "standard", "date": None},
    "LYPWC-KH38N-ZADY3-QX0JR-EUGN7": {"type": "standard", "date": None},
    "E3TU9-LKNVD-HCZ7M-MY3WP-PKJFX": {"type": "standard", "date": None},
    "ZXTP9-DCJQK-LYUR8-KXA37-NJMVC": {"type": "standard", "date": None},
    "B3YH8-QK7LM-XFZ9P-PYVWC-TGJ9E": {"type": "standard", "date": None},
    "VLU8Z-X4NEH-R97KW-3TDLP-KMFYA": {"type": "standard", "date": None},
    "3RKZC-YXP58-VTNLA-EQJY2-MGXWF": {"type": "pro", "date": None},
    "U38TZ-NAVCP-H4EKR-JZ91B-XTFDQ": {"type": "pro", "date": None},
    "JYWR4-K9D3V-LPTU2-XGQWZ-BEVY1": {"type": "pro", "date": None},
    "WL9CP-Q4MUK-DTVN3-AHF52-X7MZK": {"type": "pro", "date": None},
    "ZKJRP-E9WXN-YC6FU-3AVKQ-HGDY3": {"type": "pro", "date": None},
    "DFZT8-KVJLM-NW4HR-YXCG9-JBVU2": {"type": "premium", "date": None},
    "KT94X-WUEJG-LZP9N-YRCV3-H8EMQ": {"type": "premium", "date": None},
    "Y5TVF-ZALJX-KPU9N-CHVE7-XQMRD": {"type": "premium", "date": None},
    "NXD2C-WY9RL-MQZTP-K83FV-JUGET": {"type": "premium", "date": None},
    "FP3ZC-K9YRL-ZVUXQ-NMTA8-HJEW2": {"type": "premium", "date": None},
}

users = {}
a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = symbols('a b c d e f g h i j k l m n o p q r s t u v w x y z')

def enregistrer_utilisateur(user_id, info):
    with open("utilisateurs.txt", "a") as f:
        ligne = f"{user_id},{info['key']},{info['type']},{info['expire'] if info['expire'] else 'illimité'}\n"
        f.write(ligne)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenue ! Tape /licence pour entrer ta clé. Ensuite, utilise /menu. Achetez une clé de licence ici https://sites.google.com/view/math-cl-de-licence/accueil ")

async def licence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "licence"
    await update.message.reply_text("🔐 Envoie ta clé maintenant.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        await update.message.reply_text("⛔ Tu n'as pas encore de licence active. Utilise /licence.")
        return
    await update.message.reply_text("📘 Menu : /fact /dev /simp /ppcm /pgcd /cramer")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    txt = update.message.text.strip().upper()

    # Si on est en mode licence
    if context.user_data.get("mode") == "licence":
        if user_id in users:
            await update.message.reply_text("✅ Tu as déjà une licence.")
            context.user_data["mode"] = None
            return

        if txt in cles:
            key_info = cles[txt]
            if key_info["date"] is not None:
                await update.message.reply_text("❌ Clé déjà utilisée.")
                return

            now = datetime.now()
            expire = {
                "standard": now + timedelta(days=3),
                "premium": now + timedelta(days=90),
                "pro": None
            }.get(key_info["type"], None)

            users[user_id] = {
                "key": txt,
                "type": key_info["type"],
                "expire": expire
            }
            cles[txt]["date"] = now
            await update.message.reply_text(f"✅ Clé {txt} activée ({key_info['type']}) !")
            enregistrer_utilisateur(user_id, users[user_id])
            context.user_data["mode"] = None
        else:
            await update.message.reply_text("❌ Clé invalide. La clé doit être sous ce format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX")
        return

    await process_expr(update, context)

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users: return await update.message.reply_text("⛔ Pas de licence.")
    await update.message.reply_text("Envoie l'expression à factoriser.")
    context.user_data['mode'] = 'fact'

async def dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users: return await update.message.reply_text("⛔ Pas de licence.")
    await update.message.reply_text("Envoie l'expression à développer.")
    context.user_data['mode'] = 'dev'

async def simp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users: return await update.message.reply_text("⛔ Pas de licence.")
    await update.message.reply_text("Envoie l'expression à simplifier.")
    context.user_data['mode'] = 'simp'

async def ppcm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Donne deux entiers séparés par un espace : ex: 12 15")
    context.user_data['mode'] = 'ppcm'

async def pgcd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Donne deux entiers séparés par un espace : ex: 18 24")
    context.user_data['mode'] = 'pgcd'

async def cramer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envoie les 6 coefficients a1 b1 c1 a2 b2 c2 (séparés par un espace).")
    context.user_data['mode'] = 'cramer'

async def process_expr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    txt = update.message.text.strip()
    if mode == 'fact':
        try:
            result = factor(expand(txt))
            await update.message.reply_text(pretty(result))
        except:
            await update.message.reply_text("Erreur de factorisation.")
    elif mode == 'dev':
        try:
            result = pretty(expand(txt))
            await update.message.reply_text(result)
        except:
            await update.message.reply_text("Erreur de développement.")
    elif mode == 'simp':
        try:
            result = pretty(sympify(expand(txt)))
            await update.message.reply_text("Forme simplifiée :\n" + result)
        except:
            await update.message.reply_text("Erreur de simplification.")
    elif mode == 'ppcm':
        try:
            a, b = map(int, txt.split())
            await update.message.reply_text(f"PPCM({a},{b}) = {math.lcm(a,b)}")
        except:
            await update.message.reply_text("Erreur dans les nombres.")
    elif mode == 'pgcd':
        try:
            a, b = map(int, txt.split())
            await update.message.reply_text(f"PGCD({a},{b}) = {math.gcd(a,b)}")
        except:
            await update.message.reply_text("Erreur dans les nombres.")
    elif mode == 'cramer':
        try:
            a1, b1, c1, a2, b2, c2 = map(int, txt.split())
            D = a1*b2 - a2*b1
            Dx = b1*c2 - b2*c1
            Dy = a1*c2 - a2*c1
            if D == 0:
                if Dx == 0 and Dy == 0:
                    await update.message.reply_text("Système : infinité de solutions.")
                else:
                    await update.message.reply_text("Pas de solution.")
            else:
                x = Dx/D
                y = Dy/D
                await update.message.reply_text(f"x = {x}, y = {y}")
        except:
            await update.message.reply_text("Erreur dans les données.")
    context.user_data['mode'] = None

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("licence", licence))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("fact", fact))
app.add_handler(CommandHandler("dev", dev))
app.add_handler(CommandHandler("simp", simp))
app.add_handler(CommandHandler("ppcm", ppcm))
app.add_handler(CommandHandler("pgcd", pgcd))
app.add_handler(CommandHandler("cramer", cramer))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot lancé...")
app.run_polling()
