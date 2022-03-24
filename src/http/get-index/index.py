# example lambda function
from random import randint
import requests

from shared import settings

logger = settings.logger


def flip_dogecoin():
    heads_up = randint(0, 1)
    return heads_up


def handler(event, context):
    logger.debug(event)
    logger.debug(context)
    heads_up = flip_dogecoin()
    coin_position = 'facing up' if heads_up else 'facing down'
    coin_flip_message = f"Today's Dogecoin landed {coin_position}!"

    # Setup what coin we are trying to find and the currency we want to use
    coin = 'dogecoin'
    vs_currency = 'usd'

    # go and get the data about the coin an API
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={vs_currency}'
    response = requests.get(url)

    logger.debug(f'{response.json()}')
    json_response = response.json()
    current_price = json_response[coin][vs_currency]
    current_price_message = f'The current price of a {coin.title()} is: ${current_price:.7f} {vs_currency.upper()}'
    prediction_message = f'I predict the price of {coin.title()} to {"rise" if heads_up else "fall"}!'

    tweet_message = f'{coin_flip_message} \n' \
                    f'{current_price_message} \n' \
                    f'{prediction_message}'
    # TODO tweet it out
    # tweet_it.send_message(tweet_message)

    response_body = {
        'message': tweet_message,
        'heads_up': bool(heads_up),
        'current_price': f'{current_price:.7f}',
        'coin': coin,
        'currency': vs_currency
    }
    return {'body': response_body}
