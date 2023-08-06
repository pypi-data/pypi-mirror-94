# from logger.logging_functions import login, start_run, log, upload_file, finish_run

from logging_functions import login, start_run, log, upload_file, finish_run

# import ldm_python_client_lib
# ldm = ldm_python_client_lib.logging_functions

# from ldm_python_client_lib.logging_functions import login, start_run, log, upload_file, finish_run


print ("abc")


# print ("ldm ", ldm)


def main():
    print("Starting main ... ")
    logged_in = login('a2@test.com', 'a2')
    if logged_in:
        print("Logged in successfully.")
    else:
        print("Login failed.")
        exit()

    PROJECT_ID = "60086cbd731a62d07b7eb612"
    start_run(PROJECT_ID, "comment", "https://gitlab.com/sprogis/dl-framework/-/commit/dd97bb13d1b95409a4129d7bff90e5c5a64a98d0")
    

    log({"msg": "starting program execution"})
    
    log({"msg": "test msg 1"})

    # upload_file('./python_client_app/weights.txt',".chp")
    # upload_file('./python_client_app/python_logging_client.py', "code")
    # upload_file('./python_client_app/labels.txt',"labels")

    log({"msg": "finishing program execution"})
    
    finish_run()
    return

    


main()
