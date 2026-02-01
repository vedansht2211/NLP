from datetime import datetime
import webbrowser
import requests

def get_location():
    response=requests.get("http://ip-api.com/json/")
    data=response.json()
    city=data.get('city',"unknown")
    country=data.get('country',"unknown")
    return city,country

weather_api="94dc82a3070ddc73c0f2ec753b59574b"
def get_weather():
    response=requests.get("http://ip-api.com/json/")
    data=response.json()
    lon=data.get('lon',"unknown")
    lat=data.get('lat',"unknown")
    res=requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api}&units=metric")
    temp=res.json()
    desc=temp['weather'][0]['description']
    cur_temp=temp['main']['temp']
    feels=temp['main']['feels_like']
    humidity=temp['main']['humidity']
    print(f"\n Weather     : {desc}\n Temperature : {cur_temp}°C\n Feels like  : {feels}°C\n Humidity    : {humidity}%\n")










chat=1
greet=["hello","hey","hi","hi there"]
datemsg=["tell me date","todays date","whats the date","date"]
timemsg=["tell me time","current time","whats the time","time"]
end=["bye","stop","end","dont talk","stop talking","blocked","block","shut up"]
cal=["cal","calculate","calc"]
while chat:
    msg=input("enter your msg : ").lower()

    if msg in end:
        break
    #weather
    elif ("temp" in msg) or ("temperature" in msg) or ("weather" in msg):
        get_weather()
    #websites
    elif msg.split()[0]=="open":
        s=msg.split()[1]
        link="https://www."+s+".com"
        webbrowser.open(link)
    #calculator
    elif msg.split()[0] in cal:
        s=msg.split()[1]
        print(eval(s))
    #location
    elif "location" in msg:
        city,country=get_location()
        print(f"\nYour location is {city},{country}")
    #greets
    elif msg in greet:
        print("hi how are you")
    #date
    elif msg in datemsg:
        print(datetime.now().date())
    #time
    elif msg in timemsg:
        cur=datetime.now().time()
        print(cur.strftime("%I:%M:%S"))

    else:
        print("i cant understand")