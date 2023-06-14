import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Tool_Pack import tools

def scrape_subs():
    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    subreddit_url = 'https://www.reddit.com/r/python/'  # URL of the subreddit you want to crawl
    driver.get(subreddit_url)

    # Scroll down to load more submissions (customize the range as needed)
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Add a delay to allow the page to load more submissions



        # "author"
        # "author_fullname"
        # "id"
        # "permalink"
        # "retrieved_utc"
        # "score"
        # "selftext"
        # "subreddit"
        # "title"
        # "url"
        # "utc_datetime_str"

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    # scrape_subs()
    a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\New_Submissions\20_btc_submissions")
    b = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\New_Submissions\20_btc2_submissions")
    print()
