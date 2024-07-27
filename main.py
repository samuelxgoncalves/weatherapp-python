from tkinter import *
import customtkinter as ctk
from PIL import ImageTk, Image
import pywinstyles
import requests
import json
from datetime import datetime
import urllib
import io

def request_current():
        info = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q=Sesimbra&lang=pt")
        content = info.content
        content = json.loads(content)
        return content

def url_img(url):
   with urllib.request.urlopen(url) as u:
       raw_data = u.read()
       return raw_data
    #data = urllib.request.urlopen(url).read()
   
def get_hour_icon(day, hour):
    CURRENT_HOUR_ICON = url_img(f"http:{request_current()["forecast"]["forecastday"][day]["hour"][hour]["condition"]["icon"]}")
    hour_image = Image.open(io.BytesIO(CURRENT_HOUR_ICON))
    icon = ctk.CTkImage(hour_image, size=(64, 64))
    return icon

def get_hour_temp(day, hour):
    return request_current()["forecast"]["forecastday"][day]["hour"][hour]["temp_c"]

API_KEY = "x"
WIDTH = 1200
HEIGHT = 700


CITY = request_current()["location"]["name"]
REGION = request_current()["location"]["region"]
CURRENT_TEMP = request_current()["current"]["temp_c"]
CONDITION_TEXT = request_current()["current"]["condition"]["text"]
MIN_TEMP = request_current()["forecast"]["forecastday"][0]["day"]["mintemp_c"]
MAX_TEMP = request_current()["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
CURRENT_DATETIME = datetime.now()
CURRENT_HOUR = CURRENT_DATETIME.hour

class App(Tk):

    def __init__(self, app_title, theme):
        super().__init__()

        pywinstyles.apply_style(self, theme)
        pywinstyles.change_title_color(self, color="white") 
        pywinstyles.change_border_color(self, color="#588157")

        self.title(app_title)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.iconbitmap("weather-app.ico")

        APPFRAMECOLOR = "DeepSkyBlue4"
        self.appFrame = ctk.CTkFrame(self, width=1175, height=675, border_width=0, fg_color=APPFRAMECOLOR)
        self.appFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        OPENINGCOLOR = "mint cream"
        self.openingImgLoad = ctk.CTkImage(Image.open("haze.png"), size=(200, 113))
        self.openingImgLabel = ctk.CTkLabel(self.appFrame, image=self.openingImgLoad, text="", bg_color=APPFRAMECOLOR)
        self.openingImgLabel.place(relx=0.5, rely=0.11, anchor=CENTER)
        
        self.cityLabel = ctk.CTkLabel(self, text=CITY, font=ctk.CTkFont("Lexend", size=30, weight="bold"), text_color=OPENINGCOLOR, fg_color=APPFRAMECOLOR)
        self.cityLabel.place(relx=0.5, rely=0.25, anchor=CENTER)

        self.curTempLabel = ctk.CTkLabel(self, text=f"{CURRENT_TEMP}°", font=ctk.CTkFont("Lexend", size=34, weight="bold"), text_color=OPENINGCOLOR, fg_color=APPFRAMECOLOR)
        self.curTempLabel.place(relx=0.505, rely=0.295, anchor=CENTER)

        self.curCondLabel = ctk.CTkLabel(self, text=CONDITION_TEXT, font=ctk.CTkFont("Lexend", size=20, weight="bold"), text_color=OPENINGCOLOR, fg_color=APPFRAMECOLOR)
        self.curCondLabel.place(relx=0.5, rely=0.335, anchor=CENTER)

        self.minmaxLabel = ctk.CTkLabel(self, text=f"{MIN_TEMP}° | {MAX_TEMP}°", font=ctk.CTkFont("Lexend", size=15, weight="bold"), text_color=OPENINGCOLOR, fg_color=APPFRAMECOLOR)
        self.minmaxLabel.place(relx=0.5, rely=0.365, anchor=CENTER)

        HOURLYFRAMECOLOR = "cadet blue"
        self.hourlyFrame = ctk.CTkFrame(self.appFrame, width=1150, height=120, border_width=0, fg_color=HOURLYFRAMECOLOR)
        self.hourlyFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        hour_count_x = 80
        for i in range(CURRENT_HOUR, 24):
            if i == CURRENT_HOUR:
                self.hourLabel = ctk.CTkLabel(self.hourlyFrame, text="Now", font=ctk.CTkFont("Lexend", size=14, weight="bold"), text_color="dark slate gray", fg_color=HOURLYFRAMECOLOR)
                self.hourLabel.place(x=30, y=24, anchor=CENTER)

                self.nowImgLabel = ctk.CTkLabel(self.hourlyFrame, image=get_hour_icon(0, CURRENT_HOUR), text="", bg_color=HOURLYFRAMECOLOR)
                self.nowImgLabel.place(x=30, y=62, anchor=CENTER)

                self.hourTempLabel = ctk.CTkLabel(self.hourlyFrame, text=get_hour_temp(0, CURRENT_HOUR), font=ctk.CTkFont("Lexend", size=14, weight="bold"), text_color="dark slate gray", fg_color=HOURLYFRAMECOLOR)
                self.hourTempLabel.place(x=30, rely=0.82, anchor=CENTER)
            else:
                self.hourLabel = ctk.CTkLabel(self.hourlyFrame, text=i, font=ctk.CTkFont("Lexend", size=12, weight="bold"), text_color="midnight blue", fg_color=HOURLYFRAMECOLOR)
                self.hourLabel.place(x=hour_count_x, y=25, anchor=CENTER)

                self.nowImgLabel = ctk.CTkLabel(self.hourlyFrame, image=get_hour_icon(0, i), text="", bg_color=HOURLYFRAMECOLOR)
                self.nowImgLabel.place(x=hour_count_x, y=62, anchor=CENTER)

                self.hourTempLabel = ctk.CTkLabel(self.hourlyFrame, text=get_hour_temp(0, i), font=ctk.CTkFont("Lexend", size=14, weight="bold"), text_color="dark slate gray", fg_color=HOURLYFRAMECOLOR)
                self.hourTempLabel.place(x=hour_count_x, rely=0.82, anchor=CENTER)

                hour_count_x += 50

        WEEKLYFRAMECOLOR = "steel blue"
        self.weeklyFrame = ctk.CTkFrame(self.appFrame, width=750, height=270, border_width=0, fg_color=WEEKLYFRAMECOLOR)
        self.weeklyFrame.place(relx=0.5, rely=0.82, anchor=CENTER)



        NAVBARCOLOR = "gray2"
        self.botnavbarFrame = ctk.CTkFrame(self, width=820, height=50, border_width=1, border_color="gray12", fg_color=NAVBARCOLOR)
        self.botnavbarFrame.place(relx=0.5, rely=1.01, anchor=S)


if __name__ == "__main__":

    app = App("Weather", "acrylic")
    app.mainloop()
