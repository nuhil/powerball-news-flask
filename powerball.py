from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class PowerballScraper:
    """
    A class to scrape Powerball lottery results and information from
    the official Powerball website.

    Attributes:
    -----------
    url : str
        The URL of the Powerball website.
        Defaults to "https://www.powerball.com/".
    chrome_options : webdriver.ChromeOptions
        Chrome options used by the Selenium webdriver.
    service : selenium.webdriver.chrome.service.Service
        Chrome service used by the Selenium webdriver.
    driver : selenium.webdriver.chrome.webdriver.WebDriver
        The Selenium webdriver instance used to interact with the website.
    soup : bs4.BeautifulSoup
        The BeautifulSoup instance used to parse the HTML
        source code of the website.

    Methods:
    --------
    scrape_winning_numbers(self) -> str:
        Returns the winning numbers for the latest Powerball draw as a string.
    scrape_dates(self) -> Tuple[str, str]:
        Returns a tuple containing the date of the last Powerball draw and
        the date of the next Powerball draw.
    scrape_winners(self) -> Dict[str, Dict[str, str]]:
        Returns a dictionary containing information about the winners of
        the latest Powerball draw.
    scrape_next_drawing_jackpot(self) -> str:
        Returns the estimated jackpot for the next Powerball draw as a string.
    """

    def __init__(self, url="https://www.powerball.com/"):
        """
        Initializes a new PowerballScraper instance.

        Parameters:
        -----------
        url : str, optional
            The URL of the Powerball website.
            Defaults to "https://www.powerball.com/".
        """

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--headless')
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service,
                                       options=self.chrome_options
                                       )

        self.driver.get(url)
        source = self.driver.page_source
        self.soup = BeautifulSoup(source, "html.parser")
        self.driver.quit()

    def scrape_winning_numbers(self) -> str:
        """
        Returns the winning numbers for the latest Powerball draw as a string.

        Returns:
        --------
        str
            Winning numbers for the latest Powerball draw, separated by spaces.
        """

        complete_card = self.soup.find("div", id="numbers")
        numbers = complete_card.find_all('div', {'class': 'item-powerball'})
        numbers = ' '.join([item.text.strip() for item in numbers])

        return numbers

    def scrape_dates(self) -> dict:
        """
        Returns a tuple containing the date of the last Powerball draw and
        the date of the next Powerball draw.

        Returns:
        --------
        dict[str, str]
            A dictionary containing the date of the last Powerball draw and
            the date of the next Powerball draw.
        """

        last_draw_date = self.soup.find("div", id="numbers")\
                                  .find('h5', class_='title-date').text
        next_draw_date = self.soup.find("div", id="next-drawing")\
                                  .find('h5', class_='title-date').text

        return {
                'last_draw_date': last_draw_date,
                'next_draw_date': next_draw_date
                }

    def scrape_winners(self) -> dict:
        """
        Scrapes the winners of each game from the Powerball website.

        Returns:
        --------
        winners_dict: dict
            A dictionary containing the winners of each game, with the game name
            as the key, and the winner type and location as values.
        """

        winners_card = self.soup.find("div", id="winners")
        winners = winners_card.find_all('div', class_='winners-group')
        winners_dict = {}

        for winner in winners:
            game_name = winner.find('span', class_='game-name').text.strip()
            winner_type = winner.find('span', class_='winner-type').text.strip()
            winner_location = winner.find('span', class_='winner-location').text.strip()  # noqa E501
            winners_dict[game_name] = {'winner_type': winner_type, 'winner_location': winner_location}  # noqa E501

        return winners_dict

    def scrape_next_drawing_jackpot(self) -> str:
        """Scrape the next Powerball drawing jackpot amount from the website.

        Returns:
            str: The jackpot amount as a string.
        """

        next_drawing_card = self.soup.find("div", id="next-drawing")
        jackpot_amount = next_drawing_card.find('span', class_="game-jackpot-number").text  # noqa E501

        return jackpot_amount
