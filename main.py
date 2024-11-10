from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from dao.shop_dao import ShopDAO
from model.shop import Shop

app = Flask(__name__)
CORS(app)
customer_in_store = 0
is_close = False


# kiểm tra kết nối đến server
@app.route("/")
def home():
    return render_template("index.html")


# đẩy dữ liệu số lượng khách trong cửa hàng
@app.route("/send/customer_in_store", methods=["POST"])
def set_customer_in_store():
    global customer_in_store
    try:
        customer_in_store = int(request.values.get('customer_in_store'))
        return jsonify({"success": "Send successful.", "customer_in_store": customer_in_store})
    except ValueError:
        return jsonify({"error": "Wrong type of data."})


# lấy dữ liệu số lượng khách trong cửa hàng để hiển thị biểu đồ
@app.route("/get/customer_in_store")
def get_customer_in_store():
    return jsonify({"customer_in_store": customer_in_store})


# đẩy dữ liệu số lượng khách vào/ra cửa hàng
@app.route("/send/shop_info", methods=["POST"])
def add_shop_info():
    try:
        customers_entering = int(request.values.get('customers_entering'))
        customers_exiting = int(request.values.get('customers_exiting'))
        shop = Shop(customers_entering, customers_exiting)
        is_success = ShopDAO.add_info(shop)
        if is_success:
            return jsonify({"success": "Add successful."})
        else:
            return jsonify({"error": "Something was an error."})
    except ValueError:
        return jsonify({"error": "Wrong type of data."})


# lấy dữ liệu số lượng khách vào/ra cửa hàng để hiển thị biểu đồ
@app.route("/get/shop_info/", methods=["POST"])
def get_shop_info():
    date = request.values.get('date')  # date dạng yyyy-mm-dd
    time_mark = request.values.get('time_mark')
    result = None
    if date != 'null' and time_mark != 'null':
        result = ShopDAO.get_info_by_date_and_time(date, time_mark)
    elif date != 'null' and time_mark == 'null':
        result = ShopDAO.get_info_by_date(date)
    else:
        result = ShopDAO.get_all_info()

    return jsonify({"success": "Get data successful.", "result": result})


# gửi trạng thái đóng/mở cửa hàng đến server
@app.route("/send/store_open")
def set_store_open():
    global is_close
    is_close = False
    return jsonify({"success": "Send successful."})


@app.route("/send/store_close")
def set_store_close():
    global is_close
    is_close = True
    return jsonify({"success": "Send successful."})


# nhận trạng thái cửa hàng
@app.route("/get/store_state")
def get_store_state():
    return jsonify({"is_close": is_close})


if __name__ == "__main__":
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000
    )

