import asyncio
from gtts import gTTS
from googletrans import Translator
import random as r
import datetime as dt
import speech_recognition as sr
import pyttsx3
import playsound3 as ps
import os 

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


# -----------------------
# CARD DETAILS
# -----------------------
user_balance = 100000
card_pin = 1234
card_id = "PTH2786940263QK"
is_authenticated = False
pref_lang = 'en'

# -----------------------
# speech system
# -----------------------
class Speak_Lang():
    def __init__(self):

        self.lang = pref_lang
        self.translator = Translator()

    def speak_lang(self,text):
        if self.lang != "en":
            try:
                result = asyncio.run(self.translator.translate(text, dest=self.lang))
                translated_text = result.text
            except Exception as e:
                print('Error occur in translation.',e)
                translated_text = text
            

        else: translated_text = text
        try:
            tts =gTTS(translated_text,lang=self.lang)
            filename = "voice.mp3"
            tts.save(filename)
            ps.playsound(filename)
        except Exception as e:
            print(f"Audio playback/TTS error: {e}")

        finally:
            os.remove(filename)
# 

def show_show_options():
    print("""
Choose one service at a time from following:-

1. Check your bank balance
2. Withdraw money from your bank account
3. Change the Card PIN
4. Give feedback of our services
5. Write complain to the bank
6. Exit
""")




# -----------------------
# Get User Input
# -----------------------
def get_user_choice(hint):
    user_choice = input(f"Enter your {hint}: ")
    return user_choice



# -----------------------
# Check valid input
# -----------------------
def is_correct_option_int_input(user_choice,start=1,end=6):
    try:
        user_int_choice = int(user_choice)
        if start <= user_int_choice <= end:
            return user_int_choice
        else:
            s1.speak_lang("Please select option from 1 to 6")
            print("Please select option from 1 to 6")
            return show_show_options()
    
    except ValueError:
        sl.speak_lang("Please enter valid option in given format")
        print("please enter the valid option")



# -----------------------
# Check account balance
# -----------------------
def check_balance():
    return user_balance



# -----------------------
# Check or Change card PIN
# -----------------------
def check_card_pin(sl,change = False):
    i = 1
    while i <= 5:
        if i == 1 and 4:
            print(pref_lang)
            sl.speak_lang("Please enter your current four digits Card PIN")
        pin = get_user_choice('four digit PIN')
        pin = int(pin)
        if change == True:
            sl.speak_lang("Please enter your new four digits Card PIN")
            new_pin = get_user_choice('new four digit PIN')
            new_pin = card_pin
            sl.speak_lang("congratulations! Your card PIN is updated.")
        if pin == card_pin:
            global is_authenticated
            is_authenticated = True
            sl.speak_lang('User verification done!')
            break

        else:
            if i == 1 and 4:
                sl.speak_lang(f"Wrong PIN. Please notice that you only have {5-i} attempts left after last attempt we will block your's card for 2 days.")
            elif i == 5:
                sl.speak_lang("You crossed your pin limits. now we are blocking your A.T.M. card. For further queries visit the nearest bank branch.")
                break
            print(f"Wrong PIN. Try again {i} out of 5 try")
            i = i+1
            continue



# -----------------------
# Check original User
# -----------------------
def check_authenticated_user():

    if is_authenticated:
                check_card_pin()
            
    else: 
        print("Unauthenticated person. For reset Card PIN contact with bank branch. ")
        print("Thanks!")



# -----------------------
# withdraw function
# -----------------------
def withdraw_money(withdraw_amount,sl):
    global user_balance
    try:
        withdraw_amount = int(withdraw_amount)
        if user_balance < withdraw_amount:
            print(f"Your balance is insufficient. your account balance is {user_balance}! ")
        elif user_balance == withdraw_amount or user_balance == (withdraw_amount + 500):
            print("You can't withdraw all amount from your account. Minimum $500 is required to maintain bank account!. Try again! ")
        else:
            current_balance = user_balance - withdraw_amount
            user_balance = current_balance
            print(f"taking money process successfully. please take your money and your's available balance is {user_balance}!")
            sl.speak_lang(f"Withdraw process successfully. please take your money and your's available balance is {user_balance}!")

            return True
            
    except ValueError:
        print("Use Numerical values for amount!")



# -----------------------
# Complain function
# -----------------------
def complain_submition(sl):

    complains = [
        'Problem in Authentication ',
        'Problem in cash counting',
        'Problem in selectinng button/options',
        'Problem in reset Card PIN',
        'Problem in Display screen'
    ]
    sl.speak_lang("We appologise for our mistakes. Please try to provide complete complain or select complain for following options.")
    print("""
    We applogise for our mistakes. Please try to provide complete complain or select complain for following options:-

    1. Problem in Authentication 
    2. Problem in cash counting
    3. Problem in selecting button/options
    4. Problem in reset Card PIN
    5. Problem in Display screen
    6. Others. 
    """)

    user_complain = get_user_choice("complain for the show_options")
    valid_option = is_correct_option_int_input(user_choice=user_complain)

    if 1<= valid_option <=5:
        sl.speak_lang(f'Sorry for our mistake! your complain regarding "{complains[(valid_option - 1)]}" is submitted successfully. Our team do the needfull queries.')
        print(f'Sorry for our mistake! your complain regarding "{complains[(valid_option - 1)]}" is submitted successfully. Our team will answer the required correction.')
        
    else:
        sl.speak_lang("Its looking like you're encounting new techniqual issue. PLease write your complain in box.")
        usr_comp = get_user_choice('complain in detail:')
        sl.speak_lang('Sorry for our mistake! your complain is submitted successfully. Our team do the needfull queries.')
        print('Sorry for our mistake! your complain is submitted successfully. Our team do the needfull queries.')

    sl.speak_lang("Enter any key to go to Home Tab. ")
    cont = input("Enter any key to go back to Home tab: ")
    return



# -----------------------
# Creating receipt 
# -----------------------
def give_receipt(user_balance,withdraw_amount):
    token_no = r.randint(1000000000,100000000000)
    date = dt.datetime.now()
    print(f"""
    *************************************
    *               *                   *
    *   Token No.   *   {token_no}      *
    *               *                   *
    *************************************
    *               *                   *
    *   Card ID.    *   {card_id}       *
    *               *                   *
    *************************************
    *               *                   *
    *   Withdraw    *  {withdraw_amount}*
    *               *                   *
    *************************************
    *               *                   *
    *   Aval. bal.  *  {user_balance}   *
    *               *                   *
    *************************************
    *               *                   *
    *   date        *  {date}*
    *               *                   *
    *************************************
    """)



def choose_lang():
    global pref_lang
    
    engine.say("Your's Card inserted successfully! Don't try to remove it. Welcome to Python A.T.M. Please select your language for better experience.")
    engine.runAndWait()
    
    print("""
Select the language in which you want to communicate:
1. English
2. Hindi
3. Punjabi
""")

    while True:
        lang = input("Enter Your language (1-3): ")
        cho_lang = is_correct_option_int_input(lang, 1, 3)
        if cho_lang is not None:
            break

    if cho_lang == 1:
        pref_lang = 'en'
    elif cho_lang == 2:
        pref_lang = 'hi'
    else:
        pref_lang = 'pa'

    print("Selected language", pref_lang)




# ----------------------
# MAIN FUNCTION
# ----------------------

def main():
    print("Welcome to Python A.T.M. ")
    choose_lang()
    sl = Speak_Lang()
    #  invoking check_card_pin function
    check_card_pin(sl)


    if is_authenticated:
                while True:
                    show_show_options()
                    sl.speak_lang("Please! enter service code that you may want to use.")
                    user_choice = get_user_choice('choice')
                    valid_choice = is_correct_option_int_input(user_choice=user_choice)
                    
                    # ----------------------
                    # Checking bank balance
                    # ----------------------
                    if valid_choice == 1:
                        balance = check_balance()
                        print(f"Your current account balance is {balance}")
                        sl.speak_lang(f"Your current account balance is {balance}")

                        
                    
                    # ----------------------
                    # Withdrawing money process
                    # ----------------------

                    elif valid_choice == 2:
                        withdraw_attempt = 1
                        while withdraw_attempt <= 3:
                            sl.speak_lang("Enter the amount your want to take!")
                            withdraw_amount = get_user_choice("money account you want to withdraw")
                            withdrawed = withdraw_money(withdraw_amount,sl)
                            withdraw_attempt = withdraw_attempt+1
                            if withdraw_attempt == 4 :
                                print("You cross withdraw amount limit. Try again by inserting card again!")
                                sl.speak_lang("You cross withdraw amount limit. Try again by inserting card again!")
                                exit()
                            elif withdrawed:
                                sl.speak_lang("Do you want receipt! ")
                                receipt = input("Do you want receipt!(Yes/No ): ")
                                if receipt == 'Yes' or 'yes':
                                    sl.speak_lang("please wait we are making your receipt!")
                                    give_receipt(user_balance,withdraw_amount)
                                    sl.speak_lang("Now! we are moving back you to main screen")
                                    break
                                else:
                                  break

                        

                    # ----------------------
                    # Change Card PIN
                    # ----------------------
                    elif valid_choice == 3:
                        check_card_pin(sl=sl,change=True)
                        print("Card PIN updated successfully!")
                        sl.speak_lang("Card PIN updated successfully!")



                    # ----------------------
                    # FeedBack Process
                    # ----------------------
                    elif valid_choice == 4:
                        sl.speak_lang("We appreciate your feedback decision. select number from 1 to 6.")
                        user_feedback = get_user_choice("feedback stars from 1 to 6!")
                        valid_feedback = is_correct_option_int_input(user_choice=user_feedback)
                        if 5 <= valid_feedback <=6:
                            print("Your feedback submited! thanks for submition")
                            sl.speak_lang("Your feedback submited! thanks for submition and appreciation our services.")

                        elif 1 <= valid_feedback <=3:
                            print("Your feedback submited! thanks for submition. Please provide complain or suggestion to improve our service.")
                            sl.speak_lang("Your feedback submited! thanks for submition. Please provide complain or suggestion to improve our service.")
                            sl.speak_lang("Enter any key to go to Home Tab. ")
                            cont = input("Enter any key to go back to Home tab: ")
                            

                    
                    # ----------------------
                    # Complain Process
                    # ----------------------
                    elif valid_choice == 5:
                        complain_submition(sl)


                    # ----------------------
                    # exit Process
                    # ----------------------
                    elif valid_choice == 6:
                        print('Thanks for using our services. Please take your"s card when light stop blinking')
                        sl.speak_lang('Thanks for using our services. Please take your"s card when light stop blinking')

                        break
    else: 
        print("Unauthenticated person. For reset Card PIN contact with bank branch. ")
        print("Thanks!")
        sl.speak_lang("Unauthenticated person. For reset Card PIN contact with bank branch. Thanks!")



if __name__ == "__main__":
    main()