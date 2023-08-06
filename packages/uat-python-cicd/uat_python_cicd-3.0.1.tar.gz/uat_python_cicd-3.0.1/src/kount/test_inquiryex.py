import uuid

from kount.client import Client
from kount.config import SDKConfig
from kount.inquiry import Inquiry
from kount.request import InquiryMode, MerchantAcknowledgment, CurrencyType
from kount.util.address import Address
from kount.util.cartitem import CartItem
from kount.util.payment import CardPayment
from kount.util.payment import Payment
from datetime import datetime

MERCHANT_ID = 900431
EMAIL_CLIENT = "sanjeev.kumar@intimetec.com"
SHIPPING_ADDRESS = Address("16th Main", "BTM 2nd Stage", "Bangalore", "KA", "560076", "IN")
B2A1 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
SHIPPING_ADDRESS = Address("16th Main", "BTM 2nd Stage", "Bangalore", "KA", "560076", "IN")
BILLING_ADDRESS = Address("16th Main", "BTM 2nd Stage", "Bangalore", "KA", "560076", "IN")

PTOK = "4111111111111111"
SITE_ID = "192.168.0.104"
URL_API = "https://risk.test.kount.net"
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI5MDA0MzEiLCJhdWQiOiJLb3VudC4xIiwiaWF0IjoxNTYzOTM4NjA2LCJzY3AiOnsia2EiOnRydWUsImtjIjp0cnVlLCJhcGkiOnRydWUsInJpcyI6dHJ1ZX19.WidWQkNcPeVRlBdu77cgsyQOSMRqzQHnzH3S70cnU38"
PROVIDED_CONFIGURATION_KEY = b'1b^jIFD)e1@<ZKuH"A+?Ea`p+ATAo6@:Wee+EM+(FD5Z2/N<'

USA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
SDKConfig.setup(PROVIDED_CONFIGURATION_KEY)


def generate_unique_id():

	return str(uuid.uuid4()).replace('-','').upper()

def evaluate_inquiry():
	session_id = generate_unique_id()[:32]
	inquiry = Inquiry()

	inquiry.set_merchant(MERCHANT_ID)
	inquiry.set_request_mode(InquiryMode.DEFAULT)
	inquiry.set_merchant_acknowledgment(MerchantAcknowledgment.TRUE)
	inquiry.set_website("DEFAULT")
	inquiry.set_session_id(session_id)
	# inquiry.set_request_mode("K")
	inquiry.set_unique_customer_id(session_id[:20])
	inquiry.set_ip_address(SITE_ID)
	# payment = CardPayment(PTOK, khashed=False)
	payment = Payment("CARD", PTOK, khashed=False)
	inquiry.set_billing_phone_number("4111111111111111")
	inquiry.set_shipping_phone_number("4111111111111111")
	# inquiry.payment_type("BLMLw")
	inquiry.set_shipping_name("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	inquiry.set_email_shipping("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	inquiry.set_payment(payment)
	inquiry.set_customer_name("Sanjeev Kumar")
	# cr_date = datetime(2022, 1, 1, 00, 00, 00, 00)
	inquiry.set_date_of_birth("1992-12-12")
	inquiry.set_email_client(EMAIL_CLIENT)
	inquiry.set_shipping_address(SHIPPING_ADDRESS)
	inquiry.set_billing_address(BILLING_ADDRESS)
	inquiry.set_gender("M")
	# inquiry.set_version("h")
	# inquiry.set_order_number(4111111111111111411111111111111141111111111111114111111111111111)
	inquiry.set_currency(CurrencyType.USD)
	inquiry.set_total('999999999999999')
	inquiry.set_cash("999999999999999")
	inquiry.set_unique_customer_id("41111111111111114111111111111111")
	# inquiry.set_timestamp("012345")
	inquiry.set_user_agent(USA)
	# inquiry.set_shipment_type("pp")
	# inquiry.set_authorization_status("R")
	# inquiry.set_avs_zip_reply("C")
	# inquiry.set_avs_address_reply("M")
	# inquiry.set_avs_cvv_reply("C")
	inquiry.set_website("DEFAULT")
	# inquiry.set_anid("411111111111111141111111111111114111111111111111411111111111111")
	cart_items = list()
	cart_items.append(CartItem("SHOPPING_GOODS", "SG999999", "3000 CANDLEPOWER PLASMA FLASHLIGHT", "22", "68990"))
	inquiry.set_shopping_cart(cart_items)

	client = Client(URL_API, API_KEY)
	respon = client.process(inquiry)
	print(respon)
	# for key, value in response.items():
	# 	print(key, "==>", value)

evaluate_inquiry()
