"""
Диагностика проблемы с токеном Яндекс.Диска
"""
import requests

def diagnose_token(token):
    print("=" * 60)
    print("ДИАГНОСТИКА ТОКЕНА ЯНДЕКС.ДИСК")
    print("=" * 60)
    
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Проверяем базовый доступ
    print("\n1. Проверка доступа к API...")
    response = requests.get(
        "https://cloud-api.yandex.net/v1/disk",
        headers=headers,
        timeout=10
    )
    
    print(f"   Статус: {response.status_code}")
    print(f"   Ответ: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"  Доступ есть! Диск: {data.get('total_space', 0)/1024**3:.1f}GB")
        return True
    elif response.status_code == 403:
        print("    Ошибка 403: Доступ запрещен")
        print("\n   Возможные причины:")
        print("   • Токен не имеет прав на Яндекс.Диск")
        print("   • Токен создан для другого приложения")
        print("   • Нужно подтвердить права в Яндекс.OAuth")
    elif response.status_code == 401:
        print("    Ошибка 401: Неавторизован (токен недействителен)")
    else:
        print(f"  Неожиданный статус: {response.status_code}")
    
    # 2. Проверяем, какой это тип токена
    print("\n2. Проверка типа токена...")
    print(f"   Длина токена: {len(token)} символов")
    print(f"   Начинается с: {token[:20]}...")
    
    # 3. Пробуем получить информацию о приложении
    print("\n3. Пробуем получить информацию о токене...")
    try:
        info_response = requests.get(
            "https://login.yandex.ru/info",
            headers={'Authorization': f'OAuth {token}'},
            timeout=10
        )
        print(f"   Статус info: {info_response.status_code}")
        if info_response.status_code == 200:
            print(f"   Токен валиден для аккаунта")
            print(f"   Инфо: {info_response.json().get('login', 'N/A')}")
        else:
            print(f"   Нет доступа к информации аккаунта")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # 4. Проверяем права через OAuth
    print("\n4. Проверка прав токена...")
    print("   Перейдите на: https://oauth.yandex.ru/authorize?response_type=token&client_id=")
    print("   Посмотрите, какие права запрашиваются")
    
    return False

def get_working_solution():
    print("\n" + "=" * 60)
    print("РЕШЕНИЕ ПРОБЛЕМЫ С ТОКЕНОМ")
    print("=" * 60)
    
    print("\nВАРИАНТ 1: Получить токен через Яндекс.OAuth (правильно)")
    print("  1. Зайдите: https://oauth.yandex.ru/client/new")
    print("  2. Создайте новое приложение:")
    print("     • Название: 'Test API App'")
    print("     • Платформы: 'Веб-сервисы'")
    print("     • Callback URI: https://oauth.yandex.ru/verification_code")
    print("     • ПРАВА: Обязательно выберите 'Яндекс.Диск REST API'")
    print("  3. Получите Client ID и Client Secret")
    print("  4. Используйте для получения токена")
    
    print("\nВАРИАНТ 2: Использовать токен из командной строки (быстро)")
    print("  curl -X POST https://oauth.yandex.ru/token \\")
    print("       -d 'grant_type=password' \\")
    print("       -d 'username=ВАШ_ЛОГИН' \\")
    print("       -d 'password=ВАШ_ПАРОЛЬ' \\")
    print("       -d 'client_id=ВАШ_CLIENT_ID' \\")
    print("       -d 'client_secret=ВАШ_CLIENT_SECRET'")
    
    print("\nВАРИАНТ 3: Временное решение для тестового задания")
    print("  Используйте заглушки (моки) для демонстрации логики")
    print("  Объясните, что с рабочим токеном все будет работать")

if __name__ == "__main__":
    # Введите ваш токен здесь
    YOUR_TOKEN = input("Введите ваш токен: ").strip()
    
    if not YOUR_TOKEN:
        YOUR_TOKEN = "y0_AgAAAAA2gcKaAAr7IAAAADqBeK7iRKbEVfJz9MZOF7GmUEE"
        print(f"Используется тестовый токен: {YOUR_TOKEN[:20]}...")
    
    is_valid = diagnose_token(YOUR_TOKEN)
    
    if not is_valid:
        get_working_solution()
    
    input("\nНажмите Enter для выхода...")