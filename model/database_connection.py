import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        # Kiểm tra xem instance đã tồn tại chưa
        if cls._instance is None:
            # Nếu chưa, tạo một instance mới và thiết lập kết nối
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._connection = mysql.connector.connect(
                    host='sql10.freesqldatabase.com',
                    port=3306,
                    user='sql10746631',
                    password='gB3ipJbu5J',
                    database='sql10746631'
                )
                print("Database connection established!")
            except Error as e:
                print(f"Error: {e}")
                cls._connection = None
        return cls._instance

    @staticmethod
    def get_connection():
        # Trả về kết nối cơ sở dữ liệu
        if DatabaseConnection._connection:
            return DatabaseConnection._connection
        else:
            raise Exception("Database connection failed!")

    def close_connection(self):
        # Đóng kết nối cơ sở dữ liệu
        if DatabaseConnection._connection:
            DatabaseConnection._connection.close()
            print("Database connection closed.")


if __name__ == '__main__':
    db = DatabaseConnection()
    try:
        connection = db.get_connection()
        print("Successfully connected to the database.")
    except Exception as e:
        print(e)