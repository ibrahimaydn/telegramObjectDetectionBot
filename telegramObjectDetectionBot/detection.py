# bot.py
import os
import io
import asyncio
from PIL import Image
import numpy as np

from ultralytics import YOLO

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

#eğitilmiş modelin var ise 1. yöntemi yoksa 2. yöntemi kullanabilirisn

# 1. eğitilen .pt uzantılı dosya buraya eklenecektir
#YOLO_WEIGHTS = os.environ.get("YOLO_WEIGHTS", "best.pt")

# 2. Hazır YOLOv8 nano modelini yükleyerek çalışmak için br yol
YOLO_WEIGHTS = YOLO("yolov8n.pt")


#Telegram BotFather'dan alınan token buraya yapıştırılacak
BOT_TOKEN = "TOKEN"

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN çevresel değişkeni bulunamadı. 'export BOT_TOKEN=...' ile ayarla.")

# Modeli yükle (senkron yükleme)
print("YOLO model yükleniyor:", YOLO_WEIGHTS)
model = YOLO(YOLO_WEIGHTS)
print("Model yüklendi. Sınıf isimleri:", model.names)




async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! bir fotoğraf gönder, nesne tespiti yapıp sonuçla birlikte etiketli görseli geri göndereyim."
    )


def _format_detections(results):

    boxes = results.boxes  # Boxes objesi
    if boxes is None or len(boxes) == 0:
        return "Herhangi bir nesne tespit edilmedi."
    lines = []
    for i, box in enumerate(boxes):
        cls = int(box.cls[0]) if hasattr(box.cls, "__len__") else int(box.cls)
        conf = float(box.conf[0]) if hasattr(box.conf, "__len__") else float(box.conf)
        name = model.names[cls] if cls in model.names else str(cls)
        xyxy = box.xyxy[0].tolist() if hasattr(box.xyxy, "__len__") else box.xyxy.tolist()
        lines.append(
            f"{i + 1}. {name} — {conf:.2f} (bbox: {int(xyxy[0])},{int(xyxy[1])},{int(xyxy[2])},{int(xyxy[3])})")
    return "\n".join(lines)


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    await msg.reply_chat_action("typing")
    photo = msg.photo[-1]
    file = await photo.get_file()
    bio = io.BytesIO()
    await file.download_to_memory(out=bio)
    bio.seek(0)

    loop = asyncio.get_running_loop()

    def run_inference(image_bytes):

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        results = model.predict(source=np.array(img), conf=0.25, imgsz=640, verbose=False)
        return results[0]

    image_bytes = bio.getvalue()
    try:
        results = await loop.run_in_executor(None, run_inference, image_bytes)
    except Exception as e:
        await msg.reply_text("Model çalıştırılırken hata oluştu: " + str(e))
        return

    caption = _format_detections(results)

    try:
        annotated = results.plot()
        annotated_img = Image.fromarray(annotated)
        out_buf = io.BytesIO()
        annotated_img.save(out_buf, format="JPEG")
        out_buf.seek(0)
    except Exception as e:
        out_buf = io.BytesIO(image_bytes)
        out_buf.seek(0)
        caption += "\n(Not: etiketlenmiş görsel oluşturulamadı.)"

    # Gönder
    await msg.reply_photo(photo=InputFile(out_buf, filename="result.jpg"), caption=caption)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fotoğraf gönderirsen nesne tespiti yaparım. /start ile başlayabilirsin.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot çalışıyor...")
    app.run_polling()


if __name__ == "__main__":
    main()
