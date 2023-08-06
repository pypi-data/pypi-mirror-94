from logging_functions import Logger
import os

def main():
    print("Starting main ... ")

    user_token = "pbkdf2:sha256:150000$nWdPlQAs$aabb00748878c7a14cf11cc52f8403a4c8f67cc5d01dfed72a909102efea2716"
    project_id = "601ce17e4b412c36f67a495e"


    # logger = Logger(user_token, project_id, "http://185.23.162.189:5000")

    # logger = Logger(user_token, None, "http://185.23.162.189:5000")

    logger = Logger(user_token, project_id)

    logger.add_project("Test upload2", "ImageClassificationa", description="This is description")


    # logger.start_run("comment", "https://gitlab.com/sprogis/dl-framework/-/commit/dd97bb13d1b95409a4129d7bff90e5c5a64a98d0")
    

    # logger.log({"msg": "starting program execution"})
    # logger.log({"msg": "test msg 1"})
    # logger.log({"msg": "finishing program execution"})


    # logger.upload_file('./captioning.py', "checkpoint")


    # results = [{"file": "image_0241.jpg", "silver": "buttercup is a flower",},
    #             {"file": "image_0242.jpg", "silver": "buttercup is a flower",},
    #             {"file": "image_0243.jpg", "silver": "bluebell is a flower",},
    #             {"file": "image_0244.jpg", "silver": "buttercup is a flower",},
    #             {"file": "image_0245.jpg", "silver": "bluebell is a flower",},
    #             {"file": "image_0246.jpg", "silver": "buttercup is a flower",},
    #             {"file": "image_0247.jpg", "silver": "bluebell is a flower",},
    #             {"file": "image_1126.jpg", "silver": "bluebell is a flower",},
    #         ]


    # logger.download_dataset("", "train")

    # logger.upload_dataset("../train", "Train")


    # results = [{"file": "Vid2.mp4", "silver": "abcded asdf asdf",},
    #             ]



    # logger.validate(results, "Train")


    # logger.finish_run()




    print ("Done")
    
    
main()
