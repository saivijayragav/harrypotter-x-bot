import tweepy
import time
import json

# Load state from a file
def load_state():
    try:
        with open('state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'i': 0, 'l': 0, 'head': "The Philsopher's Stone CH-1 Lines of 552 lines\n"}  # default starting values

# Save state to a file
def save_state(i, l, head):
    with open('state.json', 'w') as f:
        json.dump({'i': i, 'l': l, 'head': head}, f)

state = load_state()
i = state['i']
l = state['l']
head = state['head']

# Your Twitter credentials
api_key = "[api_key]"
api_secret = "[api_secret]"
bearer_token = r"[bearer_token]"
access_token = "[access_token]"
access_token_secret = "[access_token_secret]"
# Connecting to Twitter API
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

file = open("harrypotter3.txt", 'r', encoding="utf-8")
f = file.readlines()

while i < len(f):
    try:
        message = ""
        if f[i][:5] == "Book:":
            head = f[i][5:]
            l = 1
            i += 1
        else:
            c = 0
            for j in range(3):
                if i + j < len(f) and f[i + j][:5] != "Book:":
                    cond1 = j == 0 and l == 1
                    if cond1 or len(f[i+j]) <= 1:
                        message += f[i + j]
                    elif f[i+j][0] == "“" and f[i+j].strip()[-1] == "”":
                        if j == 0:
                            message += f[i+j]
                        else:
                            message += '\n' + f[i+j]
                    elif f[i+j].strip()[-1] == "”":
                        message += f[i+j]
                    else:
                        message += f[i+j].strip() + ' '
                    c += 1
                else:
                    break

            if c == 1:
                head2 = head.replace("Lines", "Line " + str(l))
            else:
                head2 = head.replace("Lines", "Lines " + str(l) + '-' + str(l + c - 1))

            message = head2 + '\n' + message
            client.create_tweet(text=message)

            if i + j < len(f) and f[i + j][:5] != "Book:":
                i += 1
                l += 1
            i += j
            l += j

            # Save the state after each tweet, including the head
            save_state(i, l, head)

        time.sleep(1800)
    except Exception as e:
        print(f"An error occurred: {e}")
        break
