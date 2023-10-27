import json
from os import environ as env
import boto3
import pymysql
from pymysql.cursors import DictCursor


def get_db_cursor():
    sm = boto3.client("secretsmanager")
    secret = sm.get_secret_value(SecretId=env["DB_SECRET_NAME"])
    dbcreds = json.loads(secret["SecretString"])
    db_user = dbcreds.get("username")
    db_pass = dbcreds.get("password")
    db_name = dbcreds.get("dbname")
    db_host = dbcreds.get("host")
    db_port = dbcreds.get("port")

    if not (db_user and db_pass and db_name and db_host and db_port):
        raise Exception("Missing required database parameters in environment")

    connection = pymysql.connect(
        user=db_user,
        passwd=db_pass,
        db=db_name,
        host=db_host,
        port=db_port,
        cursorclass=DictCursor,
    )

    return connection.cursor()


def crete_database_employeetable():
    """id emplyee,counter and database doesnot exist crete the schama"""
    try:
        db = get_db_cursor()
        print("db", db)
        database_schame ="""CREATE DATABASE IF NOT EXISTS employee  """
        db.execute(database_schame)
        db.connection.commit()
        
        emplyees_schame =""" CREATE TABLE IF NOT EXISTS employee.employees (
            regid VARCHAR(30) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            phoneNo VARCHAR(20),
            addressDetails JSON,
            workExperience JSON,
            qualifications JSON,
            projects JSON,
            photo LONGBLOB
        );
        """
        db.execute(emplyees_schame)
        db.connection.commit()

        counter_schame =""" CREATE TABLE IF NOT EXISTS employee.sequence (
                name VARCHAR(30) PRIMARY KEY,
                value INT NOT NULL
            ); """
        db.execute(counter_schame)
        db.connection.commit()

        return 200, {"message":"If resources doentexist create schema was successfull", "success":"true"}

    except Exception as e:
        print("error",e)
        return 500, {"message": "unbale to connect to mysql","success":"false"}




def Validate_Filed_Names(data, schema):
    """validating input fileds entered currectly or not"""
    errors = []
    try:
        for key, expected_type in schema.items():
            if key not in data:
                if "_schema" in key:
                    if key.replace("_schema","") not in data[key.replace("_schema","")]  :
                        if isinstance(data[key.replace("_schema","")], dict) :
                            invalid_fileds = set(data[key.replace("_schema","")].keys()).difference(set(schema[key].keys()))
                            if invalid_fileds:
                                errors.append(f"Validation Error: Field '{invalid_fileds}' is missing in the data")
                            missing =set(schema[key].keys()).difference(set(data[key.replace("_schema","")].keys()))
                            if missing:
                                errors.append(f"Validation Error:Invalid Field '{invalid_fileds}' is entered in the '{key.replace('_schema','')}'")
                            
                            
                        if isinstance(data[key.replace("_schema","")], list) :
                            for i in data[key.replace("_schema","")]:
                                missing = set(schema[key].keys()).difference(set(i.keys()))
                                if missing:
                                    errors.append(f"Validation Error: Field '{missing}' is missing in the '{key.replace('_schema','')}'")
                                invalid_fileds = set(i.keys()).difference(set(schema[key].keys()))
                                if invalid_fileds:
                                    errors.append(f"Validation Error:Invalid Field '{invalid_fileds}' is entered in the '{key.replace('_schema','')}'")
                else:
                    errors.append( f"Validation Error: Field '{key}' is missing in the data.")
        invaild_str_fileds = set(data.keys()).difference(set(schema.keys())) 
        if invaild_str_fileds:
            errors.append(f"Validation Error:Invalid Field '{invaild_str_fileds}' is entered in the data")
        return 400 if errors else 200 , {"errors":errors}
    except Exception as e:
        print("dfdg",e)
        return 500, {"errors":f"Error occured while validateing input fields" }
        
        
def Validate_Field_Types(data, schema):
    """validating the ype of entered fileds are type is valid or not """
    try:
        errors = []
        # Check if all keys in the schema are present in the data
        for key, expected_type in schema.items():
            print("key", key)
            # validationg keys
            if key in data:
                value = data[key]
                if expected_type == dict:
                    if not isinstance(value, dict):
                        errors.append( f"Validation Error: Field '{key}' should be a dictionary.")
                    inner_schema = schema[key + "_schema"]
                    validation_code, errors1 = Validate_Field_Types(value, inner_schema)
                    if validation_code != 200:
                        errors.append(errors1["errors"])
                elif expected_type == list:
                    if not isinstance(value, list):
                        errors.append( f"Validation Error: Field '{key}' should be a list.")
                    inner_schema = schema[key + "_schema"]
                    for item in value:
                        validation_code, errors1 = Validate_Field_Types(item, inner_schema)
                        if validation_code != 200:
                            errors.append(errors1["errors"])
                elif not isinstance(value, expected_type):
                    errors.append( f"Validation Error: Field '{key}' should be of type {expected_type.__name__}")

        return 400 if errors else 200, {"errors":errors}  # No validation errors
    except Exception as e:
        print("fdg",e)
        return 500, {"errors":f"Error occured while validating type"}


schema = {
    "name": str,
    "email": str,
    "age": int,
    "gender": str,
    "phoneNo": str,
    "addressDetails": dict,
    "addressDetails_schema": {
        "hno": str,
        "street": str,
        "city": str,
        "state": str,
    },
    "workExperience": list,
    "workExperience_schema": {
        "companyName": str,
        "fromDate": str,
        "toDate": str,
        "address": str,
    },
    "qualifications": list,
    "qualifications_schema": {
        "qualificationName": str,
        "fromDate": str,
        "toDate": str,
        "percentage": (int, float),
    },
    "projects": list,
    "projects_schema": {
        "title": str,
        "description": str,
    },
    "photo": str
}


from .create import Post_Handler as create
from .delete import Delete_Handler as delete
from .read import Get_Handler as read
from .update import Put_Handler as update
