import pytest
import tempfile
import os
from api.client import YandexDiskAPI

# ТЕСТОВЫЙ ТОКЕН с полигона 
TEST_TOKEN = "y0_AgAAAABknB8DAAG8XgAAAADN6GpSKd66ThUOdkFdhld_Ga8N"

@pytest.fixture(scope="session")
def api_client():
    """Фикстура с API-клиентом"""
    return YandexDiskAPI(TEST_TOKEN)

@pytest.fixture
def temp_file():
    """Создаём временный файл для тестов"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content for Yandex Disk API")
        temp_path = f.name
    
    yield temp_path
    
    # Удаляем после теста
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def test_folder_name():
    return "test_folder_api"