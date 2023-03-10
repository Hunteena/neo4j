# Тестовое задание по графовым базам данных

Структура репозитория:  
- [jupyter](jupyter) - папка, содержащая [Jupiter (iPython) Notebook](jupyter/neo4j.ipynb) и файлы, 
необходимые для его запуска,
- [.env.example](.env.example) - пример необходимых переменных окружения для сервиса [app.py](app.py),
- [app.py](app.py) - rest-сервис для доступа к базе данных 
(см. описание [ниже](#REST-API-для-получения-информации-из-Neo4j)),
- [README.md](README.md) - файл с этим текстом,
- [requirements.txt](requirements.txt) - зависимости, необходимые для работы сервиса [app.py](app.py).


### Работа с графовой базой данных Neo4j с использованием Cypher
[Jupiter Notebook](jupyter/neo4j.ipynb) содержит :
* внесение данных из источника,
* запросы к базе данных,
* примеры проекций и алгоритмов.


### REST API для получения информации из Neo4j

Данный сервис получает из графовой базы данных все события, 
в которых участвовал указанный человек, 
и записывает узлы и связи в файл формата graphml.  
Пример использования:   
[http://localhost:3000/?name=Галчевская+Карина+Владимировна&filename=events.graphml](http://localhost:3000/?name=Галчевская+Карина+Владимировна&filename=events.graphml)


#### Подготовка
1. Клонируйте этот репозиторий:
    ```shell
    git clone https://github.com/Hunteena/neo4j.git
    ```
2. Создайте файл .env, аналогичный файлу [.env.example](.env.example), и внесите в него свои значения.   

3. Установите зависимости
    ```shell
    pip install -r requirements.txt
    ```

#### Запуск
```shell
flask run
```

#### Использование
Сервер доступен по адресу [http://localhost:3000](http://localhost:3000) 
(если переменная FLASK_RUN_PORT=3000).

Для получения данных задайте в параметрах запроса ФИО 
и, при желании, имя файла для вывода (по умолчанию используется имя файла _output.graphml_).
