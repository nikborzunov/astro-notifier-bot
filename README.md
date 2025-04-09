# AstroNotifierBot

**AstroNotifierBot** is a Telegram bot that provides users with real-time alerts and information about cosmic events, dangerous asteroids, and daily space photos provided by NASA. The bot uses the NASA API to fetch the latest data and deliver it directly to users.

## Features
- **Cosmic Event Notifications**: Get alerts about upcoming cosmic events (e.g., eclipses, meteor showers).
- **Dangerous Asteroids**: Get information about asteroids that could potentially be hazardous to Earth.
- **Space Photos**: Receive a fresh space photo from NASA every day.

## Technologies Used
- **Python 3.x**
- **python-telegram-bot** library for interacting with Telegram API
- **NASA API** for fetching space-related data
- **SQLite** for storing user preferences and settings

## Setup and Installation

### Prerequisites
To run the bot, you need:
- Python 3.x installed on your machine.
- A Telegram bot token (you can create one using [BotFather](https://core.telegram.org/bots#botfather)).
- A NASA API key (you can get it from [NASA's API portal](https://api.nasa.gov/)).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AstroNotifierBot.git
   cd AstroNotifierBot
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Telegram Bot token and NASA API key:

   ```bash
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   NASA_API_KEY=your_nasa_api_key
   ```

5. Run the bot:

   ```bash
   python bot.py
   ```

### Database Setup

The bot uses SQLite to store user preferences and settings. When you run the bot for the first time, the database will be automatically created.

### Usage

Once the bot is running, search for `@AstroNotifierBot` in Telegram and start a conversation. You can configure preferences such as:
- Whether to receive alerts about cosmic events.
- Whether to receive notifications about dangerous asteroids.
- Opt-in to daily space photos.

## Contributing

Feel free to fork the repository and submit pull requests with improvements or bug fixes. Here are some ideas for contribution:
- Add more notifications for different space events.
- Improve the user interface of the bot.
- Add more error handling and logging.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Created by
[**@kupilulitku**](https://t.me/kupilulitku)