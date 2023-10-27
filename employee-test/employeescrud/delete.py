from io import StringIO
from . import get_db_cursor
import json

def Delete_Handler(query):
    try:
        print("databefore",type(query), query)
        data_st= query.replace("\n", "")
        data_st= data_st.replace("\n", "")
        query = json.loads(data_st)
    except Exception as e:
        return 500, {"message":f"Invalid json format", "success":"false"}
    try:
        print(query, type(query))
        db = get_db_cursor()
        print("db",db)
        if query and  "regid" in query:
            search_regid = query['regid']
            query = "DELETE FROM employee.employees WHERE regid = %s"
            # Execute the query with the search parameter
            db.execute(query, (search_regid,))
            # Fetch the result
            result = db.fetchall()
            print("result",result)
            if db.rowcount > 0:
                message ="Record deleted successfully."
                return 200, {"message":message, "success":"true"}
            else:
                message ="No matching record found."
                return 404, {"message": message , "success":"true"}
        else:
            return 404, {"message": "regid was not given to delete" , "success":"true"}


    except Exception as e:
        return 500, {"message":f"{e}","success":"false"}
