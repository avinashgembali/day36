import requests
import math
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ACCOUNT_SID = "YOU ACC SID"
AUTH_TOKEN = "YOUR AUTHENTICATION TOKEN"

parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "TOUR API KEY"
}
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": "YOUR NEWS KEY",
}
stock_response = requests.get(url=STOCK_ENDPOINT, params=parameter)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
yesterday_data = float(data["2024-08-28"]["4. close"])
day_before_yesterday_data = float(data["2024-08-27"]["4. close"])
diff = abs(yesterday_data - day_before_yesterday_data)
percent = (diff / yesterday_data) * 100
# i have taken 1 here because my diff is 1.6 something around so to keep message to be sent i had kept it 1
if percent > 1:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    sliced_data = news_data[0:3]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in sliced_data:
        title = article["title"]
        brief = article["description"]
        message = client.messages.create(
            body=f"Headline:{title}. \nBrief: {brief}.",
            from_="TWILLIO PROVIDED NUMBER",
            to="YOUR NUMBER",
        )
        print(message.body)

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

