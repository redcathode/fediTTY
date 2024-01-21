import os
from mastodon import Mastodon
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print(os.getenv("BOT_ACCESS_TOKEN"))

# Initialize Mastodon API client
mastodon = Mastodon(
    access_token=os.getenv("BOT_ACCESS_TOKEN"),
    api_base_url='https://fedi.computernewb.com'
)

def fetch_and_process_responses():
    # Fetch the bot's last post
    user = mastodon.account_verify_credentials()
    statuses = mastodon.account_statuses(user['id'], limit=1)
    if not statuses:
        print("No posts found.")
        return

    last_status = statuses[0]

    # Get the responses to the last post
    notifications = mastodon.notifications()
    responses = [n for n in notifications if n['type'] == 'mention' and n['status']['in_reply_to_id'] == last_status['id'] and not any(keyword in n['status']['content'] for keyword in ['shutdown', 'masscan', 'nmap']) and "!" in n['status']['content']]

    # Process the responses
    for response in responses:
        soup = BeautifulSoup(response['status']['content'], 'html.parser')
        plain_text = soup.get_text()
        plain_text = '!' + plain_text.split('!', 1)[1].strip()
        

        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.findAll('a'):
            link.replace_with(link.get('href'))
        plain_text = str(soup)
        plain_text = plain_text.replace("&amp;", "&")
        plain_text = plain_text.replace("–", "--")

        print(f"Processed response: {plain_text}")

# Run the function
if __name__ == "__main__":
    fetch_and_process_responses()