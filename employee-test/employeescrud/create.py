from . import get_db_cursor, Validate_Filed_Names, Validate_Field_Types, schema
import json
import pymysql
from pymysql.cursors import DictCursor



# Validate the field types and key presence
def Post_Handler(data):
    try:
        print("databefore",type(data), data)
        data_st= data.replace("\n", "")
        data= json.loads(data_st)
    except Exception as e:
        return 500, {"message":f"Invalid json format", "success":"false"}
    
    try:
        error=[]
        validationstatus1,errors1 = Validate_Filed_Names(data, schema)
        validationstatus2, errors2 = Validate_Field_Types(data, schema)
        print(validationstatus1,errors1)
        print(validationstatus2,errors2)
        if validationstatus1 != 200 or validationstatus2 != 200 :
            error.append(errors2)
            error.append(errors1)
            return 400, {"message": error, "success":"false"}
        db = get_db_cursor()
        print("db",db)
        db.execute("SELECT value FROM employee.sequence WHERE name = 'EMP'")
        next_value = db.fetchone()["value"]
        print("next_value", next_value)


        formatted_number = "{:03d}".format(next_value)
        print(formatted_number)
        
        # Generate the 'regid' manually
        regid = f"EMP:{formatted_number}"
        print("regid", regid)
        db.execute(
            """
            INSERT INTO employee.employees (regid, name, email, age, gender, phoneNo, addressDetails, workExperience, qualifications, projects, photo)
            VALUES (%(regid)s,%(name)s, %(email)s, %(age)s, %(gender)s, %(phoneNo)s, %(addressDetails)s, %(workExperience)s, %(qualifications)s, %(projects)s, %(photo)s)
            """,
            {   
                'regid': regid,
                'name': data['name'],
                'email': data['email'],
                'age': data['age'],
                'gender': data['gender'],
                'phoneNo': data['phoneNo'],
                'addressDetails': json.dumps(data['addressDetails']),
                'workExperience': json.dumps(data['workExperience']),
                'qualifications': json.dumps(data['qualifications']),
                'projects': json.dumps(data['projects']),
                'photo': data['photo']
            }
        )
        db.connection.commit()
        print("data inserted")
        db.execute("UPDATE employee.sequence SET value = value + 1 WHERE name = 'EMP'")
        db.connection.commit()
        print("dataupdated")
        return 200, {"message":"employee created successfully", "regid":f"{regid}", "success":"true"}
    except pymysql.err.IntegrityError as e:
        return 409, {"message": f"employe details already exists with same mailid or regid", "success":"false"}
    except Exception as e:
        print("eeore", e)
        return 500, {"message":f"{e}", "success":"false"}
        
