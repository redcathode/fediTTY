import random
import time
import os
from mastodon import Mastodon
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

# Register your app - only needs to be done once
'''
mastodon = Mastodon.create_app(
     'pytooterapp',
     api_base_url = 'https://wetdry.world',
     to_file = 'pytooter_clientcred.secret'
)
'''

# Log in - either every time, or use persisted
mastodon = Mastodon(
    access_token=os.getenv('BOT_ACCESS_TOKEN'),
    api_base_url='https://wetdry.world'
)

def post_image_and_log_response():
    # Post the image
    media = mastodon.media_post('./placeholder.png', 'image/png', description="placeholder")
    status = mastodon.status_post(status='', media_ids=[media], visibility='unlisted')

    # Wait for an hour
    time.sleep(60)

    # Get the responses
    notifications = mastodon.notifications()

    # Filter responses to only mentions that are replies to our status
    responses = [n for n in notifications if n['type'] == 'mention' and n['status']['in_reply_to_id'] == status['id']]

    # Find the most favorited response
    if responses:
        max_faves = max(response['status']['favourites_count'] for response in responses)
        top_responses = [response for response in responses if response['status']['favourites_count'] == max_faves]
        most_favorited_response = random.choice(top_responses)
        
       # Extract the plain text from the HTML content
        soup = BeautifulSoup(most_favorited_response['status']['content'], 'html.parser')
        plain_text = soup.get_text()

       # Remove mentions
        plain_text = re.sub(r'@\w+', '', plain_text).strip()

        print(f"Most favorited response: {plain_text}")

        if plain_text.startswith('!ctrl'):
            print("CONTROL")
            print(plain_text[6]) # Print the first character after '!ctrl'
        elif plain_text.startswith('!enter'):
            print("ENTER")
        elif plain_text.startswith('!cmd'):
            print("COMMAND")
            print(plain_text[5:]) # Print everything after '!cmd '
        else:
            print(f"Most favorited response: {plain_text}")
            # print(f"Most favorited response: {most_favorited_response['status']['content']}")
    else:
        print("No responses received.")

# Run the bot
while True:
    post_image_and_log_response()
# mastodon.toot('api test')