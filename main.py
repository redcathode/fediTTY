import random
import time
import os
from mastodon import Mastodon
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import libvirt_interface
import cv2
import pytesseract
from constants import *

load_dotenv()

mastodon = Mastodon(
    access_token=os.getenv("BOT_ACCESS_TOKEN"),
    api_base_url=INSTANCE_URL
)

# def parse_command(content):
#     # Extract the plain text from the HTML content
#     soup = BeautifulSoup(content, 'html.parser')
#     plain_text = soup.get_text()
    
#     # Replace HTML entities with their corresponding characters
#     plain_text = plain_text.replace("&amp;", "&")
#     plain_text = plain_text.replace("–", "--")
    
#     # Check if the plain text starts with '!' and does not contain forbidden keywords
#     if any(keyword in plain_text for keyword in ['!cmd', '!enter', '!ctrl', '!type']) and not any(keyword in plain_text for keyword in ['shutdown', 'masscan', 'nmap']):
#         command = plain_text.split('!', 1)[1].strip()
#         return command
#     else:
#         return None

def handle_mentions(original_post_id, timer=6300):
    # notifications = mastodon.notifications()
    valid_responses = []
    start_time = time.time()
    processed_mentions = set()
    
    while time.time() - start_time < timer:
        notifications = mastodon.notifications()
        for notification in notifications:
            if notification['type'] == 'mention':
                mention_id = notification['status']['id']
                if mention_id in processed_mentions:
                    continue  # Skip this mention if it has already been processed
                content = notification['status']['content']
                plain_text = content
                soup = BeautifulSoup(content, 'html.parser')
                plain_text = soup.get_text()
                # really basic keyword filter that blocks people from just rm -rf'ing the whole disk or portscanning
                # this is very, very, very easy to get around
                # we're basically assuming that people won't try very hard to do anything bad
                # if that's something you're considering... please don't waste your time wasting mine.
                if notification['status']['in_reply_to_id'] == original_post_id and any(keyword in plain_text for keyword in ['!cmd', '!enter', '!ctrl', '!type']) and not any(keyword in plain_text for keyword in ['masscan', 'rm -rf /*', 'rm -fr /*', 'rm -rf / --no-preserve-root']):
                    # Post the parsed command response
                    response_status = mastodon.status_post(
                        status=f"Favorite this post to vote for the above command!",
                        in_reply_to_id=notification['status']['id'],
                        visibility=POST_VISIBILITY
                    )
                    # Store the response details
                    valid_responses.append({
                        'response_id': response_status['id'],
                        'original_comment_id': notification['status']['id'], 
                        'username': notification['account']['username'],
                        'favorites_count': 0
                    })
                    processed_mentions.add(mention_id)  
        time.sleep(5)

    return valid_responses

def post_image_and_log_response():
    # Post the image
    media_filename = f"./{libvirt_interface.grab_screenshot()}"
    print(f"screenshotted {media_filename}")
    img = cv2.imread(media_filename)
    ocr = "[automatic] OCR of the screenshot: \n" + pytesseract.image_to_string(img)
    media = mastodon.media_post(media_filename, 'image/png', description=ocr[:1499])
    status = mastodon.status_post(status='', media_ids=[media], visibility=POST_VISIBILITY)
    

    # Wait for an hour
    # time.sleep((2 * 3600) - (15 * 60))
    valid_responses = handle_mentions(status['id'], 30)
    # valid_responses = handle_mentions(status['id'], 20)
    # time.sleep(60 * 5)
    for response in valid_responses:
        response_status = mastodon.status(response['response_id'])
        response['favourites_count'] = response_status['favourites_count']
        print(f"re-fetched favorite count: {response['favourites_count']}")

    # Get the responses
    # notifications = mastodon.notifications()

    # Filter responses to only mentions that are replies to our status
    # responses = [n for n in notifications if n['type'] == 'mention' and n['status']['in_reply_to_id'] == status['id'] and any(keyword in n['status']['content'] for keyword in ['!ctrl', '!enter', '!cmd', '!type']) and not any(keyword in n['status']['content'] for keyword in ['shutdown', 'masscan', 'nmap'])]
    # FIXME: we should really check if the response starts with '!' after all the mentions
    # this might break in weird ways later
    
    # Find the most favorited response
    if valid_responses:
        max_faves = max(response['favourites_count'] for response in valid_responses)
        top_responses = [response for response in valid_responses if response['favourites_count'] == max_faves]
        print(f'top responses: {top_responses}')
        most_favorited_response = random.choice(top_responses)
        
        original_comment_id = most_favorited_response['original_comment_id']
        original_comment = mastodon.status(original_comment_id)
        
        print(f"selected original comment content: {original_comment['content']}")
        
       # Extract the plain text from the HTML content
        soup = BeautifulSoup(original_comment['content'], 'html.parser')
        plain_text = soup.get_text()
        plain_text = '!' + plain_text.split('!', 1)[1].strip()
        
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.findAll('a'):
            link.replace_with(link.get('href'))
        plain_text = str(soup)
        plain_text = plain_text.replace("&amp;", "&")
        plain_text = plain_text.replace("–", "--")
        
        print(f"Most favorited response: {plain_text}")
        
        author_username = most_favorited_response['username']
        mastodon.status_post(f"Selected response:\n{plain_text}\nposted by @{author_username}\nPosting a screenshot in {TIME_ANNOUNCEMENT_STRING}!", visibility=POST_VISIBILITY)

        if plain_text.startswith('!ctrl'):
            print("CONTROL")
            print(plain_text[6]) # Print the first character after '!ctrl'
            libvirt_interface.control_key(plain_text[6])
        elif plain_text.startswith('!enter'):
            print("ENTER")
            libvirt_interface.hit_enter()
        elif plain_text.startswith('!cmd'):
            print("COMMAND")
            print(plain_text[5:])
            libvirt_interface.run_command(plain_text[5:])
        elif plain_text.startswith('!type'):
            print("TYPE")
            print(plain_text[6:])
            libvirt_interface.type_text(plain_text[6:])
            
        else:
            print(f"Most favorited response: {plain_text}")
            # print(f"Most favorited response: {most_favorited_response['status']['content']}")
    else:
        print("No responses received.")

# Run the bot
while True:
    post_image_and_log_response()
    time.sleep(5)
    # time.sleep(60)
