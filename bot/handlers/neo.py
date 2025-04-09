from services.nasa_api import get_near_earth_objects  
from bot.handlers.message_utils import send_message_with_keyboard  
from utils.logger import logger  
from datetime import datetime

async def send_neo(query):
    try:
        neo_data = get_near_earth_objects()

        if neo_data:
            def get_approach_date(neo):
                try:
                    return datetime.strptime(neo["close_approach_data"][0]["close_approach_date"], "%Y-%m-%d")
                except:
                    return datetime.min

            sorted_neo = sorted(neo_data, key=get_approach_date, reverse=True)

            top_neo = sorted_neo[:10]

            def get_diameter(neo):
                try:
                    return float(neo["estimated_diameter"]["meters"]["estimated_diameter_max"])
                except (KeyError, ValueError):
                    return 0

            sorted_top_neo = sorted(top_neo, key=get_diameter, reverse=True)

            neo_message = (
                "🌌 **Today's Potentially Hazardous Near-Earth Objects (NEOs)** 🚀\n\n"
                "These are asteroids and comets that are closely approaching Earth today. "
                "Let's take a look at the most important NEOs passing by today! 🪐\n\n"
                "🔭 **Details on each NEO:**\n\n"
            )

            for index, neo in enumerate(sorted_top_neo, start=1):
                neo_name = neo.get("name", "Unknown")
                
                try:
                    neo_diameter = float(neo["estimated_diameter"]["meters"]["estimated_diameter_max"])
                except (KeyError, ValueError):
                    neo_diameter = "Unknown"

                try:
                    if neo.get("close_approach_data"):
                        neo_velocity = float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
                        neo_approach_date = neo["close_approach_data"][0]["close_approach_date"]
                        neo_min_distance = float(neo["close_approach_data"][0]["miss_distance"]["kilometers"])
                    else:
                        neo_velocity = "Unknown"
                        neo_approach_date = "Unknown"
                        neo_min_distance = "Unknown"
                except (KeyError, ValueError, IndexError):
                    neo_velocity = "Unknown"
                    neo_approach_date = "Unknown"
                    neo_min_distance = "Unknown"

                try:
                    neo_discovery_date = neo.get("discovery_date", "Unknown")
                except KeyError:
                    neo_discovery_date = "Unknown"

                try:
                    neo_object_type = neo.get("is_potentially_hazardous_asteroid", "Unknown")
                except KeyError:
                    neo_object_type = "Unknown"
                
                if isinstance(neo_velocity, float):
                    neo_velocity_display = f"⚡ **Speed**: {neo_velocity:,.2f} km/h"
                else:
                    neo_velocity_display = f"⚡ **Speed**: {neo_velocity if neo_velocity != 'Unknown' else 'Data not available'}"
                
                if neo_approach_date != 'Unknown':
                    neo_approach_date_display = f"📅 **Closest Approach**: {neo_approach_date}"
                else:
                    neo_approach_date_display = "📅 **Closest Approach**: Data not available"
                
                neo_min_distance_display = f"🌍 **Min Distance**: {neo_min_distance:.3f} km" if neo_min_distance != "Unknown" else "🌍 **Min Distance**: Data not available"
                
                neo_message += (
                    f"🪐 **{neo_name}** \n"
                    f"🌌 **Size**: {neo_diameter if isinstance(neo_diameter, float) else 'Unknown'} m\n"
                    f"{neo_velocity_display}\n"
                    f"{neo_approach_date_display}\n"
                    f"{neo_min_distance_display}\n"
                    f"🔭 **Discovery Date**: {neo_discovery_date}\n"
                    f"🚀 **Object Type**: {'Asteroid' if neo_object_type else 'Comet'}\n"
                    "\n━━━━━━━━━━━━━━━━━━━━━\n"
                )

            neo_message += "\nStay curious and safe! 🌌💫"
            
            await send_message_with_keyboard(query, neo_message)
            logger.info(f"Sent NEO data to {query.from_user.username}")
        else:
            await send_message_with_keyboard(query, "⚠️ No recent Near-Earth Object events found today.")
    
    except Exception as e:
        logger.error(f"Error in sending NEO data: {e}")
        await send_message_with_keyboard(query, "⚡ Something went wrong while fetching today's NEO data! Please try again later.")
