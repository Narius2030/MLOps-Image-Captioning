class QueryTemplate:
    def __init__(self, table_name, schema=None):
        self.table_name = table_name
        self.schema = schema
    
    def create_query_select(self, columns, latest_time):
        if not columns:
            column_str = "*"
        else:
            column_str = ", ".join(columns)
        
        query = f"""
            SELECT {column_str} 
            FROM {self.table_name}
            WHERE created_time > TIMESTAMP '{latest_time}'
        """
        return query
    
    def create_query_upsert(self, columns, conflict_columns, arrjson_column):
        self.columns = ""
        self.values = ""
        self.odku = ""

        end_col = columns[-1]
        conflict_columns = ','.join([f'"{col}"' for col in conflict_columns])
        for col in columns:
            if col == end_col:
                self.columns += f'"{col}"'
                self.values += ":" + col
                self.odku += f'"{col}"' + "=" + "EXCLUDED." + f'"{col}"' 
            else:
                self.columns += f'"{col}"' + ", "
                self.values += ":" + col + ", "
                self.odku += f'"{col}"' + "=" + "EXCLUDED." + f'"{col}"' + ","

        create_query = \
            f"INSERT INTO {self.schema}.{self.table_name}" + \
            f" ({self.columns}) " + \
            f"VALUES ({self.values}) " + \
            f"ON CONFLICT (" + conflict_columns + ") " + \
            f"DO UPDATE SET {self.odku}"
        return create_query
    
    def create_query_insert(self, columns, arrjson_column):
        self.columns = ""
        self.values = ""
        self.odku = ""

        end_col = columns[-1]
        for col in columns:
            if col == end_col:
                self.columns += f'"{col}"' + f''
                self.values += "?"
                self.odku += f'"{col}"' + "=" + "EXCLUDED." + f'"{col}"'
            else:
                self.columns += f'"{col}"' + ", "
                self.values += "?, "
                self.odku += f'"{col}"' + "=" + "EXCLUDED." + f'"{col}"' + ","
        
        if self.schema is None:
            create_query =  f"INSERT INTO {self.table_name}"
        else:
            create_query = f"INSERT INTO {self.schema}.{self.table_name}"
        
        create_query += f"({self.columns}) VALUES ({self.values})"
        return create_query
    
    def create_query_update(self, columns, where_columns, arrjson_column):
        # Khởi tạo các chuỗi cần thiết cho câu lệnh UPDATE
        set_clause = ""
        where_clause = ""
        
        # Định dạng các cột cần UPDATE
        end_col = columns[-1]
        for col in columns:
            if col == end_col:
                set_clause += f'"{col}" = :{col}'
            else:
                set_clause += f'"{col}" = :{col}, '

        # Định dạng các cột trong mệnh đề WHERE
        end_where_col = where_columns[-1]
        for col in where_columns:
            if col == end_where_col:
                where_clause += f'"{col}" = :{col}'
            else:
                where_clause += f'"{col}" = :{col} AND '
        
        update_query = \
            f"UPDATE {self.schema}.{self.table_name} " + \
            f"SET {set_clause} " + \
            f"WHERE {where_clause}"
            
        return update_query
