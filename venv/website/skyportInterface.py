import json
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import requests

class SkyportInterface:
    def __init__(self):
        self.base_url = "https://api.daikinskyport.com"
        self.url_login = self.base_url + '/users/auth/login'
        self.url_auth_token = self.base_url + '/users/auth/token'
        self.url_device_data = self.base_url + '/deviceData'
        self.url_devices = self.base_url + '/devices'
        self.url_users_me = self.base_url + '/users/me'

        self.access_token = None
        self.refresh_token = None
        self.email = None
        self.expires = None
        self.thermostat_name = None
        self.db = TinyDB('users.json')

    def login(self, email, password, thermostat_name):
        print('\nLogin procedure has started for ' + email)
        self.email = email
        self.thermostat_name = thermostat_name

        if (not self._findToken(email, thermostat_name)):
            print("No saved tokens found, proceeding with login")
            auth_obj = {'email': email, 'password': password}
            response =  self._send(self.url_login, 'POST', obj=auth_obj)

            if (response):
                self.access_token = response['accessToken']
                self.refresh_token = response['refreshToken']
                expires_in_seconds = response['accessTokenExpiresIn']
                self.expires = f'{datetime.now() + timedelta(seconds=expires_in_seconds)}'

                self.db.insert({
                'email': email,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires': self.expires,
                'thermostat_name' : thermostat_name
                })
            else:
                print("Login error ")
                return False
        return True
    
    def destroy(self):
      print("Destroy triggered for ", self.email)
      self.access_token = None
      self.refresh_token = None
      self.email = None
    

    def device_data(self, deviceId):
      print("Read triggered for ", self.email)
      url = self.url_device_data + '/' + deviceId if deviceId else self.url_device_data
      resp =  self._auth_token_and_send(url, "GET")
      return resp if resp else None

    def put(self, deviceId, obj):
      print("\nThermostat write tirggered for " +  deviceId)
      resp =  self._auth_token_and_send(self.url_device_data+'/'+deviceId ,"PUT", obj=obj)
      return resp if resp else None

    def devices(self):
      print("Read list of devices " + self.email)
      resp =  self._auth_token_and_send(self.url_devices, "GET")
      return resp if resp else []

    def usersName(self):
      print("Read users name")
      resp =  self._auth_token_and_send(self.url_users_me, "GET")
      return resp if resp else None

    def _auth_token(self):
      print("Auth token triggered " + str(datetime.now()))
      auth_obj = {'email': self.email, 'refreshToken': self.refresh_token}
      resp =  self._send(self.url_auth_token, "POST", obj=auth_obj)
      if (resp):
        self.access_token = resp['accessToken']
        expires_in_seconds = resp['accessTokenExpiresIn']
        self.expires = f'{datetime.now() + timedelta(seconds=expires_in_seconds)}'
        Token = Query()
        self.db.update(
          {
            'email': self.email,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires': self.expires,
            'thermostat_name': self.thermostat_name,
          }, 
          (Token.email == self.email) & (Token.thermostat_name == self.thermostat_name)
        )
      else:
        print("Refresh token error ")

    def _auth_token_and_send(self, url, method, obj={}):
      date_format = "%Y-%m-%d %H:%M:%S.%f"
      if (self.expires and datetime.strptime(self.expires, date_format) < datetime.now()):
         self._auth_token()
      return  self._send(url, method, obj)


    def _findToken(self, email, thermostat_name ):
        print("\nFind tokens for " + email)
        Token = Query()
        docs = self.db.search((Token.email == email) & (Token.thermostat_name == thermostat_name))
        if (len(docs) == 0):
            return None

        self.access_token = docs[0]['access_token']
        self.refresh_token = docs[0]['refresh_token']
        self.expires = docs[0]['expires']
        print("Found valid token which can be reused\n")

        return docs
    
    def _send(self, url, method, obj):
        try:
            headers = {
              "Content-Type": "application/json"
            }

            if (self.access_token):
              headers["Authorization"] = f'Bearer {self.access_token}'

            body = None
            if(len(obj)>0):
                body = json.dumps(obj)
            
            response = requests.request(method=method, url=url, headers=headers, data=body)
            data = response.json()
            return data

        except requests.exceptions.HTTPError as http_err:
          print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
          print(f'Connection error occurred: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
          print(f'Timeout error occurred: {timeout_err}')
        except requests.exceptions.RequestException as req_err:
          print(f'An error occurred: {req_err}')
        except ValueError as json_err:
          print(f'Error parsing JSON: {json_err}')
        


