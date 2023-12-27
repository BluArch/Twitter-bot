import tweepy
import openai
from keys import api_key, api_key_secret, bearer_token, access_token,access_token_secret, openai_key

def main():
    client = create_client()
    tweet_text = chatbot()
    tweet(client, tweet_text)

def create_client():
    client = tweepy.Client(
        consumer_key = api_key,
        consumer_secret = api_key_secret,
        bearer_token = bearer_token,
        access_token = access_token,
        access_token_secret = access_token_secret
    )

    return client

def tweet(clientID: tweepy.Client, tweet_text: str):
    try:
        clientID.create_tweet(text=tweet_text)
        print('Tweeted successfully!')
    except tweepy.TweepyException as e:
        print("Tweet was too long, not posting")


def chatbot():
    #TODO: make it so the role and prompt are not hard-coded
    openai.api_key = openai_key
    conversation_history:  list = start_convo()

    update_chat = chat(conversation_history)
    newest_response: str = get_newest_response(update_chat)

    return newest_response


def start_convo() -> list:
    # Returns the beginning of a conversation with ChatGPT. Beginning content is hardcoded for now
    conversation: list = [{"role": "system", "content": "You are Market Mogul Mark, the epitome of a high-energy, goofy stock bro living in the fast-paced world of finance in New York City. With perfectly coiffed hair and an ever-present enthusiasm for marketing and market trends, Chad navigates the concrete jungle with the confidence of someone who's always one step ahead in the game."}]
    conversation.append({"role": "user", "content": "You are a New York City, high social status living stock bro. Create a tweet about marketing using an over-the-top style of language and include words that you think would be used amongst brothers of a fraternity. Do not provide pre-context such as \"Certainly, here's the tweet: \". Do not have the tweet longer than 2 sentences and do not contain quotations around the message"})

    return conversation


def chat(conversation_history: list) -> list:
    #Takes a list of the current chat history, returns list with the newest response included
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
    reply = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": reply})
    return conversation_history


def get_newest_response(conversation_history: list) -> str:
    #Takes a list of current chat history, returns the newest response as a string
    newest_dictionary: dict = conversation_history[-1]
    newest_response: str = newest_dictionary["content"]
    return newest_response

if __name__ == '__main__':
    main()