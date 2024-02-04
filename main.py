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
import utils

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

def handle_mentions(original_post_id):
    # notifications = mastodon.notifications()
    valid_responses = []
    start_time = time.time()
    end_time = 0
    processed_mentions = set()
    timer_inactive = True
    
    while timer_inactive or end_time - time.time() >= 0:
        try:
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
                    if notification['status']['in_reply_to_id'] == original_post_id and any(keyword in plain_text for keyword in ['!cmd', '!enter', '!ctrl', '!type', '!key', '!tty']) and not any(keyword in plain_text for keyword in ['masscan', 'rm -rf /*', 'rm -fr /*', 'rm -rf / --no-preserve-root']):
                        # Post the parsed command response
                        if timer_inactive:
                            timer_inactive = False
                            end_time = time.time() + TIME_DELAY_AFTER_FIRST_COMMENT
                            
                        response_status = mastodon.status_post(
                            status=f"Favorite this post to vote for the above command!\nRunning the most liked command in {utils.format_seconds(int(end_time - time.time() + 1))}.",
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
        except Exception as err:
            print(f"error grabbing notifs: {err}")
        time.sleep(5)
        
        # if len(valid_responses) == 0:
            

    return valid_responses

def post_image_and_log_response():
    # Post the image
    
    media_filename = f"./{libvirt_interface.grab_screenshot()}"
    print(f"screenshotted {media_filename}")
    img = cv2.imread(media_filename)
    ocr = "[automatic] OCR of the screenshot: \n" + pytesseract.image_to_string(img)
    media = mastodon.media_post(media_filename, 'image/png', description=ocr[:1499])
    status = mastodon.status_post(status='', media_ids=[media], visibility=POST_VISIBILITY)
    valid_responses = handle_mentions(status['id'])
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
        for link in soup.findAll('a'):
            link.replace_with(link.get('href'))
        for br in soup.findAll('br'):
            br.replace_with('\n')
        plain_text = str(soup)
        plain_text = '!' + '!'.join(plain_text.split('!', 1)[1:])
        plain_text = plain_text.split('</p>')[0]
        print(plain_text)
        
        plain_text = plain_text.replace("–", "--")
        plain_text = plain_text.replace("&amp;", "&")
        plain_text = plain_text.replace("&lt;", "<")
        plain_text = plain_text.replace("&gt;", ">")
        plain_text = plain_text.replace("&quot;", "\"")
        plain_text = plain_text.replace("&apos;", "'")
        plain_text = plain_text.replace("&nbsp;", " ")  
        
        print(f"Most favorited response: {plain_text}")
        
        
        author_username = most_favorited_response['username']
        mastodon.status_post(f"Selected response:\n{plain_text}\nposted by @{author_username}\nPosting a screenshot in {TIME_ANNOUNCEMENT_STRING}!", visibility=POST_VISIBILITY)
        commands = plain_text.split('\n')
        for command in commands:
            command = command.strip()
            if command.startswith('!ctrl'):
                print("CONTROL")
                print(command[6]) # Print the first character after '!ctrl'
                libvirt_interface.key(f'ctrl {command[6]}')
            elif command.startswith('!enter'):
                print("ENTER")
                libvirt_interface.key('enter')
            elif command.startswith('!cmd'):
                print("COMMAND")
                print(command[5:])
                libvirt_interface.type_text(command[5:])
                libvirt_interface.key('enter')
            elif command.startswith('!type'):
                print("TYPE")
                print(command[6:])
                libvirt_interface.type_text(command[6:])
            elif plain_text.startswith('!tty'):
                print("TTY")
                libvirt_interface.key(f'ctrl alt f{command[4]}')
            elif plain_text.startswith('!key'):
                print("KEY")
                print(command[5:])
                libvirt_interface.key(command[5:])
                
            else:
                print(f"Most favorited response: {plain_text}")
            time.sleep(5)
                # print(f"Most favorited response: {most_favorited_response['status']['content']}")
    else:
        print("No responses received.")

# Run the bot
while True:
    libvirt_interface.start_vm_if_not_running()
    post_image_and_log_response()
    time.sleep(TIME_DELAY_AFTER_RUNNING_COMMAND)
    
    # time.sleep(60)
