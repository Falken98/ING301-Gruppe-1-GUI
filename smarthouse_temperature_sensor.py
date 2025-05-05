import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")
        
        # send temperature to the cloud service with regular intervals
        while True:
            # send request to cloud service to update current temperature
            response = requests.post(f'http://localhost:8000/device/{self.did}/current', json={'state': self.measurement.value})
            if response.status_code == 200:
                logging.info(f"Sensor Client {self.did} sent temperature: {self.measurement.value}")
            else:
                logging.error(f"Sensor Client {self.did} failed to send temperature: {response.status_code}")

            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

    def run(self):
        # create and start thread simulating physical temperature sensor
        sensor_thread = threading.Thread(target=self.simulator, daemon=True)
        sensor_thread.start()

        # create and start thread sending temperature to the cloud service
        client_thread = threading.Thread(target=self.client, daemon=True)
        client_thread.start()

