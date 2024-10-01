import os
import requests
import time

class Vana:

    def headers(self, initData):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Telegram-Web-App-Init-Data": initData
        }

    def log(self, msg):
        print(f"[*] {msg}")

    def wait_with_countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"[*] Mohon tunggu {i} detik untuk akun selanjutnya...", end='\r')
            time.sleep(1)
        print()

    def get_player_data(self, initData):
        url = 'https://www.vanadatahero.com/api/player'
        headers = self.headers(initData)
        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            self.log('Terjadi kesalahan saat memanggil API')
            print(e)

    def post_task_completion(self, initData, taskId, points):
        url = f'https://www.vanadatahero.com/api/tasks/{taskId}'
        headers = self.headers(initData)
        payload = {
            "status": "completed",
            "points": float(points)
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.json().get('message') == 'Points limit exceeded':
                self.log('Berhasil melakukan semua tugas untuk hari ini!')
                return False
            return True
        except Exception as e:
            self.log('Terjadi kesalahan saat menyelesaikan tugas')
            print(e)
            return False

    def get_tasks(self, initData):
        url = 'https://www.vanadatahero.com/api/tasks'
        headers = self.headers(initData)
        try:
            response = requests.get(url, headers=headers)
            return response.json().get('tasks', [])
        except Exception as e:
            self.log('Terjadi kesalahan saat mengambil daftar tugas')
            print(e)

    def complete_pending_tasks(self, initData):
        tasks = self.get_tasks(initData)
        exclude_ids = [2, 17, 5, 9]
        for task in tasks:
            if not task.get('completed') and task['id'] not in exclude_ids:
                success = self.post_task_completion(initData, task['id'], task['points'])
                if success:
                    self.log(f"Menjalankan tugas {task['name']} berhasil mendapatkan: {task['points']}")

    def process_account(self, initData, accountIndex):
        try:
            playerData = self.get_player_data(initData)
            if playerData:
                print(f"========== Menjalankan akun {accountIndex} | {playerData['tgFirstName']} ==========")
                self.log(f"Points: {playerData['points']}")
                self.log(f"Multiplier: {playerData['multiplier']}")
            while True:
                taskCompleted = self.post_task_completion(initData, 1, round((50000.0 - 40000.0) * time.time(), 1))
                if not taskCompleted:
                    break
                updatedPlayerData = self.get_player_data(initData)
                if updatedPlayerData:
                    self.log(f"Auto tap berhasil. Total Balance: {updatedPlayerData['points']}")
                time.sleep(1)
            self.complete_pending_tasks(initData)
        except Exception as e:
            self.log('Terjadi kesalahan saat memproses akun')
            print(e)

    def main(self):
        data_file = os.path.join(os.getcwd(), 'data.txt')
        with open(data_file, 'r') as f:
            initDataList = [line.strip() for line in f.readlines() if line.strip()]
        for i, initData in enumerate(initDataList):
            self.process_account(initData, i + 1)
            self.wait_with_countdown(3)
        self.wait_with_countdown(86400)


if __name__ == "__main__":
    vana = Vana()
    vana.main()
