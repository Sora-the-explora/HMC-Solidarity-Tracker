from bs4 import BeautifulSoup
import requests

Initial = 17050

def getGFM(Initial = Initial):
    """
    Scrapes the GFM for the amount raised in the progress bar. Takes amount you're measuring against as a parameter
    """

    #get the HTML of the GFM page
    link = "https://www.gofundme.com/f/hmc-solidarity-covid19-mutual-aid-fund"
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')

    #parse the progress bar, convert the object to a string and then an int
    h2 = str(soup.find_all('h2', class_='m-progress-meter-heading'))
    raised = h2[h2.index("$")+1:h2.index("<!")]
    big = raised[:raised.index(",")]
    small = raised[raised.index(",")+1:]
    numraised = int(big)*1000 + int(small)

    total = numraised - Initial

    return total

print(getGFM())