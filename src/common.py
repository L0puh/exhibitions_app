import os, json

def icon(path:str):
    return os.path.join(ICON_DIR, path)

def get_json(key) -> list:
    name = os.path.join(os.getcwd(), "assets", "data.json")
    try:
        file = open(name, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
        return data[key]
    except:
        print("error in getting json:", name)
        return []


ICON_DIR = os.path.join(os.getcwd(), 'assets', 'icons')
SQL_FILE = os.path.join(os.getcwd(), 'assets', 'query.sql')
DATABASE_FILE = os.path.join(os.getcwd(), 'assets', 'database.db')


WELCOME_TEXT = """
<h1>Добро пожаловать в приложение для автоматизации выставочного
агенства "Арт Экспо".</h1>

<p>Мы рады приветствовать вас в нашем решении, созданном для упрощения процесса
организации выставок. С помощью приложения вы сможете легко создавать
выставки и эффективно управлять доставкой экспонатов. </p>

<h2>Наш главный функционал включает:</h2>
<li>
<ul>1. Создание выставок и экспонатов</ul>
<ul>2. Возможность отслеживания процесса организации выставки</ul>
<ul>3. Менеджмент бронирования экспонатов</ul>
</li>

<p>Для подробной информации о функциональности программы обратитесь к 
разделу "Помощь".</p>

</p>Мы надеемся, что наше приложение сделает вашу работу легче и эффективнее.</p>
Приятной работы!
"""
