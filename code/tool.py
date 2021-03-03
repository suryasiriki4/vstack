import random


import sumy


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



def print_results(QUSTION_IDS, QUESTIONS, ANSWERS):

    num_of_results = len(QUSTION_IDS)



    
    for i in range(num_of_results):
        answer = ANSWERS[i].body
        parser = PlaintextParser.from_string(answer,Tokenizer("english"))
    
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document,10);
        


        print(' ')
        print("#####################################################################################################")
        print(' ')
        print('Question: ')
        print(' ')
        print(QUESTIONS[i].body)
        print(' ')
        print("-----------------------------------------------------------------------------------------------------")
        print(' ')
        print("Author: " + ANSWERS[i].author)
        print(' ')
        print(' ')
        print("Answer: ")
        for sentence in summary :
            print(sentence)
        
    return
