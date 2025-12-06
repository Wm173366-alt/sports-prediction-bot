from telegram import Update
from telegram.ext import ContextTypes
from analysis.predictor import Predictor

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bienvenue sur Google Antigravity - Intelligence ultime de prédiction sportive.\n\nUtilisez /predict pour voir les prédictions du jour.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Commandes disponibles:\n/start - Démarrer\n/predict - Voir les prédictions\n/help - Aide")

async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictor = Predictor()
    results = predictor.predict_upcoming_matches()
    
    if not results:
        await update.message.reply_text("Aucun match à venir trouvé dans la base de données.")
        return

    message = "🔮 **Prédictions Google Antigravity** 🔮\n\n"
    
    # Chunking messages to avoid limit
    MAX_LENGTH = 3000
    current_day = None

    for res in results:
        # Extract Day (Assuming format "dd/mm HH:MM")
        match_day = res['date'].split(' ')[0]
        
        if match_day != current_day:
            current_day = match_day
            header = f"\n📅 ═══ **{current_day}** ═══ 📅\n\n"
            if len(message) + len(header) > MAX_LENGTH:
                await update.message.reply_text(message, parse_mode='Markdown')
                message = "🔮 **Suite...**\n\n"
            message += header

        # Cleaner, Stylish Format
        match_title = res['match'].replace("⚽", "").replace("🏀", "").strip() # Clean old icons if present
        sport_icon = "🏀" if res.get('sport') == 'basketball' else "⚽"
        
        entry = f"{sport_icon}  **{match_title}**\n" 
        entry += f"🕐  _{res['date'].split(' ')[1]}_\n\n" 
        
        entry += f"🎯  **PRONO : {res['prediction']}**\n"
        entry += f"⚡  _Confiance : {res['confidence']}_\n\n"
        
        entry += "📝  *Détails & Stats :*\n"
        entry += f"  • 🥅  {res['goals']}\n"
        
        if res.get('sport') == 'football':
            entry += f"  • 🚩  Corners : {res['corners']}\n"
            entry += f"  • 🛡️  Fautes : {res['fouls']}\n"
            entry += f"  • 🟨  Cartons : {res['yellow_cards']}\n"
        
        entry += "\n══════════════════════\n"
        
        if len(message) + len(entry) > MAX_LENGTH:
            await update.message.reply_text(message, parse_mode='Markdown')
            message = "🔮 **Suite...**\n\n" + (f"\n📅 ═══ **{current_day}** ═══ 📅\n\n" if current_day else "")
        
        message += entry
    
    if len(message) > 0:
        await update.message.reply_text(message, parse_mode='Markdown')
