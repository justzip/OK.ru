# OK.RU Scraping Tool

This tool is designed for scraping various types of information from OK.RU, including group members, friends lists, and member group affiliations. It utilizes Selenium for web scraping and requires valid OK.RU credentials for login.

## Features

- Scrape group members from a specified group URL.
- Scrape friends from a user's friends page.
- Scrape groups that a member belongs to.

## Prerequisites

- Python 3
- Selenium WebDriver
- ChromeDriver (or any driver compatible with your browser)

## Installation

1. Installez les dépendances :

   ```bash
   pip install selenium

## Usage

Run the script from the command line, providing the necessary arguments:

python ok_ru_scraping_tool.py -n YOUR_PHONE_NUMBER -p YOUR_PASSWORD [-g GROUP_URL] [-f FRIENDS_URL] [-m MEMBER_GROUPS_URL]

markdown
Copy code

### Arguments

- `-n`, `--number`: Phone number for login.
- `-p`, `--password`: Password for login.
- `-g`, `--group_url`: URL of the group to scrape members from (optional).
- `-f`, `--friends_url`: URL of the user's friends page to scrape (optional).
- `-m`, `--member_groups_url`: URL of the member's groups page to scrape (optional).

## Disclaimer

This tool is for educational purposes only. Please use responsibly and in accordance with OK.RU's terms of service.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with your suggestions.

## License

[Your preferred license]

## Author

justzip - [your contact information or website]
