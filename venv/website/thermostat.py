import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from skyportInterface import SkyportInterface
from typing import Optional
from datetime import datetime
import termcolor

class Thermostat:
    def __init__(self) -> None:
        self.skyport = SkyportInterface()
        self.device_id = None
        self.dkn = None
        self.prev_read: Optional[datetime] = None
        self.prev_write: Optional[datetime] = None
        self.datamap = None
    
    def login(self, email, password, thermostat_name):
        try:
            if (self.skyport.login(email, password, thermostat_name)):
                # if (os.environ.get("ID")):
                #     self.device_id = os.environ["ID"]
                #     print("Found a device ID which can be reused")
                #     return
                # print("Device ID does not exist!")
                # device_id = input("\nPlease provide device ID: ")
                # self.device_id = device_id
                # os.environ["ID"] = self.device_id

                devices = self.skyport.devices()
                device = None
                for item in devices:
                    if (item["name"].lower().strip() == thermostat_name.lower().strip()):
                        device = item
                
                if(device):
                    print("Computed device id: " + device["id"])
                    self.device_id = device["id"]
                    # os.environ["ID"] = self.device_id
                else:
                    print("Thermostat: " + thermostat_name + "not found")
            else: 
                "Unable to login to account"
        except Exception as e:
            print(f'An error occured during attempt to login: {e}')
    

    def read_datamap(self):
        try:
          # Use cached value if available. Cache ttl is 60 seconds
          now = datetime.now()
          diff = None

          if (self.prev_read):
            diff = now.timestamp()*1000 - self.prev_read.timestamp()*1000

          # if 60s have passed update the datamap
          if (diff == None or diff >= 60 * 1000):
            print(termcolor.colored('\ncollecting data...', "light_yellow"))
            print('for device ID: ', self.device_id)
            self.datamap = self.skyport.device_data(self.device_id)
            self.prev_read = now
            print(termcolor.colored('Datamap received!', "light_blue"))

          return self.datamap
        except Exception as e:
            print(f'An error occurred during attempt to read datamap: {e}')
    
    def write_datamap(self, changes = {}):
        try:
          # Limit write to once every 30 seconds
          now = datetime.now()
          diff = None

          if(self.prev_write):
              diff = now.timestamp()*1000 - self.prev_write.timestamp()*1000

          self.prev_write = now

          if (diff == None or diff >= 30 * 1000):
              return self.skyport.put(self.device_id, changes)
          else:
              print("Too many writes to thermostat. Limit writes to once every 30 seconds")
        except Exception as e:
            print(f'An error occurred during attempt to write to datamap: {e}')
        


            
  
        
      

        

    
