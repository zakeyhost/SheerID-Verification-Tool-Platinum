"""
Telegram Bot Interface for SheerID Verification
"""
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.constants import ParseMode

import config
import sheerid_api
import student_generator
import doc_generator
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🤖 **SheerID Auto Verifier Bot**\n\n"
        "I can automatically verify student status for Gemini AI/Youtube Premium offers.\n\n"
        "**How to use:**\n"
        "1. Get a student offer link (e.g. from Google One AI Premium page)\n"
        "2. Send command: `/verify <YOUR_LINK>`\n\n"
        "**Example:**\n"
        "`/verify https://services.sheerid.com/verify/...`\n\n"
        "⚠️ **Note:** Use US VPN (IP is critical!)"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📚 **Help Guide**\n\n"
        "1. **Link Format**: Must contain `verificationId` (usually inside `/verify/` URL)\n"
        "2. **VPN**: You MUST be connected to a US VPN. The bot runs on this server, but if you are clicking the final link, your IP matters too.\n"
        "Wait... actually the bot does the submission, so the bot's server IP is what matters. "
        "Make sure this bot is running on a server with US IP/Proxy!\n\n"
        "**Commands:**\n"
        "/start - Start bot\n"
        "/verify <link> - Verify a link\n"
        "/status - Check bot health"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract link
    if not context.args:
        await update.message.reply_text("❌ Please provide a link!\nUsage: `/verify https://...`", parse_mode=ParseMode.MARKDOWN)
        return

    url = context.args[0]
    user = update.effective_user
    
    # Initialize API
    client = sheerid_api.SheerIDClient(proxy=config.PROXY_URL if config.USE_PROXY else None)
    
    verification_id, is_program = client.extract_verification_id_from_url(url)
    if not verification_id:
        await update.message.reply_text("❌ Invalid link! Could not find verification ID.")
        return

    # Notification message
    status_msg = await update.message.reply_text(
        f"🔄 **Processing Request**\n"
        f"🆔 ID: `{verification_id}`\n"
        f"👤 User: {user.first_name}\n"
        f"⏳ Status: Generating student profile...",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Step 1: Generate Profile
        profile = student_generator.generate_student_profile()
        univ_name = profile["display_info"]["university"]
        student_name = profile["display_info"]["full_name"]
        
        await status_msg.edit_text(
            f"🔄 **Processing Request**\n"
            f"🆔 ID: `{verification_id}`\n"
            f"🏫 Univ: {univ_name}\n"
            f"👤 Name: {student_name}\n"
            f"⏳ Status: Submitting to SheerID...",
            parse_mode=ParseMode.MARKDOWN
        )

        # Step 2: Submit
        # Define doc generator wrapper
        def doc_gen_wrapper(first, last, school):
             # Randomly choose ID or Transcript
             if doc_generator.select_document_type() == "student_id":
                 return doc_generator.generate_student_id(first, last, school)
             else:
                 # Need DOB for transcript
                 return doc_generator.generate_transcript(first, last, profile["birthDate"], school)

        result = client.process_verification(verification_id, is_program, profile, doc_gen_wrapper)
        
        # Step 3: Handle Result
        if result["status"] == "SUCCESS":
            success_text = (
                f"✅ **VERIFICATION SUCCESS!**\n\n"
                f"🎓 University: {univ_name}\n"
                f"👤 Identity: {student_name}\n"
                f"📧 Email: `{profile['email']}`\n\n"
            )
            
            if result.get("reward_code"):
                success_text += f"🎁 **Reward Code:** `{result['reward_code']}`\n"
                
            if result.get("redirect_url"):
                success_text += f"🔗 [Click to Claim Offer]({result['redirect_url']})\n"
                
            await status_msg.edit_text(success_text, parse_mode=ParseMode.MARKDOWN)
            
        elif result["status"] == "TIMEOUT":
             last_step = result.get("last_details", {}).get("currentStep")
             if last_step == "pending":
                  await status_msg.edit_text(
                      f"⏳ **Under Manual Review**\n\n"
                      f"✅ Documents Submitted Successfully.\n"
                      f"The verification is pending review by SheerID.\n"
                      f"🤖 **I will notify you automatically when it finishes!** (Monitoring for 30 mins)\n"
                      f"Please check this link manually if I don't respond:\n"
                      f"`{url}`",
                      parse_mode=ParseMode.MARKDOWN
                  )
                  
                  # Spawn background monitor
                  import subprocess
                  subprocess.Popen(["python3", "monitor_task.py", verification_id, str(update.effective_chat.id)])
                  
             else:
                  await status_msg.edit_text("⚠️ Verification timed out. Please check the link manually.", parse_mode=ParseMode.MARKDOWN)
        
        else:
            error_codes = result.get("errors", result.get("reason", "Unknown"))
            await status_msg.edit_text(
                f"❌ **Verification Failed**\n"
                f"Reason: {error_codes}\n"
                f"Univ: {univ_name}\n\n"
                f"Try generating a new link and trying again!",
                parse_mode=ParseMode.MARKDOWN
            )

    except Exception as e:
        await status_msg.edit_text(f"❌ **System Error:** {str(e)}", parse_mode=ParseMode.MARKDOWN)
        logging.error(f"Error processing {verification_id}: {e}")

def run_bot():
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set BOT_TOKEN in config.py")
        return

    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("verify", verify_command))
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
