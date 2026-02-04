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
        "*SYSTEM ONLINE*\n"
        "`SHEERID VERIFICATION MODULE [PLATINUM]`\n\n"
        "*COMMANDS*\n"
        "`/verify [url]`   Initiate verification sequence\n"
        "`/status      `   Check system operational status\n"
        "`/help        `   Display manual\n\n"
        f"SESSION ID: `{update.effective_user.id}`\n"
        "ACCESS LEVEL: *AUTHORIZED*"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "*MANUAL PROTOCOL*\n\n"
        "1. *SOURCE LINK*: Obtain `verificationId` from target offer page.\n"
        "2. *NETWORK*: End-node must terminate in US Region.\n\n"
        "*COMMAND LIST*\n"
        "`/start ` - System initialization\n"
        "`/verify` - Execute payload [requires link]\n"
        "`/status` - Diagnostic check"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract link
    # Extract link
    if not context.args:
        await update.message.reply_text("ERROR: MISSING ARGUMENT\nUsage: `/verify https://...`", parse_mode=ParseMode.MARKDOWN)
        return

    url = context.args[0]
    user = update.effective_user
    
    # Initialize API
    client = sheerid_api.SheerIDClient(proxy=config.PROXY_URL if config.USE_PROXY else None)
    
    verification_id, is_program = client.extract_verification_id_from_url(url)
    if not verification_id:
        await update.message.reply_text("ERROR: INVALID IDENTIFIER")
        return

    # Notification message
    status_msg = await update.message.reply_text(
        f"*VERIFICATION SEQUENCE INITIATED*\n\n"
        f"ID        :: `{verification_id}`\n"
        f"USER      :: {user.first_name}\n"
        f"TIMESTAMP :: {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"[>>] GENERATING PROFILE...",
        parse_mode=ParseMode.MARKDOWN
    )

    try:
        # Step 1: Generate Profile
        profile = student_generator.generate_student_profile()
        univ_name = profile["display_info"]["university"]
        student_name = profile["display_info"]["full_name"]
        
        await status_msg.edit_text(
            f"*VERIFICATION SEQUENCE INITIATED*\n\n"
            f"ID        :: `{verification_id}`\n"
            f"TARGET    :: {univ_name}\n"
            f"PROFILE   :: {student_name}\n\n"
            f"[>>] INJECTING PAYLOAD...",
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
                f"*VERIFICATION SUCCESSFUL*\n\n"
                f"INSTITUTION :: {univ_name}\n"
                f"IDENTITY    :: {student_name}\n"
                f"EMAIL       :: `{profile['email']}`\n\n"
                f"*REWARD DATA*\n"
            )
            
            if result.get("reward_code"):
                success_text += f"Code      :: `{result['reward_code']}`\n"
                
            if result.get("redirect_url"):
                success_text += f"Link      :: [Direct Connection]({result['redirect_url']})\n"
                
            success_text += "\n[SECURE CONNECTION TERMINATED]"
                
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
            # Extract deep error message
            reason = result.get("reason")
            if isinstance(reason, list):
                reason = ", ".join(reason)
            elif isinstance(result.get("details"), dict):
                 # Try to get systemErrorMessage
                 reason = result["details"].get("systemErrorMessage", "Unknown Error")
            
            error_msg = str(reason or result.get("status", "Unknown"))
            
            await status_msg.edit_text(
                f"*VERIFICATION FAILED*\n\n"
                f"REASON    :: {error_msg}\n"
                f"TARGET    :: {univ_name}\n\n"
                f"HINT      :: Session might be tainted (IP Mismatch).\n"
                f"             Retry with a FRESH link (Copy Link Address).",
                parse_mode=ParseMode.MARKDOWN
            )

    except Exception as e:
        await status_msg.edit_text(f"SYSTEM ERROR: {str(e)}", parse_mode=ParseMode.MARKDOWN)
        logging.error(f"Error processing {verification_id}: {e}")

def run_bot():
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set BOT_TOKEN in config.py")
        return

    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("verify", verify_command))
    
    # Handler for raw links (No /verify needed)
    async def handle_raw_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if "sheerid.com/verify/" in text:
            # Inject arguments so verify_command works
            context.args = [text.strip()]
            await verify_command(update, context)
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_raw_message))

    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
