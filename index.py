import requests
from datetime import datetime, timedelta
import time
import pygame as pyg

def input_kota():
    kota = input('Masukkan Kota Anda: ')
    return kota.lower()

def get_date_now():
    today = datetime.now()
    return today.day, today.month, today.year

def get_adzan():
    pyg.init()
    pyg.mixer.init()
    pyg.mixer.music.load('adzan.mp3')
    pyg.mixer.music.set_volume(1.0)
    pyg.mixer.music.play()

def get_kota_id(url, kota):
    url += f'kota/cari/{kota}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['data'][0]['id']
    else:
        print(f'Error: {response.status_code}')

def get_data_sholat_api(url, kota_id):
    day, month, year = get_date_now()
    
    url += f'jadwal/{kota_id}/{year}/{month}/{day}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        jadwal = data['data']['jadwal']
            
        print('Tekan "Spasi" untuk melihat waktu sekarang')
        print('Tekan "Esc" untuk mematikan aplikasi')
        
        while True:
            waktu_sekarang = datetime.now().time().replace(microsecond=0)
            
            for waktu, jam in jadwal.items():
                if waktu != 'tanggal' and waktu != 'date':
                    jadwal_jam = datetime.strptime(jam, '%H:%M').time()
                    
                    if (datetime.combine(datetime.today(), jadwal_jam) + timedelta(minutes=10)).time() >= waktu_sekarang > jadwal_jam or waktu_sekarang == jadwal_jam:
                        print(f'Waktunya Adzan {waktu.capitalize()}')
                        get_adzan()
                        while pyg.mixer.music.get_busy():
                            time.sleep(0.1)
                        
                        time.sleep(1800)
                    
                    if (datetime.combine(datetime.today(), jadwal_jam) - timedelta(minutes=10)).time() <= waktu_sekarang < jadwal_jam:
                        print(f'Sebentar lagi waktunya Adzan {waktu.capitalize()}')
                        print(f'Adzan {waktu.capitalize()}: {jadwal_jam}')
                        
                        time.sleep(300)
            
            time.sleep(1)
            
    else:
        print(f'Error: {response.status_code}')
    

if __name__ == '__main__':
    url = 'https://api.myquran.com/v2/sholat/'
    
    kota = input_kota()
    kota_id = get_kota_id(url, kota)
    if kota_id:
        get_data_sholat_api(url, kota_id)
        
    