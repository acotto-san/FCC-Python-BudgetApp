class Category:
    
    def __init__(self,category_name) -> None:
        self.category_name = category_name.capitalize()
        self.ledger = []
        self.total = 0
        self.total_withdrawals = 0

    def get_category_name(self):
        return self.category_name
    
    def add_to_ledger(self,object):
        self.ledger.append(object)
        self.add_to_total(object["amount"])

    def deposit(self,amount,description=""):
        self.add_to_ledger({"amount":amount,"description":description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.add_to_ledger({"amount":-amount,"description":description})
            self.add_to_total_withdrawals(amount)
            return True
        else: return False

    def add_to_total(self,amount):
        self.total += amount

    def get_balance(self):
        return self.total
    
    def check_funds(self,amount):
        if self.get_balance() >= amount:
            return True
        else: return False

    def transfer(self,amount,buget_category):
        if self.check_funds(amount):
            self.withdraw(amount,"Transfer to {}".format(buget_category.get_category_name()))
            buget_category.deposit(amount,"Transfer from {}".format(self.get_category_name()))
            return True
        else: return False
    
    def get_ledger(self):
        return self.ledger

    def __str__(self) -> str:
        title = self.get_category_name().center(30,'*')
        to_str = "{}\n".format(title)
        
        for i in self.get_ledger():
            ledger_description_characters = 23
            ledger_amount_characters = 7

            ledger_item = i["description"][:ledger_description_characters].ljust(ledger_description_characters)
            ledger_item += format(i["amount"],'.2f')[:ledger_amount_characters].rjust(ledger_amount_characters)
            to_str += "{}\n".format(ledger_item)    
        
        to_str += "Total: {}".format(self.get_balance(),'.2f')

        return to_str

    def add_to_total_withdrawals(self,amount):
        self.total_withdrawals += amount

    def get_total_withdrawals(self):
        return self.total_withdrawals


def create_spend_chart(categories_list):
    spend_chart = "Percentage spent by category\n"
    spend_chart += add_percentage_lines(categories_list)
    spend_chart += add_category_names([cat.get_category_name() for cat in categories_list])
    return spend_chart

def add_percentage_lines(category_list):

    percentage_line = ""

    for i in range (100,-1,-10):
        percentage_line += "{}|".format(i).rjust(4)
        for category in category_list:
            percentage = (category.get_total_withdrawals()*100)/sum([cat.get_total_withdrawals() for cat in category_list ])
            
            if (percentage//10)*10 >= i:
                percentage_line += " o "
            else:
                percentage_line += "   "
        percentage_line += " \n"
    
    percentage_line += add_separation_line(len(category_list))
    return percentage_line

def add_separation_line(amount_percentage_items):
    separation_line = "    "
    for x in range (amount_percentage_items):
        separation_line += "---"
    separation_line += "-\n"
    return separation_line

def add_category_names(category_names_list):
    category_names_lines = ""
    padding = "    "

    for i in range(len(max(category_names_list, key=len))):

        category_names_lines += padding

        for name in category_names_list:
            if i < len(name):
                category_names_lines += " {} ".format(name[i])
            else:
                category_names_lines += "   "
                
        if i != len(max(category_names_list, key=len))-1:
            category_names_lines += " \n"
        else:
            category_names_lines += " "
            
    return category_names_lines
