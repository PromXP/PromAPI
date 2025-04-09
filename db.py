from motor import motor_asyncio
import logging
import asyncio

# MongoDB setup
client = motor_asyncio.AsyncIOMotorClient("mongodb+srv://admpromxp:admpromxp@promcluster.w2kxjjn.mongodb.net/?retryWrites=true&w=majority&appName=promcluster")
database = client.Main
admin_lobby = database.Admin_Lobby 
doctor_lobby = database.Doctor_Lobby 
patient_data = database.Patient_Data
notification_data = database.Notification_Data

def fix_mongo_id(document):
    if document is None:
        return document
    document["_id"] = str(document["_id"])
    return document


async def keep_server_alive():
    while True:
        logging.info("🔁 Tick: Server is alive.")
        await asyncio.sleep(105)  # 1 minute 45 seconds = 105 seconds

def update_questionnaire_completion(uhid: str, name: str, period: str, completed: int = 1):
    filter_query = {
        "uhid": uhid,
        "questionnaire_assigned": {
            "$elemMatch": {
                "name": name,
                "period": period
            }
        }
    }

    update_query = {
        "$set": {
            "questionnaire_assigned.$.completed": completed
        }
    }

    result = patient_data.update_one(filter_query, update_query)
    return result
