from seleniumbase import SB
import time


with SB(uc=True, test=True) as sb:
    url = "https://kick.com/browse"
    sb.uc_open_with_reconnect(url, 5)
    sb.uc_gui_click_captcha()
    sb.sleep(2)
    sb.uc_gui_handle_captcha()
    start_time = time.time()
    duration = 100 * 60
    while time.time() - start_time < duration:
        if sb.is_element_present('button:contains("I am 18+")'):
            sb.uc_click('button:contains("I am 18+")', reconnect_time=4)
        if sb.is_element_present('button:contains("Accept")'):
            sb.uc_click('button:contains("Accept")', reconnect_time=4)
        sb.sleep(5)
