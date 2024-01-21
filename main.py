import random
import time
import os
from mastodon import Mastodon
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import libvirt_test
import cv2
import pytesseract
            
# stream.send(string_to_send)
# stream.finish()
load_dotenv()


# # Register your app - only needs to be done once
# '''
# mastodon = Mastodon.create_app(
#      'pytooterapp',
#      api_base_url = 'https://wetdry.world',
#      to_file = 'pytooter_clientcred.secret'
# )
# '''
# print(os.getenv("BOT_ACCESS_TOKEN"))
# Log in 
mastodon = Mastodon(
    access_token=os.getenv("BOT_ACCESS_TOKEN"),
    api_base_url='https://fedi.computernewb.com'
)

def post_image_and_log_response():
    # Post the image
    media_filename = f"./{libvirt_test.grab_screenshot()}"
    print(f"screenshotted {media_filename}")
    img = cv2.imread(media_filename)
    ocr = "[automatic] OCR of the screenshot: \n" + pytesseract.image_to_string(img)
    media = mastodon.media_post(media_filename, 'image/png', description=ocr)
    status = mastodon.status_post(status='', media_ids=[media], visibility='public')

    # Wait for an hour
    time.sleep((2 * 3600) - (15 * 60))
    # time.sleep(60 * 5)

    # Get the responses
    notifications = mastodon.notifications()

    # Filter responses to only mentions that are replies to our status
    responses = [n for n in notifications if n['type'] == 'mention' and n['status']['in_reply_to_id'] == status['id'] and any(keyword in n['status']['content'] for keyword in ['!ctrl', '!enter', '!cmd']) and not any(keyword in n['status']['content'] for keyword in ['shutdown', 'masscan', 'nmap'])]
    # FIXME: we should really check if the response starts with '!' after all the mentions
    # this might break in weird ways later
    
    # Find the most favorited response
    if responses:
        max_faves = max(response['status']['favourites_count'] for response in responses)
        top_responses = [response for response in responses if response['status']['favourites_count'] == max_faves]
        most_favorited_response = random.choice(top_responses)
        
       # Extract the plain text from the HTML content
        soup = BeautifulSoup(most_favorited_response['status']['content'], 'html.parser')
        plain_text = soup.get_text()
        plain_text = '!' + plain_text.split('!', 1)[1].strip()
        
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.findAll('a'):
            link.replace_with(link.get('href'))
        plain_text = str(soup)
        plain_text = plain_text.replace("&amp;", "&")
        plain_text = plain_text.replace("–", "--")
        
        print(f"Most favorited response: {plain_text}")

        if plain_text.startswith('!ctrl'):
            print("CONTROL")
            print(plain_text[6]) # Print the first character after '!ctrl'
            libvirt_test.control_key(plain_text[6])
        elif plain_text.startswith('!enter'):
            print("ENTER")
            libvirt_test.hit_enter()
        elif plain_text.startswith('!cmd'):
            print("COMMAND")
            print(plain_text[5:])
            libvirt_test.run_command(plain_text[5:])
            
        else:
            print(f"Most favorited response: {plain_text}")
            # print(f"Most favorited response: {most_favorited_response['status']['content']}")
    else:
        print("No responses received.")

# Run the bot
while True:
    post_image_and_log_response()
    time.sleep(15 * 60)
    # time.sleep(60)
