from gadgethiServerUtils.encryption import *
from gadgethiServerUtils.file_basics import *
from datetime import datetime
from os.path import expanduser
import time

credentials = load_config(expanduser("~") + "/.gserver/credentials.yaml")

def verify_finish_payment(intella_payment_data, **configs):
	"""
	This function verifies that the payment has been processed 
	Using dodaytest01 crypto class
	- Input:
		* intella_payment_data: Sent from Notification Payment Center
	- Output:
		* Integrity: Bool False/True
	"""
	iv =  credentials["intella_iv"].encode() 
	password = credentials["intella_password"] 
	cert_path = credentials["public_key_cert_path"]
	encryptor = GadgetEncryption(base64.b64encode(os.urandom(16)), iv, cert_path)

	try:
		Sign = intella_payment_data["Sign"]
		print ("Sign from intella = ",Sign)
		if Sign == "admin":
			return True
	except:
		pass
		
	if encryptor.verify(intella_payment_data):
		return True
	else:
		return False


def post_to_Intella(order_data, number_of_data, **server_config):
	"""
	This function posts the order info to intella service and gets a url
	- Input:
		* order_data: dictionary of data
	- Return:
		* url: url of payment info
	"""
	StoreOrderNo = order_data['order_id']
	Body = str(order_data['serial_number'])
	TotalFee = str(order_data['total_price'])
	"""
	Only for AWS
	"""
	if server_config["server_location"] == "AWS":
		shift_timezone = int(server_config["time_zone"])
	elif server_config["server_location"] == "local":	
		shift_timezone = 0

	cTime = int(datetime.now().timestamp()) + (shift_timezone*60*60)
	time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(cTime))

	iv =  credentials["intella_iv"].encode() 
	cert_path = credentials["public_key_cert_path"]
	encryptor = GadgetEncryption(base64.b64encode(os.urandom(16)), iv, cert_path)

	password = credentials["intella_password"] 
	tradekey = encryptor.sha256encrypt_string(password)

	data_info = {"DeviceInfo":"skb0001","StoreOrderNo":StoreOrderNo,"Body":"訂單"+str(Body),"TotalFee":TotalFee,"CallBackUrl":"http://order.doday.com.tw/success_page.html","Delay":"3"}

	test_data ={
	  "Header": {
		"Method": "00000",
		"ServiceType":"OLPay",
		"MchId": credentials["doday_mchid"],
		"TradeKey": tradekey,
		"CreateTime": time_str
	  },
		"Data": json.dumps(data_info)
	}	

	payload = str(encryptor.generateRequestDict(test_data))
	payload.replace("\'","\"")

	payload = ast.literal_eval(payload)

	intella_response = (encryptor.client_post("https://a.intella.co/allpaypass/api/general", payload))
	intella_response = ast.literal_eval(intella_response)

	intella_response = encryptor.decodeIntellaResponse(intella_response)
	intella_response = ast.literal_eval(intella_response)

	return intella_response


def post_to_blue(order_data):
	
	test_string = {'MerchantID':order_data['MerchantID'],'RespondType':'JSON','TimeStamp':order_data['time'],'Version':1.5,'MerchantOrderNo':order_data['MerchantOrderNo'],'Amt':order_data['Amt'],'ItemDesc':order_data['ItemDesc'],'Email':order_data['Email'],'LoginType':0,'ANDROIDPAY':0}
	
	# iv and key position
	iv = credentials["blue_iv"].encode()
	key = credentials["blue_key"].encode()

	# str iv,key
	str_iv = credentials["blue_iv"]
	str_key = credentials["blue_key"]

	encryptor = GadgetEncryption(key,iv,AES_decode_mode='hex')
	urlencode_data = urlencode(test_string)
	string = encryptor.encrypt_AES(urlencode_data)

	SHA256_string = 'HashKey='+str_key+'&'+string+'&HashIV='+str_iv

	SHA = encryptor.hashFunction(SHA256_string)
	SHA = str.upper(SHA)

	decode_string = encryptor.decrypt_AES(string)

	return string,SHA

def poll_multiple_orders(interval, **server_config):
	"""
	This function uses the Intella multiple order polling.

	Request should be 

	{
	  "Header": {
		"Method": "00000",
		"ServiceType": "OrderQuery",
		"MchId": "myMchId",
		"TradeKey": "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0",
		"CreateTime": "20180715105349"
	  },
	  "Data": "{\"StartDate\":\"20180715\",\"EndDate\":\"20180716\",\"OrderStatus\":\"1\"}"
	}
	
	Response may be 

	{
	  "Header": {
		"StatusCode": "0000",
		"StatusDesc": "執行成功",
		"Method": "00000",
		"ServiceType": "OrderQuery",
		"MchId": "myMchId"
	  },
	  "Data": {
		"DataValue": [
		  {
			"StoreOrderNo": "PO-20180715-004",
			"SysOrderNo": "104605",
			"TotalFee": 10,
			"FeeType": "TWD",
			"Status": "Trade success",
			"Description": "-7082",
			"Method": "11500"
		  },
		  {
			"StoreOrderNo": "PO-20180715-005",
			"SysOrderNo": "104644",
			"TotalFee": 10,
			"FeeType": "TWD",
			"Status": "Trade success",
			"RefundStatus": "Refund success",
			"Description": "Chicken Rice-0247",
			"Method": "31800"
		  }
		]
	  }
	}

	"""
	if server_config["server_location"] == "AWS":
		shift_timezone = int(server_config["time_zone"])
	elif server_config["server_location"] == "local":	
		shift_timezone = 0

	cTime = int(datetime.now().timestamp()) + (shift_timezone*60*60)
	start_time = int(cTime - interval)
	print("Current time = ",time.strftime("%Y%m%d%H%M%S", time.localtime(cTime)))
	current_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(cTime))
	start_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))
	print ("Start time = ",start_time_str)

	iv =  credentials["intella_iv"].encode() 
	cert_path = credentials["public_key_cert_path"]
	encryptor = GadgetEncryption(base64.b64encode(os.urandom(16)), iv, cert_path)
	
	password = credentials["intella_password"] 
	tradekey = encryptor.sha256encrypt_string(password)

	data_info = {"StartDate":start_time_str,"EndDate":current_time_str,"OrderStatus":"1"}
	test_data ={
	  "Header": {
		"Method": "00000",
		"ServiceType":"OrderQuery",
		"MchId": credentials["doday_mchid"],
		"TradeKey": tradekey,
		"CreateTime": current_time_str
	  },
		"Data": json.dumps(data_info)
	}	

	payload = str(encryptor.generateRequestDict(test_data))
	payload.replace("\'","\"")

	payload = ast.literal_eval(payload)

	intella_response = (encryptor.client_post("https://a.intella.co/allpaypass/api/general", payload))
	intella_response = ast.literal_eval(intella_response)

	intella_response = encryptor.decodeIntellaResponse(intella_response)
	intella_response = ast.literal_eval(intella_response)
	return intella_response





