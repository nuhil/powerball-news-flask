from powerball import PowerballScraper
from writer import WriteArticle
from flask import abort
import logging


def health():
    return {'message': 'API server is running fine!'}, 200


def get(use_ai=True):
    """
    Get the latest Powerball lottery information and write an article using it.

    :param use_ai: A boolean indicating whether to use artificial intelligence
    to generate the article (default True)
    :return: The content of the written article
    """

    try:
        scraper = PowerballScraper()
        numbers = scraper.scrape_winning_numbers()
        winners = scraper.scrape_winners()
        jackpot = scraper.scrape_next_drawing_jackpot()
        dates = scraper.scrape_dates()
        data = {
            'winning_numbers': numbers,
            'winners': winners,
            'estimated_jackpot': jackpot,
            'drawing_dates': dates
        }
    except Exception as e:
        # Log the error and return a 404 error response
        logging.error(f'Error: Exception occurred while parsing Powerball website: {e}')  # noqa E501
        abort(404, "No article was created/found!")

    else:
        # Write an article using the retrieved data
        article = WriteArticle(data)
        article_content = article.write(use_ai)

        return article_content
