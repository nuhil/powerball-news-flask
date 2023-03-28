import os
import re
import openai
from flask import abort
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")


class WriteArticle:
    """
    A class that generates news articles based on Powerball lottery data
    using OpenAI's GPT-3 API.

    ...

    Attributes
    ----------
    data : dict
        A dictionary containing the Powerball lottery data including the
        drawing dates, winning numbers, winners' information,
        and the estimated jackpot.

    Methods
    -------
    write(use_ai=True):
        Generates a news article based on the Powerball lottery data.

        Parameters:
            use_ai (bool): A flag to indicate whether to use OpenAI's GPT-3 API
            to dynamically generate the news article.

        Returns:
            dict: A dictionary containing the headline and the body of the
            generated news article.
    """

    def __init__(self, data) -> None:
        """
        Constructs all the necessary attributes for the WriteArticle object.

        Parameters:
            data (dict): A dictionary containing the Powerball lottery data
            including the drawing dates, winning numbers, winners' information,
            and the estimated jackpot.
        """

        self.data = data

    def write(self, use_ai=True) -> dict:
        """
        Generates a news article based on the Powerball lottery data.

        Parameters:
            use_ai (bool): A flag to indicate whether to use OpenAI's GPT-3 API
            to dynamically generate the news article.

        Returns:
            dict: A dictionary containing the headline and the body of
            the generated news article.
        """

        if use_ai:
            # Dynamically generate a news article using OpenAI and lottery data
            try:
                response = openai.Completion.create(model="text-davinci-003",
                                                    prompt=f"""I want you to act as a News Article Writer about Powerball lottery for a national news outlet.
                                                    Write an engaging article within 300 words based on the information given below from the latest drawing of the Powerball:

                                                    Last Draw Date: {self.data['drawing_dates']['last_draw_date']}
                                                    Winning Numbers: {self.data['winning_numbers']}
                                                    Jackpot Winner: {'No One' if self.data['winners']['Powerball']['winner_location'] == 'None' else 'From the State '+self.data['winners']['Powerball']['winner_location']}
                                                    Next Draw Date: {self.data['drawing_dates']['next_draw_date']}
                                                    Estimated Jackpot: {self.data['estimated_jackpot']}

                                                    The headline's title should indicate if there was a Powerball winner at the last drawing.
                                                    The article body should indicate if there was a winning number at the last drawing.
                                                    If there was a winner at the last drawing, the article body should include which state the winner was from.
                                                    The article body should indicate when the next drawing will be.
                                                    The article body should indicate how much the potential prize for the next drawing would be.""",
                                                    temperature=0.5,
                                                    max_tokens=300,
                                                    top_p=1.0,
                                                    frequency_penalty=0.0,
                                                    presence_penalty=0.0)
            except Exception as e:
                logging.error(f'Error: Exception occurred while interacting with OpenAI API: {e}')
                abort(404, "No article was created/found!")
            else:
                ai_response = response['choices'][0]['text']
                headline_pattern = r"^Headline: (.+)\n\n"
                headline = re.search(headline_pattern, ai_response, re.MULTILINE)
                body = re.sub(headline_pattern, '', ai_response, flags=re.MULTILINE)

                return {
                    'headline': headline.group(1),
                    'body': body
                }
        else:
            # Static article template that gets filled with lottery data
            template = (f"""No one won the Powerball jackpot at the last drawing on {self.data['drawing_dates']['last_draw_date']}."""
                        f"""The winning numbers for the draw were {self.data['winning_numbers']}, """
                        f"""but no one was able to match them all correctly. \n\n"""
                        f"""The next Powerball drawing will be on {self.data['drawing_dates']['next_draw_date']}, """
                        f"""and the estimated jackpot is {self.data['estimated_jackpot']}."""
                        f"""Players have a chance to win big if they can correctly match all five numbers plus the Powerball number.""")
            return {
                "headline": "No One Wins Powerball Jackpot at Last Drawing",
                "body": template
            }
