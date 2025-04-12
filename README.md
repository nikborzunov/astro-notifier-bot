# **AstroNotifierBot**

**AstroNotifierBot** is a Telegram bot that provides users with real-time alerts and information about cosmic events, dangerous asteroids, and daily space photos from NASA. The bot fetches the latest data from NASA's APIs and delivers it directly to users.

## **Features**
- **Cosmic Event Notifications**: Receive alerts about upcoming cosmic events (e.g., eclipses, meteor showers).
- **Dangerous Asteroids**: Get information about potentially hazardous asteroids.
- **Space Photos**: Receive a fresh space photo from NASA every day at 8 AM (APOD - Astronomy Picture of the Day).

## **Technologies Used**
- **Python 3.x**
- **python-telegram-bot**: For interacting with Telegram's API.
- **NASA API**: To fetch data related to cosmic events and dangerous asteroids.
- **NASA Images API**: For fetching space photos of the day (APOD).
- **SQLite**: For storing user preferences, configurations, and event data.
- **APScheduler**: For scheduling tasks, such as sending daily space photos at a set time.
- **dotenv**: To manage environment variables like the Telegram Bot token and NASA API key.

## **Setup and Installation**

### **Prerequisites**
To run the bot, you'll need:
- Python 3.x installed on your machine.
- A **Telegram Bot Token** (you can create one by chatting with [BotFather](https://core.telegram.org/bots#botfather)).
- A **NASA API Key** (you can get it from [NASA's API portal](https://api.nasa.gov/)).
- Optionally, Docker, if you'd like to deploy the bot via Docker.

### **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nikborzunov/AstroNotifierBot.git
   cd AstroNotifierBot
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the project root directory** and add your Telegram Bot token and NASA API key:

   ```bash
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   NASA_API_KEY=your_nasa_api_key
   ```

5. **Run the bot:**

   ```bash
   python app/telegram_bot/bot.py
   ```

### **Database Setup**

The bot uses **SQLite** to store user preferences, event data, and the history of potential asteroid threats. When you run the bot for the first time, the database will be automatically created and populated with necessary tables.

### **Usage**

Once the bot is running, search for `@AstroNotifierBot` in Telegram and start a conversation. You can configure the following preferences:
- **Receive alerts about upcoming cosmic events**.
- **Receive notifications about dangerous asteroids**.
- **Opt-in to daily space photos** (APOD) delivered at 8 AM UTC.

You can use the following commands:
- **/start** — To start interacting with the bot.
- **/scheduler_start** — To start receiving scheduled notifications (e.g., daily space photo).
- **/scheduler_stop** — To stop scheduled notifications.
- **/neo** — To get information about current potentially dangerous asteroids.
- **/neo_history** — To get historical data on potentially dangerous asteroids.

---

## **Project Structure**

The project is organized as follows:

```
astro_notifier_bot/
├── app/                                 # Main application logic
│   ├── telegram_bot/                    # Telegram bot interface
│   │   ├── bot.py                       # Bot startup and settings
│   │   ├── handlers/                    # Handlers for Telegram events
│   │   │   ├── commands/                # Telegram commands (/start, /scheduler, etc.)
│   │   │   ├── callbacks/               # Inline button callbacks
│   │   ├── ui/                          # UI components (messages, keyboards)
│   ├── services/                        # Interaction with external APIs, notifications
│   ├── db/                              # Database and models
│   ├── core/                            # Core functionality (scheduler, etc.)
│   ├── utils/                           # Helper utilities (logging, NEO utils, etc.)
├── main.py                              # Main entry point
├── .env                                 # Environment variables (API keys, tokens)
├── requirements.txt                     # Project dependencies
├── Dockerfile                           # Docker image for deployment (optional)
├── Makefile                             # Utilities for project management (build, tests)
└── README.md                            # Project documentation
```

---

## **Contributing**

Feel free to fork the repository and submit pull requests with improvements, bug fixes, or new features. Here are some ideas for contributions:
- Add more types of space event notifications.
- Improve the user interface and interactions within the Telegram bot.
- Implement additional error handling and logging features.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Created by**

[**@kupilulitku**](https://t.me/kupilulitku)