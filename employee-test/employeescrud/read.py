from io import StringIO
from . import get_db_cursor
import json

def Get_Handler(query):
    try:
        print(query, type(query))
        db = get_db_cursor()
        print("db",db)
        if query and  "regid" in query:
            search_regid = query['regid']
            query = "SELECT * FROM employee.employees WHERE regid = %s"
            
            # Execute the query with the search parameter
            db.execute(query, (search_regid,))
            # Fetch the result
            result = db.fetchall()
            print("result",result)
            if result:
                return 200, {"message": str(result) if result else result, "success":"true"}
            else:
                return 404, {"message":f"No record found for {search_regid}", "success":"false"}
        else:
            print("else")
            db.execute("""select * from employee.employees;""")
            result = db.fetchall()
            print("resdedf", result)
            if result:
                return 200, {"message":str(result),"success":"true", "query":query}
            else:
                return 404, {"message":"records not avalible", "success":"true"}


    except Exception as e:
        return 500, {"message":f"{e}","success":"false"}
