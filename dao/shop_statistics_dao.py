from mysql.connector.cursor import MySQLCursorDict


class ShopStatisticsDAO:
    @staticmethod
    def statistics_by_hour(cursor: MySQLCursorDict, day: int, month: int, year: int):
        query = '''
        SELECT 
            HOUR(time) AS hour,
            SUM(customers_entering) AS total_customers_entering,
            SUM(customers_exiting) AS total_customers_exiting
        FROM shop
        WHERE DAY(date) = %s AND MONTH(date) = %s AND YEAR(date) = %s
        GROUP BY HOUR(time)
        ORDER BY hour
        '''
        cursor.execute(query, (day, month, year))
        results = cursor.fetchall()
        return [{
            "hour": str(row['hour']) + ":00",
            "total_customers_entering": row['total_customers_entering'],
            "total_customers_exiting": row['total_customers_exiting']
        } for row in results]

    @staticmethod
    def statistics_by_day(cursor: MySQLCursorDict, month: int, year: int):
        query = '''
                SELECT 
                    DAY(date) AS day,
                    SUM(customers_entering) AS total_customers_entering,
                    SUM(customers_exiting) AS total_customers_exiting
                FROM shop
                WHERE MONTH(date) = %s AND YEAR(date) = %s
                GROUP BY DAY(date)
                ORDER BY day
                '''
        cursor.execute(query, (month, year))
        results = cursor.fetchall()
        return [{
            "day": row['day'],
            "total_customers_entering": row['total_customers_entering'],
            "total_customers_exiting": row['total_customers_exiting']
        } for row in results]

    @staticmethod
    def statistics_by_month(cursor: MySQLCursorDict, year: int):
        query = '''
                SELECT 
                    MONTH(date) AS month,
                    SUM(customers_entering) AS total_customers_entering,
                    SUM(customers_exiting) AS total_customers_exiting
                FROM shop
                WHERE YEAR(date) = %s
                GROUP BY MONTH(date)
                ORDER BY month
                '''
        cursor.execute(query, (year,))
        results = cursor.fetchall()
        months = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jan", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return [{
            "month": months[row['month']],
            "total_customers_entering": row['total_customers_entering'],
            "total_customers_exiting": row['total_customers_exiting']
        } for row in results]

    @staticmethod
    def statistics_by_year(cursor: MySQLCursorDict):
        query = '''
                SELECT 
                    YEAR(date) AS year,
                    SUM(customers_entering) AS total_customers_entering,
                    SUM(customers_exiting) AS total_customers_exiting
                FROM shop
                GROUP BY YEAR(date)
                ORDER BY year
                '''
        cursor.execute(query)
        results = cursor.fetchall()
        return [{
            "year": row['year'],
            "total_customers_entering": row['total_customers_entering'],
            "total_customers_exiting": row['total_customers_exiting']
        } for row in results]
