# Flask File Processor

### Описание

Это Flask-приложение обрабатывает файлы различных форматов, включая **plain text**, **JSON**, **YAML** и **XML**. Основная цель — обработать содержимое файла, применяя вычисления или модификации, и сохранить результат.

Приложение поддерживает загрузку файлов через веб-интерфейс, автоматическое определение типа файла, обработку его содержимого и сохранение обработанного результата.

---

### Основные возможности

1. **Обработка текста**:
   - Строки вычисляются с помощью `eval`.
   - Если вычисление невозможно, возвращается сообщение об ошибке.

2. **Обработка JSON**:
   - Парсинг JSON с использованием `json.loads`.
   - Рекурсивная обработка строк через функцию `process_text`.
   - Форматирование результата в читаемый JSON.

3. **Обработка YAML**:
   - Парсинг с использованием `yaml.safe_load`.
   - Рекурсивная обработка строк.
   - Сериализация обратно в формат YAML.

4. **Обработка XML**:
   - Парсинг с использованием `xml.etree.ElementTree`.
   - Рекурсивная обработка текстовых узлов XML-дерева.
   - Возврат результата в строковом представлении XML.

5. **Поддержка загрузки файлов**:
   - HTML-интерфейс для загрузки файлов.
   - Обработка файлов с расширениями `.txt`, `.json`, `.yaml`, `.yml`, `.xml`.

---

### Структура проекта

```plaintext
PP/
├── app/
│   ├── templates/
│   │   └── index.html      # HTML-шаблон для интерфейса
│   ├── __init__.py         # Инициализация Flask-приложения
│   ├── routes.py           # Маршруты приложения
│   └── utils.py            # Вспомогательные функции обработки файлов
├── files/                  # Папка для загрузки и хранения файлов
├── tests/                  # Unit-тесты
│   ├── __init__.py
│   └── test_routes.py
├── .gitignore              # Исключения для Git
├── README.md               # Документация проекта
├── requirements.txt        # Список зависимостей Python
└── run.py                  # Точка входа приложения
```

---

### Установка и запуск

1. **Склонируйте репозиторий**:
   ```bash
   git clone https://github.com/BOCXO2/PP.git
   cd PP
   ```

2. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите приложение**:
   ```bash
   python run.py
   ```

4. **Откройте браузер** и перейдите по адресу `http://127.0.0.1:5000`.

---

### Пример работы

1. Загрузите файл `data.json` через веб-интерфейс.
2. Приложение:
   - Парсит JSON.
   - Обрабатывает строки, вычисляя значения с помощью `eval`.
   - Сохраняет результат в файл `processed_data.json` в папке `files/`.
3. Ответ возвращается в формате JSON:
   ```json
   {
       "message": "File processed",
       "output_file": "files/processed_data.json"
   }
   ```

---

### Зависимости

Список зависимостей хранится в `requirements.txt`. Основные библиотеки:

- **Flask** — веб-фреймворк.
- **PyYAML** — для работы с YAML.
- **json** и **xml.etree.ElementTree** — стандартные библиотеки Python.

Установите зависимости с помощью:
```bash
pip install -r requirements.txt
```

---

### Тестирование

Unit-тесты расположены в папке `tests/`. Запуск тестов:
```bash
pytest tests/
```

---
