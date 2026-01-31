import requests
from api.endpoints import *

class YandexDiskAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': f'OAuth {token}',
            'Content-Type': 'application/json'
        }
    
    def _request(self, method, url, **kwargs):
        """Базовый метод для запросов"""
        response = requests.request(method, url, headers=self.headers, **kwargs)
        return response
    
    # Методы для работы с файлами
    def get_disk_info(self):
        return self._request('GET', BASE_URL)
    
    def upload_file(self, file_path, disk_file_path, overwrite=False):
        # 1. Получаем ссылку для загрузки
        params = {'path': disk_file_path, 'overwrite': overwrite}
        response = self._request('GET', FILES_URL, params=params)
        
        if response.status_code == 200:
            href = response.json()['href']
            # 2. Загружаем файл по полученной ссылке
            with open(file_path, 'rb') as f:
                upload_response = requests.put(href, files={'file': f})
            return upload_response
        return response
    
    def create_folder(self, path):
        params = {'path': path}
        return self._request('PUT', RESOURCES_URL, params=params)
    
    def delete_resource(self, path, permanently=False):
        params = {'path': path, 'permanently': permanently}
        return self._request('DELETE', RESOURCES_URL, params=params)
    
    def get_resource_info(self, path):
        params = {'path': path}
        return self._request('GET', RESOURCES_URL, params=params)
    
    def publish_resource(self, path):
        params = {'path': path}
        return self._request('PUT', PUBLISH_URL, params=params)