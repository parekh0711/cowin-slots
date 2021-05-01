import requests
import argparse
from datetime import date
from time import sleep
from playsound import playsound


def initialize_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pin_code", type=str,
                        help="PIN_CODE to look in")
    parser.add_argument("-a", "--age", type=int, help="AGE to look for")
    parser.add_argument("-r", "--retry_in", type=int,
                        default=10, help="Retry lookup in RETRY_IN seconds")
    parser.add_argument("-pi", "--print_in", type=int,
                        default=600, help="Print elapsed time every PRINT_IN seconds\n\
                        This should be a multiple of RETRY_IN")
    return parser


def print_result(result):
    print("\n\n")
    if result == []:
        print("Sorry, no centers for your parameters.\n")
        return
    for row in result:
        print("CENTER DETAILS")
        address = row[0]
        sessions = row[1]
        print("Center Name - {}\nCenter Pin Code - {}\nDistrict - {}\nBlock - {}\nCentre Fee - {}\n".format(*address))
        print("Printing Sessions for this center:")
        for session in sessions:
            print("For", session[2], end='\t')
            print("{} doses available with minimum age {} and vaccine {}".format(
                session[0], session[1], session[3]))
        print("\n")


def extract_info(data, age):
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
            if session_age > age:
                continue
            session_date = session['date']
            session_vaccine = session['vaccine']
            if session_vaccine == '':
                session_vaccine = 'unknown'
            row = (available_capacity, session_age,
                   session_date, session_vaccine)
            temp_result.append(row)
        if temp_result != []:
            address = (center_name, centre_pincode,
                       district_name, block_name, centre_fee)
            row = (address, temp_result)
            result.append(row)

    return result


def main():
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    args = initialize_parser().parse_args()
    pin = args.pin_code
    if not pin:
        pin = input("Please enter pincode: ")
    age = args.age
    if not age:
        age = int(input("Please enter your age: "))
    retry_in = args.retry_in
    print_in = args.print_in
    today = date.today()
    cowin_date = "{}-{}-{}".format(today.day, today.month, today.year)
    PARAMS = {'pincode': pin, 'date': cowin_date}
    idx = 0
    while (1):
        time_elapsed = idx * retry_in
        try:
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            if r.status_code == 400:
                print("Wrong input parameters. Please check. \n")
                exit(0)
            if not data:
                print("Sorry. Not found.\n")
            result = extract_info(data, age)
            if result:
                print('Register now!')
                print_result(result)
                while(1):
                    playsound('alarm.wav')
            else:
                if time_elapsed % print_in == 0:
                    print('Can not register yet. Time elapsed {} mins'.format(
                        time_elapsed / 60))
        except requests.exceptions.ConnectionError:
            print("Connection error. Will silently retry in {} seconds".format(retry_in))
        sleep(retry_in)
        idx += 1


if __name__ == '__main__':
    main()