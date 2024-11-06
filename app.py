from app import create_app  # Импортируем функцию create_app из модуля community_app



# Проверяем, запускается ли скрипт как основная программа
if __name__ == '__main__':
    app = create_app()  # Создаем экземпляр приложения с помощью функции create_app
    app.run()  # Запускаем приложение Flask