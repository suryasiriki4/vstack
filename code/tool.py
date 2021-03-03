import random

def souper(url):
    """ getting the beautifulSoup object from url """

    try:
        html = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)})
    except requests.exceptions.RequestException:
        print("unable to fetch stack overflow results")
        sys.exit(1)

    print(html.url)

    if re.search("\.com/nocaptcha", html.url): # checking if URL is captcha page
        return None
    else:
        return BeautifulSoup(html.text, "html.parser")

def get_search_results(soup):
    """ return a list of directories of containg serach resluts """
    search_results = []

    for result in soup.find_all("div", class_="question-summary search-result"):
        search_results.append(result)