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


#The car object (maybe not the right name for that? yes).
class Car:
    
    def __init__(self):
        self.carburant_prices = []
        self.carburant_names = []
        self.carburant_types = []

    #Requtest page in HTML and extract names + prices ----> carburant_types list (with the shorten function I made before).
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
        self.type = input("What type of fuel do you use? (list below, type the letter)\nSans Plomb 95 E5 (a)\nSans Plomb 95 E10 (b)\nBioethanol E85 (c)\nGazole B7 (d)\nGPL (e)\n").lower()
        self.refuel = float(input("Last refuel total amount (in L): "))
        self.fuelamount = float(input("Current fuel amount (in L): "))
        self.rerefuel = float(input("How much fuel do you plan on for your next refuel ? (in L): "))

    #Fuel equivalent in money.
    def moneyspent(self):
        if self.type == 'a':
            total = self.sansplomb95e5_price * self.refuel
            return f"Your last refuel ({self.refuel} L) cost {total} €"

        if self.type == 'b':
            total = self.sansplomb95e10_price * self.refuel
            return f"Your last refuel ({self.refuel} L) cost {total} €"

        if self.type == 'c':
            total = self.bioethanole85_price * self.refuel
            return f"Your last refuel ({self.refuel} L) cost {total} €"

        if self.type == 'd':
            total = self.gazoleb7_price * self.refuel
            return f"Your last refuel ({self.refuel} L) cost {total} €"

        if self.type == 'e':
            total = self.gpl_price * self.refuel
            return f"Your last refuel ({self.refuel} L) cost {total} €"

    #Lasting fuel equivalent in money.
    def equivalentmoneyfuel(self):
        if self.type == 'a':
            lasting = self.sansplomb95e5_price * self.fuelamount
            return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

        if self.type == 'b':
            lasting = self.sansplomb95e10_price * self.fuelamount
            return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

        if self.type == 'c':
            lasting = self.bioethanole85_price * self.fuelamount
            return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

        if self.type == 'd':
            lasting = self.gazoleb7_price * self.fuelamount
            return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

        if self.type == 'e':
            lasting = self.gpl_price * self.fuelamount
            return f"With {self.fuelamount} L lasting, you have the equivalent of {lasting} € to drive before another refuel."

    #Reuel equivalent in money.
    def equivalentmoneyrefuel(self):
        if self.type == 'a':
            total1 = self.sansplomb95e5_price * self.rerefuel
            return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

        if self.type == 'b':
            total1 = self.sansplomb95e10_price * self.rerefuel
            return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

        if self.type == 'c':
            total1 = self.bioethanole85_price * self.rerefuel
            return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

        if self.type == 'd':
            total1 = self.gazoleb7_price * self.rerefuel
            return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

        if self.type == 'e':
            total1 = self.gpl_price * self.rerefuel
            return f"Your next refuel (you plan {self.rerefuel} L) will cost {total1} €"

#Call object and its functions.
car = Car()
car.get_page_info()
car.extract_html_names()
car.extract_html_prices()
car.prices_to_float()
car.get_car_info()
print(car.moneyspent())
print(car.equivalentmoneyfuel())
print(car.equivalentmoneyrefuel())