#!/usr/bin/env python3

"""OK.RU scraping tool.

Created By  : justzip
Created Date: 14/12/23
Version     : 1.0.0 (14/12/23)
"""

import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BANNER = r"""
  <=======]}======
    --.   /|
   _\"/_.'/
 .'._._,.'
 :/ \{}/
(L  /--',----._
    |          \\
   : /-\ .'-'\ / |
    \\, ||    \|
     \/ ||    ||
   ___  _  __  ___ _   _
  / _ \| |/ / | _ \ | | |
 | (_) | ' < _|   / |_| |
  \___/|_|\_(_)_|_\\___/
"""

def show_banner() -> None:
    """Print the banner."""
    print(BANNER)

def login_ok_ru(driver, username, password):
    """Connect to OK.ru with provided credentials."""
    driver.get("https://ok.ru/")
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'field_email'))
        )
        email_input.send_keys(username)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'field_password'))
        )
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))
        )
        login_button.click()

        time.sleep(5)
    except Exception as e:
        print(f"Error during login: {e}")
        exit(1)kq

def scroll_to_bottom(driver: webdriver) -> None:
    """Fait défiler le navigateur jusqu'en bas de la page, en cliquant sur le bouton 'show more' si nécessaire."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Faites défiler jusqu'en bas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Attendez quelques secondes pour le chargement des nouveaux éléments

        # Essayez de cliquer sur le bouton 'show more'
        try:
            show_more_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'your_show_more_button_selector'))
            )
            show_more_button.click()
            time.sleep(3)  # Attendez que de nouveaux éléments se chargent après le clic
        except Exception as e:
            print("Aucun bouton 'show more' trouvé ou une erreur est survenue:", e)
            break  # Sortez de la boucle si aucun bouton n'est trouvé ou en cas d'erreur

        # Vérifiez si la hauteur de la page a changé
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scrape_group_members(driver, group_url):
    """Scrape members of a given group."""
    driver.get(group_url)
    scroll_to_bottom(driver)
    members = driver.find_elements(By.CSS_SELECTOR, 'a.bold.n-t')
    group_id_or_name = group_url.rstrip('/').split('/')[-2]

    output_filename = f"{group_id_or_name}_group_members.txt"
    with open(output_filename, 'w', encoding='utf-8') as file:
        for member in members:
            href = member.get_attribute('href')
            member_id = href.split('/')[-1].split('?')[0]
            member_name = member.text
            file.write(f"Member ID: {member_id}, Member Name: {member_name}\n")

def scrape_friends(driver, friends_url):
    """Scrape friends from the given URL."""
    driver.get(friends_url)
    scroll_to_bottom(driver)
    friends = driver.find_elements(By.CSS_SELECTOR, 'a.o[data-l="t,e2"]')
    user_id = friends_url.split('/')[-2]

    output_filename = f"{user_id}_friends.txt"
    with open(output_filename, 'w', encoding='utf-8') as file:
        for friend in friends:
            friend_id = friend.get_attribute('href').split('/')[-1].split('?')[0]
            friend_name = friend.text
            file.write(f"Friend ID: {friend_id}, Friend Name: {friend_name}\n")

def scrape_member_groups(driver, groups_url):
    """Scrape groups that a member belongs to."""
    driver.get(groups_url)
    scroll_to_bottom(driver)
    groups = driver.find_elements(By.CSS_SELECTOR, 'a.group-detailed-card_name.__small[data-l="t,visit"]')
    user_id = groups_url.split('/')[-2]

    output_filename = f"{user_id}_groups.txt"
    with open(output_filename, 'w', encoding='utf-8') as file:
        for group in groups:
            group_id = group.get_attribute('href').split('/')[-1]
            group_name = group.get_attribute('title')
            file.write(f"Group ID: {group_id}, Group Name: {group_name}\n")

def main(args):
    driver = webdriver.Chrome()
    login_ok_ru(driver, args.number, args.password)

    main_window_handle = driver.current_window_handle

    if args.group_url:
        scrape_group_members(driver, args.group_url)

    if args.friends_url:
        scrape_friends(driver, args.friends_url)

    if args.member_groups_url:
        scrape_member_groups(driver, args.member_groups_url)

    driver.quit()
if __name__ == "__main__":
    show_banner()
    parser = argparse.ArgumentParser(description="OK.RU Scraping Tool.")
    parser.add_argument("-n", "--number", required=True, help="Phone number for login")
    parser.add_argument("-p", "--password", required=True, help="Password for login")
    parser.add_argument("-g", "--group_url", help="URL of the group to scrape members from")
    parser.add_argument("-f", "--friends_url", help="URL of the user's friends page to scrape")
    parser.add_argument("-m", "--member_groups_url", help="URL of the member's groups page to scrape")
    args = parser.parse_args()
    main(args)
