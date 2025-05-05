import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response

        self.url = f'http://127.0.0.1:8000/smarthouse/actuator/{self.did}/current/'
        self.headers = {'accept': 'application/json'}

        while True:
            try:
                response = requests.put(self.url, headers=self.headers)
                if response.status_code == 200:
                    posts = response.json()
                    logging.info(f"Actuator {posts['id']} state: {posts['state']}")
                    self.state.state = response.json()['state']
                else:
                    logging.error(f'Error: {response.status_code}')
            except requests.exceptions.RequestException as e:
                logging.error(f'Error: {e}')
        
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

    def run(self):

        # start thread simulating physical light bulb
        actuator_thread = threading.Thread(target=self.simulator, daemon=True)
        actuator_thread.start()

        # start thread receiving state from the cloud
        actuator_client_thread = threading.Thread(target=self.client, daemon=True)
        actuator_client_thread.start()


