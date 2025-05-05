import tkinter as tk
from tkinter import ttk
import logging
import requests

from messaging import ActuatorState
import common


def lightbulb_cmd(state, did):

    new_state = state.get()

    logging.info(f"Dashboard: {new_state}")

    # send HTTP request with new actuator state to cloud service
    url = f'http://127.0.0.1:8000/smarthouse/actuator/{did}/'
    headers = {'accept': 'application/json'}
    if new_state == 'On':
        data = {'state': True}
    else:
        data = {'state': False}

    try:
        response = requests.put(url, headers=headers, params=data)
        # logging.info(f"Response: {response.status_code}")
        if response.status_code == 200:
            posts = response.json()
            logging.info(f"Actuator {posts['id']} state: {posts['is_active']}")
        else:
            logging.error(f'Error:{response.status_code}')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error:{e}')


def init_lightbulb(container, did):

    lb_lf = ttk.LabelFrame(container, text=f'LightBulb [{did}]')
    lb_lf.grid(column=0, row=0, padx=20, pady=20, sticky=tk.W)

    # variable used to keep track of lightbulb state
    lightbulb_state_var = tk.StringVar(None, 'Off')

    on_radio = ttk.Radiobutton(lb_lf, text='On', value='On',
                               variable=lightbulb_state_var,
                               command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    on_radio.grid(column=0, row=0, ipadx=10, ipady=10)

    off_radio = ttk.Radiobutton(lb_lf, text='Off', value='Off',
                                variable=lightbulb_state_var,
                                command=lambda: lightbulb_cmd(lightbulb_state_var, did))

    off_radio.grid(column=1, row=0, ipadx=10, ipady=10)
