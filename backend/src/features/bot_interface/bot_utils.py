from database.supabase import supabase
import time

def callback(res, payload, username):
    print("Callback 1: ", payload)
    new_login_passcode = ""
    if "record" in payload and "login_passcode" in payload["record"] and "username" in payload["record"]:
        if payload["record"]["username"] == username:
            new_login_passcode = payload["record"]["login_passcode"]
    if new_login_passcode != "":
        res["new"] = new_login_passcode

def respond_from_message(message: str) -> str:
    return "The function to produce this message has not been implemented yet :("

def get_phone_passcode(username: str) -> str:
    timeout_limit = 120
    timeout_curr = 0

    while timeout_curr <= timeout_limit:
        data = supabase.from_("login_passcode") \
                        .select("login_passcode") \
                        .eq("username", username) \
                        .limit(1) \
                        .execute()
        if data.data is not None:
            if len(data.data) == 1:
                login_passcode = data.data[0]["login_passcode"]
                if login_passcode is not None:
                    supabase.from_("login_passcode") \
                            .delete() \
                            .eq("username", username) \
                            .execute()
                    print("Passcode: ", login_passcode)
                    return login_passcode
        print("waiting for login passcode for ", username, "...")      
        time.sleep(5)
        timeout_curr += 5
    
    return ""

        


    