from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
import time

ibConnection = None


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


cid = 109

def handlAll(msg):
	print(msg)

if __name__ == "__main__":
	# Step 1. Establish Connection
	ibConnection = Connection.create(port=7497, clientId=999)
	status = ibConnection.connect()

	print(status)
	oid = cid
	# Step 2. Buy 123 NVDA
	contract, order = operate(ticker='TSLA', action='BUY', quantity=239)

	# Place the order
	print("Placing the order")
	# breakpoint()
	orderId = oid
	order_status = ibConnection.placeOrder(orderId, contract, order)
	print("Order status: ", order_status)

	# while 1:
	time.sleep(20)

	print("Placed the order.")

	# Step 3. Disconnect from workstation
	# ibConnection.disconnect()

