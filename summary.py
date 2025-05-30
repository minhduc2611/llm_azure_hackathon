from my_open_ai import load_open_ai
from bs4 import BeautifulSoup
import requests
import logging
system_prompt = """
You are a helpful assistant that summarizes text.
"""

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
class Website:
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
    please provide summary:\n\n"
    user_prompt += website.text
    return user_prompt      
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]
    
    
def gen_summary(url):
    try:
        beautiful_print(f"Generating summary for {url}")
        theUrl = f"https://en.wikipedia.org/wiki/{url.replace(' ', '_')}"
        beautiful_print(f"The URL is {theUrl}")
        website = Website(theUrl)
        beautiful_print(f"Contents is fetched")
        instance = load_open_ai()
        beautiful_print(f"Generating summary...")
        response = instance.chat.completions.create(
            model = "gpt-4o-mini",
            messages= messages_for(website)
        )
        beautiful_print(f"Summary generated")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return f"Error generating summary: {e}"

def beautiful_print(text):
    logging.info(text)