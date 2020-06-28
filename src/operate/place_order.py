from ib.opt import Connection, message
from ib.lib import Integer, StringBuffer
from ib.ext.Contract import Contract
from ib.ext.Order import Order
import time
import collections

ib_conn = None
oid = 0
OrderInfo = collections.namedtuple('OrderInfo',['action','quantity']) 
  

def get_valid_order_id(msg):    
	# print("msg for reqIds(): ", msg)
	global oid
	oid = msg.orderId


def error_handler(msg):    
    print ("Server Error:", msg)


def operate(ticker, action, quantity, price=None):
	# Contract
	contract = Contract()
	contract.m_symbol = ticker
	contract.m_secType = 'STK'  #
	contract.m_exchange = 'ISLAND'  #SMART, ISLAND
	# contract.m_primaryExch = 'ISLAND'
	contract.m_currency = 'USD'

	# Order
	order = Order()
	if price is not None:
		order.m_orderType = 'LMT'
		order.m_lmtPrice = price
	else:
		order.m_orderType = 'MKT'
	order.m_totalQuantity = quantity
	order.m_action = action

	return contract, order


def place_orders(orders):
	default_port = 7497
	default_client_id = 999

	for ticker, order_info in orders.items():
		# Step 1. Establish Connection
		ib_conn = Connection.create(
			port=default_port, 
			clientId=default_client_id
			)
		status = ib_conn.connect()
		print("Connection status: ", status)


		ib_conn.register(get_valid_order_id, message.nextValidId) 
		ib_conn.register(error_handler, message.Error) 

		ib_conn.reqIds(1)

		# Wait until the registered function finished
		time.sleep(2)

		# Step 2. Get the contract
		contract, order = operate(
			ticker=ticker, 
			action=order_info.action, 
			quantity=order_info.quantity
			)

		# Place the order
		print("Placing the order")
		# oid = 110
		orderId = oid
		print("Now order id is: ", orderId)
		ib_conn.placeOrder(orderId, contract, order)

		# Add some latency to ensure order placed
		time.sleep(20)

		print("Placed the order.")

		# Step 3. Disconnect from workstation
		ib_conn.disconnect()


if __name__ == "__main__":
	orders = {}
	orders['TSLA'] = OrderInfo('BUY', 299)
	orders['AAPL'] = OrderInfo('BUY', 399)
	place_orders(orders)

