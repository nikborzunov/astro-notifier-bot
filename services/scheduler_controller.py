# services/scheduler_controller.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from services.scheduler import scheduler


class SchedulerController:
    def get_scheduler_keyboard(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Запустить", callback_data="scheduler_start")],
            [InlineKeyboardButton("⏹ Остановить", callback_data="scheduler_stop")],
            [InlineKeyboardButton("🔄 Перезапустить", callback_data="scheduler_restart")],
        ])

    def handle_scheduler_action(self, action: str):
        if action == "scheduler_start":
            scheduler.start()
        elif action == "scheduler_stop":
            scheduler.shutdown()
        elif action == "scheduler_restart":
            scheduler.shutdown(wait=False)
            scheduler.start()


scheduler_controller = SchedulerController()
