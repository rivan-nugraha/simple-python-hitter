#!/usr/bin/python3

import json
import requests
import logging
from datetime import datetime
import os

# Konfigurasi Logging
LOG_DIR = 'logs'
LOG_FILE = 'hit_endpoints.log'

# Membuat direktori log jika belum ada
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def hit_endpoints():
    # Baca file JSON yang berisi daftar endpoints
    try:
        with open('endpoints.json', 'r') as file:
            data = json.load(file)
        logging.info("Berhasil membaca file endpoints.json.")
    except Exception as e:
        logging.error(f"Gagal membaca file endpoints.json: {e}")
        return

    # Dapatkan tanggal saat ini dalam format "YYYY-MM-DD"
    current_date = datetime.now().strftime('%Y-%m-%d')
    payload = {"tgl_system": current_date}

    # Loop melalui setiap endpoint dalam file JSON
    for endpoint in data.get('endpoints', []):
        name = endpoint.get('name')
        url = endpoint.get('ip')
        
        if not name or not url:
            logging.warning(f"Endpoint dengan data tidak lengkap: {endpoint}")
            continue

        try:
            # Kirim request POST dengan body JSON
            response = requests.post(url, json=payload, timeout=10, verify=False)
            if response.status_code == 200:
                logging.info(f"Berhasil mengirim request ke {name} ({url}) dengan tanggal {current_date}.")
            else:
                logging.warning(f"Gagal mengirim request ke {name} ({url}). Status code: {response.status_code}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error saat mengirim request ke {name} ({url}): {e}")

if __name__ == "__main__":
    hit_endpoints()