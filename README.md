# telegramObjectDetectionBot
Telegram Object Detection Bot


Bu proje, Telegram üzerinden gönderilen fotoğraflarda nesne tespiti yapmak için YOLOv8 modelini kullanan bir Telegram botudur. Kullanıcılar bir fotoğraf gönderdiğinde, bot nesneleri tespit eder ve etiketlenmiş görsel ile tespit sonuçlarını geri gönderir.
Özellikler

YOLOv8 ile Nesne Tespiti: Ultralytics YOLOv8 modeli kullanılarak fotoğraflarda nesne tespiti yapılır.
Telegram Entegrasyonu: Kullanıcılar Telegram üzerinden bot ile etkileşime geçebilir.
Hızlı Yanıt: Fotoğraflar hızlı bir şekilde işlenir ve sonuçlar kullanıcıya anında gönderilir.
Esnek Kullanım: Eğitilmiş bir .pt modeli veya hazır YOLOv8 nano modeli kullanılabilir.

Kurulum
Gereksinimler

Python 3.8+
Gerekli Python kütüphaneleri:
pip install telegram python-telegram-bot ultralytics pillow numpy


Adım Adım Kurulum

Depoyu Klonlayın:
git clone https://github.com/ibrahimaydn/telegramObjectDetectionBot.git

Telegram Bot Token'ı Alın:

Telegram'da @BotFather botuna gidin.
/start komutunu gönderin.
/newbot komutunu kullanarak yeni bir bot oluşturun.
BotFather size bir API Token verecektir. Bu token'ı kopyalayın.
Token'ı bot.py dosyasındaki BOT_TOKEN değişkenine yapıştırın:BOT_TOKEN = "buraya_tokeni_yapistir"


Alternatif olarak, token'ı çevre değişkeni olarak ayarlayabilirsiniz:
BOT_TOKEN="buraya_tokeni_yapistir"


YOLO Modelini Seçin:

Eğitilmiş Model Kullanımı: Eğer kendi eğitilmiş .pt modeliniz varsa, YOLO_WEIGHTS değişkenine dosya yolunu ekleyin:
YOLO_WEIGHTS = "best.pt"


Hazır Model Kullanımı: Varsayılan olarak YOLOv8 nano modeli kullanılır:
YOLO_WEIGHTS = YOLO("yolov8n.pt")




Botu Çalıştırın:
python bot.py



Kullanım

Telegram'da botunuzu bulun ve /start komutunu gönderin.
Bir fotoğraf gönderin. Bot, fotoğraftaki nesneleri tespit edecek ve etiketlenmiş görsel ile birlikte tespit sonuçlarını size gönderecektir.
Eğer fotoğraf yerine metin gönderirseniz, bot size fotoğraf göndermeniz gerektiğini hatırlatacaktır.

BotFather ile Token Alma
Telegram botu oluşturmak ve token almak için şu adımları izleyin:

Telegram uygulamasında @BotFather botunu arayın ve sohbeti başlatın.
/start komutunu gönderin.
/newbot komutunu gönderin.
BotFather, botunuzun adını ve kullanıcı adını soracaktır (örneğin, @MyYoloBot).
BotFather size bir API Token verecektir. Bu token, botunuzu programatik olarak kontrol etmek için kullanılır.
Token'ı güvenli bir yerde saklayın ve kimseyle paylaşmayın.
Token'ı bot.py dosyasındaki BOT_TOKEN değişkenine yapıştırın veya çevre değişkeni olarak ayarlayın.

Notlar

Bot, fotoğrafları işlerken YOLOv8 modelini kullanır ve tespit sonuçlarını koordinatlar (bbox) ve güven skoru ile birlikte döndürür.
Eğer etiketlenmiş görsel oluşturulamadıysa, orijinal fotoğraf geri gönderilir ve buna uygun bir not eklenir.
Modelin performansını artırmak için kendi eğitilmiş .pt modelinizi kullanabilirsiniz.

Katkıda Bulunma
Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya issue açın. Geri bildirimleriniz ve önerileriniz her zaman değerlidir!
Lisans
Bu proje MIT Lisansı altında lisanslanmıştır.
