from tkinter import *
import customtkinter as ctk
import pywinstyles
import requests
import json

API_KEY = "cd73eff588d9418f80901527242607"
WIDTH = 600
HEIGHT = 400

class App(Tk):

    def __init__(self, app_title, theme):
        super().__init__()
        pywinstyles.apply_style(self, theme)
        pywinstyles.change_title_color(self, color="white") 
        pywinstyles.change_border_color(self, color="#588157")

        self.title(app_title)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.iconbitmap("weather-app.ico")

        self.openingLabel = ctk.CTkLabel(self, text="Hello again,", font=ctk.CTkFont(size=50, weight="bold"))
        self.openingLabel.place(x=160, y=30)

        self.locationLabel = ctk.CTkLabel(self, text=f"You are currently in {request_current()["location"]["name"]}, {request_current()["location"]["region"]}.", font=ctk.CTkFont(size=18, weight="normal"))
        self.locationLabel.place(x=10, y=120)


if __name__ == "__main__":

    def request_current():
        info = requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=auto:ip&lang=pt")
        content = info.content
        content = json.loads(content)
        return content


    print(request_current()["current"]["condition"]["text"])
    app = App("Weather", "acrylic")
    app.mainloop()