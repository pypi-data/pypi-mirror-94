class soft():
	def wh(ew):
		import pymem
		import re

		pm = pymem.Pymem('csgo.exe')
		client = pymem.process.module_from_name(pm.process_handle,
		                                        'client.dll')

		clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
		address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F',clientModule).start() + 2

		pm.write_uchar(address, 2 if pm.read_uchar(address) == 1 else ew)
		pm.close_process()
				



	def bhop():
		import keyboard
		import time

		def main():
		    while True:

		        if keyboard.is_pressed("space"):
		            while True:
		                time.sleep(0.00015)
		                keyboard.press_and_release("space")
		                time.sleep(0.030)
		                break
		              
		              
		main()

	def radar():
		import pymem, requests, pymem.process
		from threading import Thread

		url = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
		response = requests.get(url).json()

		dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
		dwEntityList = int(response["signatures"]["dwEntityList"])

		m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
		m_bSpotted = int(response["netvars"]["m_bSpotted"])

		# <Подлкючение к игре>

		pm = pymem.Pymem("csgo.exe")
		client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

		# <Объявление функции>

		def RadarHack():
		    while True:
		        if pm.read_int(client + dwLocalPlayer):
		            localplayer = pm.read_int(client + dwLocalPlayer)
		            localplayer_team = pm.read_int(localplayer + m_iTeamNum)
		        for i in range(64):
		            if pm.read_int(client + dwEntityList + i * 0x10):
		                entity = pm.read_int(client + dwEntityList + i * 0x10)
		                entity_team = pm.read_int(entity + m_iTeamNum)
		            if entity_team != localplayer_team:
		                pm.write_int(entity + m_bSpotted, 1)

		# <Запуск функции>

		Thread(target=RadarHack).start()



soft.wh(1)