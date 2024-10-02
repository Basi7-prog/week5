from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables once
load_dotenv('.env')
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
phone = os.getenv('phone')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    print(f'...getting message from {channel_username}',end='\r',flush=True)
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    async for message in client.iter_messages(entity, limit=10000):
        media_path = None
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            
            print(f'\t...downloading photo ({filename})',end='\r',flush=True)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)
        
        # Write the channel title along with other data
        print(f'\t...writting on csv file {channel_username}',end='\r',flush=True)
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

# Initialize the client once
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    channels = [
            # '@helloomarketethiopia',
            '@Shewabrand','@modernshoppingcenter','@sinayelj','@ZemenExpress'  # Existing channel
                 # You can add more channels here
        ]
    for channel in channels:
        with open(f'telegram_data{channel}.csv', 'w', newline='', encoding='utf-8') as file:
            print(f'creating {channel} csv file')
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
            
            # List of channels to scrape
            
            # Iterate over channels and scrape data into the single CSV file
            await scrape_channel(client, channel, writer, media_dir)
            print(f"\t--Scraped data from {channel}")
    
with client:
    client.loop.run_until_complete(main())
