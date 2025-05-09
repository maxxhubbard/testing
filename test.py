from seleniumbase import SB
import time
import requests
import sys
import requests
import os


import os
import requests

def testtw():
    # Retrieve environment variables
    channel = os.getenv("CHANNEL")
    authorization = os.getenv("AUTHORIZATION")
    client_id = os.getenv("TCLIENTID")

    if not channel or not authorization or not client_id:
        print("Missing required environment variables: CHANNEL, AUTHORIZATION, or TCLIENTID.")
        return False

    # Set up the API request
    url = f"https://api.twitch.tv/helix/streams?user_login={channel}"
    headers = {
        "Authorization": f"Bearer {authorization}",
        "Client-Id": client_id
    }

    try:
        # Send the GET request to the Twitch API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response contains "live"
        if "live" in response.text:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False


def testkick():
    token_url = "https://id.kick.com/oauth/token"
    client_id = os.getenv("CLIENTID")  # Replace with your client ID
    client_secret = os.getenv("CLIENTSECRET")  # Replace with your client secret
    body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        token_response = requests.post(token_url, data=body)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
        print(f"Access Token: {access_token}")
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving token: {client_id} {client_secret} {e}")
        return False

    channel_slug = os.getenv("CHANNEL")  # Replace this with the channel's slug
    url = f"https://api.kick.com/public/v1/channels?slug={channel_slug}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", [])
        for channel in data:
            slug = channel.get("slug")
            is_live = channel.get("stream", {}).get("is_live")
            if is_live is True:
                return True
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving channel data: {e}")
        return False

    return False


with SB(uc=True, test=True) as sb:
    if testkick():
        channel = os.getenv("CHANNEL")
        url = f'https://kick.com/{channel}'
        sb.uc_open_with_reconnect(url, 5)
        sb.uc_gui_click_captcha()
        sb.sleep(2)
        sb.uc_gui_handle_captcha()
        start_time = time.time()
        duration = 120 * 60
        while time.time() - start_time < duration:
            if sb.is_element_present('button:contains("I am 18+")'):
                sb.uc_click('button:contains("I am 18+")', reconnect_time=4)
            if sb.is_element_present('button:contains("Accept")'):
                sb.uc_click('button:contains("Accept")', reconnect_time=4)
            if testkick():
                sb.sleep(120)
            else:
                break
    if testtw():
        channel = os.getenv("CHANNEL")
        url = f'https://www.twitch.tv/{channel}'
        sb.uc_open_with_reconnect(url, 5)
        sb.uc_gui_click_captcha()
        sb.sleep(2)
        sb.uc_gui_handle_captcha()
        start_time = time.time()
        duration = 120 * 60
        while time.time() - start_time < duration:
            if sb.is_element_present('button:contains("Start Watching")'):
                sb.uc_click('button:contains("Start Watching")', reconnect_time=4)
            if sb.is_element_present('button:contains("Accept")'):
                sb.uc_click('button:contains("Accept")', reconnect_time=4)
            if testtw():
                sb.sleep(120)
            else:
                break
    if not testtw() and not testkick():
        channel = os.getenv("CHANNEL")
        url = f'https://www.youtube.com/@{channel}/videos'
        sb.uc_open_with_reconnect(url, reconnect_time=4)
        sb.sleep(2)
        if sb.is_element_present('button:contains("Accept")'):
            sb.uc_click('button:contains("Accept")', reconnect_time=4)
        sb.uc_click("ytd-thumbnail", 4.1)
        sb.uc_click("div#contents.style-scope.ytd-rich-grid-renderer ytd-rich-grid-media ytd-thumbnail", 4.1)
        sb.sleep(2)
        sb.uc_click("div#contents.style-scope.ytd-rich-grid-renderer", 4.1)
        sb.sleep(2)
        sb.save_screenshot("ssasa.png", folder='./latest_logs')
        sb.sleep(5)
        sb.uc_click("div#contents ytd-rich-item-renderer", 4.1)
        sb.sleep(8)
            
