import requests
from datetime import date

def print_result(result):
    print("\n\n")
    if result==[]:
        print("Sorry, no centers for your parameters.\n")
        return
    for row in result:
        print("CENTER DETAILS")
        address = row[0]
        sessions = row[1]
        print("Center Name - {}\nCenter Pin Code - {}\nDistrict - {}\nBlock - {}\nCentre Fee - {}\n".format(*address))
        print("Printing Sessions for this center:")
        for session in sessions:
            print("For",session[2],end='\t')
            print("{} doses available with minimum age {} and vaccine {}".format(session[0],session[1],session[3]))
        print("\n")

def extract_info(data,age):
    result = []
    centers = data['centers']
    for center in centers:
        center_name = center['name']
        centre_pincode = center['pincode']
        district_name = center['district_name']
        block_name = center['block_name']
        centre_fee = center['fee_type']
        sessions = center['sessions']
        temp_result = []
        for session in sessions:
            available_capacity = int(session['available_capacity'])
            if available_capacity == 0:
                continue

            session_age = int(session['min_age_limit'])
            if session_age>age:
                continue
            session_date = session['date']
            session_vaccine = session['vaccine']
            if session_vaccine=='':
                session_vaccine = 'unkown'
            row = (available_capacity,session_age,session_date,session_vaccine)
            temp_result.append(row)
        if temp_result != []:
            address = (center_name,centre_pincode,district_name,block_name,centre_fee)
            row = (address, temp_result)
            result.append(row)

    return result


if __name__ == '__main__':
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    pin = input("Please enter pincode:")
    age = int(input("Please enter your age:"))
    today = date.today()
    date = "{}-{}-{}".format(today.day,today.month,today.year)
    PARAMS = {'pincode':pin, 'date':date}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    if r.status_code == 400:
        print("Wrong input parameters. Please check. \n")
        exit(0)
    if not data:
        print("Sorry. Not found.\n")
    result = extract_info(data,age)
    print_result(result)
