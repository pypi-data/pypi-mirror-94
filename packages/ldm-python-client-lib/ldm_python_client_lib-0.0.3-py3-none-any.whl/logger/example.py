from logging_functions import login, start_run, log, upload_file, finish_run

# import ldm_python_client_lib
# ldm = ldm_python_client_lib.logging_functions

# from ldm_python_client_lib.logging_functions import login, start_run, log, upload_file, finish_run


print ("abc")


# print ("ldm ", ldm)


def main():
    print("Starting main ... ")
    logged_in = login('a1@test.com', 'a1')
    if logged_in:
        print("Logged in successfully.")
    else:
        print("Login failed.")
        exit()

    start_run("5ff5d74b925b02e4de347a15",
                # "5fce614dd489a6fe90ec221b",
                "comment",
                "https://gitlab.com/sprogis/dl-framework/-/commit/dd97bb13d1b95409a4129d7bff90e5c5a64a98d0")
    

    log({"msg": "starting program execution"})
    
    log({"msg": "test msg 1"})

    # upload_file('./python_client_app/weights.txt',".chp")
    # upload_file('./python_client_app/python_logging_client.py', "code")
    # upload_file('./python_client_app/labels.txt',"labels")

    log({"msg": "finishing program execution"})
    
    finish_run()
    return

    


main()
