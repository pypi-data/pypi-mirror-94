from requests import Session, HTTPError
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.exceptions import Fault
from zeep.helpers import serialize_object


class NavSoapClient():

    def __init__(self, nav_user, nav_password, nav_soap_service, nav_company): 
        self.nav_user = nav_user
        self.nav_password = nav_password
        self.nav_soap_service = nav_soap_service
        self.nav_company = nav_company


    def read_multiple_soap_records(self, soap_object, filter_field_string, filter_type_string, filter_data=[{'property': '', 'value': ''}]):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + self.nav_company + "/Page/" + soap_object
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        filter_field = client.get_type(f"ns0:{filter_field_string}")
        filter_type = client.get_type(f"ns0:{filter_type_string}")

        # Build the search filters from the filter_data
        # Notice the default values for the filter_data arguement are empty
        # so we bring back all of the records as a default
        filters = [filter_type(filter_field(item['property']), item['value'])
                for item in filter_data]

        # setService tells the service how many records to return
        soap_response = client.service.ReadMultiple(filter=filters, setSize=0)

        serialized_response = serialize_object(soap_response)
        return serialized_response


    def create_soap_record(self, soap_object, data):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + \
            self.nav_company + "/Page/" + soap_object
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        complex_type = client.get_type(f"ns0:{soap_object}")
        record = complex_type(**data)

        soap_response = client.service.Create(record)

        serialized_response = serialize_object(soap_response)
        return serialized_response


    def update_soap_record(self, soap_object, data):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + \
            self.nav_company + '/Page/' + soap_object
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        complex_type = client.get_type(f'ns0:{soap_object}')
        record = complex_type(**data)

        soap_response = client.service.Update(record)

        serialized_response = serialize_object(soap_response)
        return serialized_response


    def delete_soap_record(self, soap_object, record_key):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + \
            self.nav_company + "/Page/" + soap_object
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        soap_response = client.service.Delete(record_key)

        serialized_response = serialize_object(soap_response)
        return serialized_response


    def refresh_prod_order(self, prod_order_status, prod_order_no):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + \
            self.nav_company + "/Codeunit/MfgFunctionsWS"
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        soap_response = client.service.RefreshProdOrder(
            prodOrderStatus=prod_order_status, prodOrderNo=prod_order_no)

        serialized_response = serialize_object(soap_response)
        return serialized_response


    def release_prod_order(self, prod_order_status, prod_order_no):
        session = Session()
        session.auth = HTTPBasicAuth(self.nav_user, self.nav_password)

        soap_service_url = self.nav_soap_service + \
            self.nav_company + "/Codeunit/MfgFunctionsWS"
        client = Client(soap_service_url, transport=Transport(
            session=session, cache=SqliteCache()))

        soap_response = client.service.ReleaseProdOrder(
            prodOrderStatus=prod_order_status, prodOrderNo=prod_order_no)

        serialized_response = serialize_object(soap_response)
        return serialized_response
