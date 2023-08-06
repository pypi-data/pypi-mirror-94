
class Zebra(object):
    total_zebras = []
    def __init__(self,name):
        self.name = name
        self.groupname  = "BCA Wale"
        self.jungle = "Bangalore"
        total.zebras.append(self)
        self.link = 'https://en.wikipedia.org/wiki/Zebra'



    @property
    def group(self):
        return self.groupname

    @property
    def author(self):
        return "Jogendra Singh "
    @group.setter
    def group(self,group):
        self.groupname = group
    def play(self):
        print("Zebras Don't play you dumb")

    def info(self):
        print(f"My name is {self.name} and i'm from {self.groupname}\nJungle {self.jungle} For more info : {self.link}")

    def speak(self):
        print("Dechu Dechu...")

    def total(self):
        print(f"{self.total_zebras}")
        


    