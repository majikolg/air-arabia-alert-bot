# Air Arabia Alert Bot

Bu bot GitHub Actions ile 6 saatte bir Air Arabia kampanya sayfasını kontrol eder ve değişiklik görürse Telegram'a bildirim gönderir.

## Gerekli GitHub Secrets

Repository > Settings > Secrets and variables > Actions bölümüne şunları ekleyin:

- `BOT_TOKEN`: BotFather'dan aldığınız Telegram bot token'ı
- `CHAT_ID`: Telegram kullanıcı/chat ID'niz

## Manuel çalıştırma

GitHub > Actions > Air Arabia Checker > Run workflow

## Güvenlik notu

Bot token'ınızı ekran görüntüsünde veya sohbetlerde paylaştıysanız BotFather üzerinden token'ı yenileyin ve GitHub Secret'ı güncelleyin.
