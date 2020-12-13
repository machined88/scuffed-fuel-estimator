import requests
from bs4 import BeautifulSoup


#Deletes every character after a certain given index.
def shorten(s, subs):
    i = s.index(subs)
    return s[:i+len(subs)]


#Deletes every character before a certain given index.
def inversedshorten(s, subs):
    i = s.index(subs)
    return s[i + len(subs):]

def validateFloatInput(value):
    try:
        return float(value)
    except ValueError:
        print("Wrong value!")

#The car object (maybe not the right name for that? yes).
class Car:
    
    def __init__(self):
        self.carburant_prices = []
        self.carburant_names = []
        self.carburant_types = []
        self.get_page_info()
        self.extract_html_names()
        self.extract_html_prices()
        self.prices_to_float()
        self.get_car_info()

    #Request page in HTML and extract names + prices and merge them into carburant_types list (with the shorten function I made before).
    def get_page_info(self):
        url = "https://carbu.com/france/prixmoyens"
        html_content = requests.get(url).text
        soup1 = BeautifulSoup(html_content, "lxml")

        for x in soup1.find_all("tr", attrs={"class": "officialPriceBe_even"}):
            x = x.text
            (self.carburant_types).append(shorten(x, "€"))
        
    #1 - Extracting fuel names from carburant_types list into carburant_names list.
    #2 - Creating separate strings for each fuel names (with the shorten function I made before).
    def extract_html_names(self):
        #1
        for obj in self.carburant_types:
            if ")" in obj:
                (self.carburant_names).append(shorten(obj, ")"))
            elif "E85" in obj:
                (self.carburant_names).append(shorten(obj, "E85"))
            elif "GPL"in obj:
                (self.carburant_names).append(shorten(obj, "GPL"))
            elif "GNV"in obj:
                (self.carburant_names).append(shorten(obj, "GNV"))
        
        #2
        self.sansplomb95e5 = self.carburant_names[0]
        self.sansplomb95e10 = self.carburant_names[1]
        self.bioethanole85 = self.carburant_names[2]
        self.gazoleb7 = self.carburant_names[3]
        self.gpl = self.carburant_names[4]

    #Extractiing fuel prices from carburant_types list into carburant_prices list (with the inversenshorten function I made before).
    def extract_html_prices(self):
        for obj in self.carburant_types:
            if ")" in obj:
                (self.carburant_prices).append(inversedshorten(obj, ")"))
            elif "E85" in obj:
                (self.carburant_prices).append(inversedshorten(obj, "E85"))
            elif "GPL"in obj:
                (self.carburant_prices).append(inversedshorten(obj, "GPL"))
            elif "GNV"in obj:
                (self.carburant_prices).append(inversedshorten(obj, "GNV"))

    #Creating separate strings for each fuel prices, then convert them to decimals (float).
    def prices_to_float(self):
        self.sansplomb95e5_price = (self.carburant_prices[0][:-2]).replace(",", ".")
        self.sansplomb95e10_price = (self.carburant_prices[1][:-2]).replace(",", ".")
        self.bioethanole85_price = (self.carburant_prices[2][:-2]).replace(",", ".")
        self.gazoleb7_price = (self.carburant_prices[3][:-2]).replace(",", ".")
        self.gpl_price = (self.carburant_prices[4][:-2]).replace(",", ".")

        self.sansplomb95e5_price = float(self.sansplomb95e5_price)
        self.sansplomb95e10_price = float(self.sansplomb95e10_price)
        self.bioethanole85_price = float(self.bioethanole85_price)
        self.gazoleb7_price = float(self.gazoleb7_price)
        self.gpl_price = float(self.gpl_price)
    
    #Getting user inputs for variables.
    def get_car_info(self):
        self.type = input("What type of fuel do you use? (list below, type the letter)\nSans Plomb 95 E5 (a)\nSans Plomb 95 E10 (b)\nBioethanol E85 (c)\nGazole B7 (d)\nGPL (e)\nExit the program (exit)\n").lower()
        while self.type not in {"a", "b", "c", "d", "e", "exit"}:
            print("Only values of a, b, c, d or e are allowed!")
            self.type = input("What type of fuel do you use? (list below, type the letter)\nSans Plomb 95 E5 (a)\nSans Plomb 95 E10 (b)\nBioethanol E85 (c)\nGazole B7 (d)\nGPL (e)\nExit the program (exit)\n").lower()
        if (self.type == "exit"): 
            exit("See you soon!")
        self.refuel = input("Last refuel total amount (in L): ")
        while not self.refuel.isnumeric():
            print("Only numeric values are allowed!")
            self.refuel = input("Last refuel total amount (in L): ")
        self.refuel = validateFloatInput(self.refuel)

        self.fuelamount = input("Current fuel amount (in L): ")
        while not self.fuelamount.isnumeric():
            print("Only numeric values are allowed!")
            self.fuelamount = input("Current fuel amount (in L): ")
        self.fuelamount = validateFloatInput(self.fuelamount)

        self.rerefuel = input("How much fuel do you plan on for your next refuel ? (in L): ")
        while not self.rerefuel.isnumeric():
            print("Only numeric values are allowed!")
            self.rerefuel = input("How much fuel do you plan on for your next refuel ? (in L): ")
        self.rerefuel = validateFloatInput(self.rerefuel)

        print(self.moneyspent())
        print(self.equivalentmoneyfuel())
        print(self.equivalentmoneyrefuel())
        self.__init__()

    #Fuel equivalent in money.
    def moneyspent(self):
        if self.type == 'a':
            total = self.sansplomb95e5_price * self.refuel
    
        elif self.type == 'b':
            total = self.sansplomb95e10_price * self.refuel
    
        elif self.type == 'c':
            total = self.bioethanole85_price * self.refuel
    
        elif self.type == 'd':
            total = self.gazoleb7_price * self.refuel
        
        elif self.type == 'e':
            total = self.gpl_price * self.refuel
        
        return f"Your last refuel ({self.refuel} L) cost {total} €"

    #Lasting fuel equivalent in money.
    def equivalentmoneyfuel(self):
        if self.type == 'a':
            lasting = self.sansplomb95e5_price * self.fuelamount

        elif self.type == 'b':
            lasting = self.sansplomb95e10_price * self.fuelamount

        elif self.type == 'c':
            lasting = self.bioethanole85_price * self.fuelamount

        elif self.type == 'd':
            lasting = self.gazoleb7_price * self.fuelamount

        elif self.type == 'e':
            lasting = self.gpl_price * self.fuelamount

        return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

    #Reuel equivalent in money.
    def equivalentmoneyrefuel(self):
        if self.type == 'a':
            total1 = self.sansplomb95e5_price * self.rerefuel

        elif self.type == 'b':
            total1 = self.sansplomb95e10_price * self.rerefuel

        elif self.type == 'c':
            total1 = self.bioethanole85_price * self.rerefuel

        elif self.type == 'd':
            total1 = self.gazoleb7_price * self.rerefuel

        elif self.type == 'e':
            total1 = self.gpl_price * self.rerefuel

        return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

#Call object and its functions.
car = Car()
