import json
from . import get_db_cursor, Validate_Filed_Names, Validate_Field_Types, schema
import re


def validate_regid(regid):
    """validation for regid field matching regular expression pattern"""
    pattern = r'^EMP:\d{3}$'
    if re.match(pattern, regid):
        return True
    else:
        return False
        
        
def Field_Validation_For_Updated(data):
    """checking validation for field of update method"""
    error = []
    if "regid" in data:
        regid = data.pop("regid")
        if type(regid) != str :
            error.append("field 'regid' should be string")
        else:
            error.append("regid is not following the pattern r'^EMP:\d{3}$'") if not validate_regid(regid) else ""
    else: 
        error.append("field 'regid' should be present")
    validationstatus1,errors1 = Validate_Filed_Names(data, schema)
    validationstatus2, errors2 = Validate_Field_Types(data, schema)
    print(validationstatus1,errors1)
    print(validationstatus2,errors2)
    if validationstatus1 != 200 or validationstatus2 != 200 or len(error)!=0 :
        error.append(errors2) if errors2 else ""
        error.append(errors1) if errors1 else ""
        return 400, error
    return 200, error 
    
    
def Put_Handler(data):
    "perform put operation on employyes table"
    try:
        print("databefore", type(data), data)
        data_st= data.replace("\n", "")
        data_st= data_st.replace("\r", "")
        data= json.loads(data_st)
    except Exception as e:
        print(e)
        return 500, {"message":f"{e}error occurred while formating jsonupdate", "success":"false"}
    try:
        new_data = data
        statuscode, error = Field_Validation_For_Updated(data) 
        if statuscode !=200 or len(error) != 0:
            return 400, {"message": f"error in the requestbody {error}", "success":"false"}
        print("data54",data)
        if data and  "regid" in data:
            search_regid = data['regid']
            query = "SELECT * FROM employee.employees WHERE regid = %s"
            # Execute the query with the search parameter
            db.execute(query, (search_regid,))
            # Fetch the result
            result = db.fetchall()
            print("result",result)
            if not result:
                return 404, {"message":"No record found for {search_regid}", "success":"false"}
        new_data['addressDetails'] = json.dumps(new_data['addressDetails'])
        new_data['workExperience'] = json.dumps(new_data['workExperience'])
        new_data['qualifications'] = json.dumps(new_data['qualifications'])
        new_data['projects'] = json.dumps(new_data['projects'])

        db = get_db_cursor()
        update_query = """
            UPDATE employees
            SET 
                name = %(name)s,
                email = %(email)s,
                age = %(age)s,
                gender = %(gender)s,
                phoneNo = %(phoneNo)s,
                addressDetails = %(addressDetails)s,
                workExperience = %(workExperience)s,
                qualifications = %(qualifications)s,
                projects = %(projects)s,
                photo = %(photo)s
            WHERE regid = %(regid)s
            """
        db.execute(update_query, new_data)
        db.commit()
        return 200, {"success":"true", "message": "successfully update the record"}
    except Exception as e:
        print("wertyh",e)
        return 500, {"success":"false", "message": "error occured during updation of record"}
    

            