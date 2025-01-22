# for future updates not used right now kinda
# will be used for coustome querys and db

class Query:
    current_query = None
    current_query_lvl=None
    query_dict={1:"query 1",
                2:"query 2",
                3:"query 3"}

    @classmethod
    def init_query(query_lvl:int):
        global query_dict,current_query,current_query_lvl
        if query_lvl == 1:
            current_query =query_dict[1]
            current_query_lvl=1
            return None

        elif query_lvl == 2:
            current_query = query_dict[2]
            current_query_lvl=2
            return None

        elif query_lvl == 3:
            current_query = query_dict[3]
            current_query_lvl=3
            return None

        else:
            current_query = query_dict[1]
            current_query_lvl=1
            return "Error: you choose bad Query lvl will continue with lvl 1 "






    

