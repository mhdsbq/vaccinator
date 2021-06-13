# search vaccination centere by district
# display centers inside selected district
# chose multipple centers
# 
# initialise look up loop
# using api, search avilability every 1 minute for the specefic centere or centers
import requests
import time

from datetime import date

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def getDistrictId():
    response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/17', headers=headers)

    if response.ok:
        r_json = response.json()
        max_length = 0
        for dist in r_json["districts"]:  
            # Fiend the length of the longest district name
            if len(dist['district_name'])>max_length:
                max_length = len(dist['district_name'])
        for dist in r_json["districts"]:   
            print(f"{dist['district_name']: <{max_length}} : {dist['district_id']}")    

def getCenterByDistrict(district_id, date="12-06-2021"):
    response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}', headers=headers)
    response_json =  response.json()
    #print(response_json)
    for center in response_json['centers']:
       print(f"{center['name']}--{center['fee_type']}")
       for session in center['sessions']:
           print(f"{session['date']} -- {session['available_capacity_dose1']} --min age:{session['min_age_limit']}")

def getAvilableCenterByDistrict(district_id,date):
    response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}', headers=headers)
    response_json =  response.json()
    #print(response_json)
    for center in response_json['centers']:
        print(f"{center['name']}--{center['fee_type']}")
        dose_avilability = False
        for session in center['sessions']:
            if session['available_capacity_dose1'] != 0:
                print(f"      {session['date']} -- {session['available_capacity_dose1']} --min age:{session['min_age_limit']}")
                dose_avilability = True
        if dose_avilability == False:
            print("      Dose not avilable")
def getTodayDate():
    today = date.today()
    return today.strftime("%d-%m-%Y")
def playAmbulanceSound():
    from playsound import playsound
    playsound("ambulance.mp3")
    
def liveNotify(district_id,date,age):
    while True:
        response = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}', headers=headers)
        response_json =  response.json()
        #print(response_json)
        for center in response_json['centers']:
            for session in center['sessions']:
                if session['available_capacity_dose1'] != 0 and int(session['min_age_limit'])<=age:
                    playAmbulanceSound()
                    print(f"{center['name']}--{center['fee_type']}")
                    print(f"      {session['date']} -- {session['available_capacity_dose1']} --min age:{session['min_age_limit']}")
        time.sleep(60*2)
        print("...")



def main():
    getDistrictId()
    district_id = int(input("enter your District Id: "))
    today = getTodayDate()
    #getCenterByDistrict(district_id,today)
    print("##############################################################################################################")
    getAvilableCenterByDistrict(district_id,today)
    age = int(input("To get live notification enter your age: "))
    print("[LIVE NOTIFY IS ACTIVE...]")
    liveNotify(district_id, today, age)
    
main()
