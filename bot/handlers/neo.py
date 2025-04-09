from services.nasa_api import get_near_earth_objects  # Import function to fetch NEO data from NASA API
from bot.handlers.message_utils import send_message_with_keyboard  # Import function to send messages with keyboard
from utils.logger import logger  # Logging utility
from datetime import datetime, timedelta

# Function to send Near-Earth Objects (NEO) data
async def send_neo(query):
    try:
        # Fetch NEO data from NASA API without a date filter
        neo_data = get_near_earth_objects()  
        
        if neo_data:
            # Initial message to explain NEO data
            neo_message = (
                "🌌 **Potentially Hazardous Near-Earth Objects (NEOs)** 🚀\n\n"
                "NEOs are asteroids and comets that orbit the Sun and can come close to Earth. "
                "While they don't all pose a threat, we closely monitor their movements. "
                "Here are some of the most important NEOs currently approaching our planet. 🪐\n\n"
                "🔭 **Details on each NEO:**\n\n"
            )

            # Process each NEO and append to the message
            for index, neo in enumerate(neo_data, start=1):  
                # Extract NEO name, default to "Unknown" if not available
                neo_name = neo.get("name", "Unknown")  
                
                try:
                    # Try to get NEO diameter, set to "Unknown" if not available
                    neo_diameter = float(neo["estimated_diameter"]["meters"]["estimated_diameter_max"])
                except (KeyError, ValueError):
                    neo_diameter = "Unknown" 

                try:
                    # Check for close approach data (date and velocity)
                    if neo.get("close_approach_data"):
                        neo_velocity = float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
                        neo_approach_date = neo["close_approach_data"][0]["close_approach_date"]
                    else:
                        neo_velocity = "Unknown"
                        neo_approach_date = "Unknown"
                except (KeyError, ValueError, IndexError):
                    neo_velocity = "Unknown"
                    neo_approach_date = "Unknown"
                
                # Format velocity display
                if isinstance(neo_velocity, float):
                    neo_velocity_display = f"⚡ **Speed**: {neo_velocity:,.2f} km/h"
                else:
                    neo_velocity_display = f"⚡ **Speed**: {neo_velocity if neo_velocity != 'Unknown' else 'Data not available'}"
                
                # Format closest approach date display
                if neo_approach_date != 'Unknown':
                    neo_approach_date_display = f"📅 **Closest Approach**: {neo_approach_date}"
                else:
                    neo_approach_date_display = "📅 **Closest Approach**: Data not available"
                
                # Debugging output to log missing data
                logger.info(f"Velocity: {neo_velocity_display}")
                logger.info(f"Closest Approach: {neo_approach_date_display}")
                
                # Create formatted message for each NEO with clear structure
                neo_message += (
                    f"🪐 **{neo_name}**  🌌 **Size**: {neo_diameter:,.2f} m\n"  # NEO name and size in one line
                    f"{neo_velocity_display}\n"  # NEO velocity
                    f"{neo_approach_date_display}\n"  # NEO closest approach date
                    "\n━━━━━━━━━━━━━━━━━━━━━\n"  # Separator between NEOs
                )

            # Final message formatting
            neo_message += "\nStay curious and safe! 🌌💫"
            
            # Sending the detailed message with NEO information
            await send_message_with_keyboard(query, neo_message)
            logger.info(f"Sent NEO data to {query.from_user.username}")
        else:
            # If no NEO data is fetched, inform the user
            neo_message = (
                "⚠️ **Oops!** We couldn't fetch the Near-Earth Objects data at the moment. "
                "Please try again later. 🌌"
            )
            await send_message_with_keyboard(query, neo_message)

    except Exception as e:
        # Handle errors gracefully and notify the user
        logger.error(f"Error in NEO: {e}")
        await send_message_with_keyboard(query, "⚡ Something went wrong while fetching NEO data! Please try again later.")
