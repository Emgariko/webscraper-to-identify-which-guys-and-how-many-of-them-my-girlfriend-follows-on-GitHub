import requests
from bs4 import BeautifulSoup
import time
import os
from anthropic import Anthropic

def get_secret_key():
    config_path = os.path.expanduser("~/.config/anthropic.token")
    try:
        with open(config_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Sadge can't get the key monkaW: {e}")
        return None

def stalk_github_following(username):
    url = f'https://github.com/{username}?tab=following'
    # pretending to be normie browser kekw
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        following = soup.find_all('span', class_='Link--secondary')
        names = [follower.text.strip() for follower in following]

        prompt = f"""analyze these GitHub usernames and identify which ones appear masculine. Return only the usernames along with an explanation of why they are considered masculine, one per line.: {', '.join(names)}"""

        # time to summon Claude monkaS
        api_key = get_secret_key()
        if not api_key:
            return "Sadge no API key found to summon Claude monkaW"

        claude = Anthropic(api_key=api_key)
        response = claude.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        masculine_names = response.content[0].text.strip().split('\n')
        masculine_names = [name.strip() for name in masculine_names if name.strip()]

        return {
            'total_following': len(following),
            'masculine_names': masculine_names,
            'total_masculine': len(masculine_names),
            'percentage': (len(masculine_names) / len(following) * 100) if following else 0
        }
    except requests.RequestException as e:
        return f"monkaW GitHub caught us in 4k: {e}"
    except Exception as e:
        return f"WeirdChamp something broke: {e}"

if __name__ == "__main__":
    username = input("Tell me your girlfriend's GitHub username: ")
    print("\ntime for some content kekw")
    time.sleep(1)

    results = stalk_github_following(username)
    if isinstance(results, dict):
        print(f"\nHere's what we found about {username}:")
        print(f"Total following count (real): {results['total_following']}")
        print(f"Masculine usernames detected monkaHmm: {results['total_masculine']}")

        if results['total_masculine'] > 0:
            # print("\nmonkaW moment... here are the masculine usernames:")
            for name in results['masculine_names']:
                print(f"- {name}")
            print(f"\nPercentage of masculine usernames monkaS: {results['percentage']:.1f}%")
        else:
            print("\nkekw they're only following the gals... still kinda sus tho")

        print("\n⚠️ Disclaimer: im not toxic copium")
    else:
        print(f"Investigation failed Sadge: {results}")

