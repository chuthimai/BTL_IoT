from dao.shop_statistics_dao import ShopStatisticsDAO
from model.database_connection import DatabaseConnection
from model.shop import Shop


def get_cursor():
    database = DatabaseConnection()
    conn = database.get_connection()
    return conn.cursor(dictionary=True), conn


class ShopDAO:
    @classmethod
    def get_all_info(cls):
        cursor, conn = get_cursor()
        try:
            query = "SELECT * FROM shop"
            cursor.execute(query)
            results = cursor.fetchall()
            # Đóng gói dữ liệu vào list các object Shop
            shops = []
            for row in results:
                shop = Shop(row['customers_entering'], row['customers_exiting'])
                shop.set_date(row['date'].strftime('%Y-%m-%d'))
                hours, remainder = divmod(row['time'].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                shop.set_time(f"{hours:02}:{minutes:02}:{seconds:02}")
                shops.append(shop.to_dict())
            return shops
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def add_info(cls, shop: Shop) -> bool:
        cursor, conn = get_cursor()
        try:
            query = '''INSERT INTO shop (customers_entering, customers_exiting, `time`, `date`)
                        VALUES (%s, %s, TIME(NOW()), DATE(NOW()))'''
            cursor.execute(query, (shop.customers_entering, shop.customers_exiting))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def get_info_by_date_and_time(cls, date: str, time_mark: str):
        cursor, conn = get_cursor()
        time_from = None
        time_to = None

        if time_mark == '1':
            time_from = "06:00:00"
            time_to = "12:00:00"
        elif time_mark == '2':
            time_from = "12:00:00"
            time_to = "18:00:00"
        elif time_mark == '3':
            time_from = "18:00:00"
            time_to = "23:59:59"

        try:
            # Câu lệnh SQL để lấy dữ liệu theo date và time
            query = '''SELECT * FROM shop
                           WHERE `date` = %s AND `time` BETWEEN %s AND %s'''

            cursor.execute(query, (date, time_from, time_to))
            results = cursor.fetchall()

            # Đóng gói dữ liệu vào list các object Shop
            shops = []
            for row in results:
                shop = Shop(row['customers_entering'], row['customers_exiting'])
                shop.set_date(row['date'].strftime('%Y-%m-%d'))
                hours, remainder = divmod(row['time'].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                shop.set_time(f"{hours:02}:{minutes:02}:{seconds:02}")
                shops.append(shop.to_dict())

            return shops  # Trả về danh sách các Shop
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def get_info_by_date(cls, date: str):
        cursor, conn = get_cursor()
        try:
            # Câu lệnh SQL để lấy dữ liệu theo date và time
            query = '''SELECT * FROM shop
                               WHERE `date` = %s'''
            cursor.execute(query, (date,))
            results = cursor.fetchall()

            # Đóng gói dữ liệu vào list các object Shop
            shops = []
            for row in results:
                shop = Shop(row['customers_entering'], row['customers_exiting'])
                shop.set_date(row['date'].strftime('%Y-%m-%d'))
                hours, remainder = divmod(row['time'].seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                shop.set_time(f"{hours:02}:{minutes:02}:{seconds:02}")
                shops.append(shop.to_dict())

            return shops  # Trả về danh sách các Shop
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def get_info_by_day_month_year(cls, day: int, month: int, year: int):
        cursor, conn = get_cursor()
        try:
            # Câu lệnh SQL để lấy dữ liệu theo time
            if day is not None and month is not None and year is not None:
                return ShopStatisticsDAO.statistics_by_hour(cursor, day, month, year)
            elif month is not None and year is not None:
                return ShopStatisticsDAO.statistics_by_day(cursor, month, year)
            elif year is not None:
                return ShopStatisticsDAO.statistics_by_month(cursor, year)
            else:
                return ShopStatisticsDAO.statistics_by_year(cursor)
        except Exception as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            cursor.close()

