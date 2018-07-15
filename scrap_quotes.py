
from bs4 import BeautifulSoup
import requests
from csv import DictWriter
from random import choice
url = 'http://quotes.toscrape.com'

def get_page(page):
    response = requests.get(url+ page)
#print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def load_quotes():
    page = ''
    #soup = get_page(page)
    #nxt = soup.find(class_= "next") #[0].find('a')['href']
    #nn = nxt#.find('a')['href']
    #if nxt:
    #    print(nn.find('a')['href'])
    #     
 
    quote_list = []    
    while True:
        soup = get_page(page)
        quotes = soup.find_all(class_ = "quote")
        
        for quote in quotes:
            quote_list.append({
                    "quote": quote.find(class_ = "text").text,
                    "author":quote.find(class_ = "author").text,
                    "link": url + quote.find('a')['href']
                    })
            
            
        
        next_page = soup.find(class_ = "next")
        print(next_page)
        if(next_page):
            page = next_page.find('a')['href']
        else:
            break
    
    return quote_list


def start_game(quote_list):
    quote = choice(quote_list)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote['quote'])
    print(quote['author'])
    
    guess = ''
    
    while guess.lower() != quote['author'].lower() and remaining_guesses:
        guess = input(f"Who said this quote? Guesses remaining : {remaining_guesses} ")
        remaining_guesses-=1
        if guess == quote['author']:
            print("YOU GOT IT RIGHT!")
            break
        if remaining_guesses == 3:
            res = requests.get(f"{quote['link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_ = "author-born-date").get_text()
            born_place = soup.find(class_ = "author-born-location").get_text()
            print(f"Here's a hint: The author was born in {birth_date} {born_place}")
            
        if remaining_guesses == 2:
            print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
        if remaining_guesses == 1:
            last_name = quote['author'].split(" ")[-1][0]
            print(f"Here's a hint: The author's last name starts with: {last_name}")
        else:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
    print("After while loop")
        
    again = ''
    
    while again.lower() not in ('y','yes','n','no'):
        again = input("Would you like to play again (y/n)?")
    if again.lower() in ('yes','y'):
        return start_game(quote_list)        
    else:
        print("Goodbye")
        
quotes = load_quotes()

#with open('save_quotes.csv','w') as csv_file:
#    headers = ['quote', 'author', 'link']
#    csv_writer = DictWriter(csv_file,fieldnames=headers)
#    csv_writer.writeheader()
#    for quote in quotes:
#        print(quote)
#        csv_writer.writerow(quote)
start_game(quotes)
    
    
    
    
    
    
    
    
    