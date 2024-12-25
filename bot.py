import loader
if loader.DEBUG:
    from aiogram import executor
else:
    from aiogram.utils.executor import start_webhook
    from settings import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT


import admin_handlers
import user_handlers

if __name__ == '__main__':

    # Параметры бота настроены, базы данных запущены или готовы к запуску, запустить бота
    print('bot.py: Запуск бота.')

    # Запуск тестирования и разработки.
    if loader.DEBUG:
        print('Debug True. Start polling.')
        executor.start_polling(loader.dp, skip_updates=True, on_startup=loader.on_startup,
                               on_shutdown=loader.on_shutdown)

    # Запуск Production среды!
    else:
        print('Debug False. Start webhook.')
        start_webhook(loader.dp, WEBHOOK_PATH, on_startup=loader.on_startup, on_shutdown=loader.on_shutdown,
                      skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)
