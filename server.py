from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="abstract project", description="useless shit", version="0.0.1", redoc_url=None)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>abstract project</title>
        </head>
        <body>
            <h1>лист кодов каких то</h1>
            <h2>используй /code/{code_id}</h2>
            <h3>1 - задание 10</h3>
            <h3>2 - задание 6</h3>
            <h3>3 - задание 5</h3>
            <h3>4 - задание 1</h3>
        </body>
    </html>
    """

@app.get("/code/{code_id}", response_class=HTMLResponse)
def read_item(code_id: int):
    match code_id:
        case 1:
            return """
    <html>
        <head>
            <title>задание 10</title>
        </head>
        <body>
            <h1>задание 10</h1>
            <h2>коды:</h2>
            <h3>тип: Переведите число 87 из десятичной системы счисления в двоичную систему счисления. В ответе укажите двоичное число. Основание системы счисления указывать не нужно.</h3>
            <h4>print(bin(87)[2:])</h4>
            <h3>тип: Среди приведенных ниже трех чисел, записанных в различных системах счисления, найдите максимальное и запишите его в ответе в десятичной системе счисления. В ответе запишите только число, основание системы счисления указывать не нужно.</h3>
            <h4>a = int("ЧИСЛО", base=16)<br>b = int("ЧИСЛО", base=8)<br>c = int("ЧИСЛО", base=2)<br>print(a, b, c)</h4>
        </body>
    </html>"""
        case 2:
            return """
    <html>
        <head>
            <title>задание 6</title>
        </head>
        <body>
            <h1>задание 6</h1>
            <h2>коды:</h2>
            <h3>тип:<br>s = int(input())<br>t = int(input())<br>if s > 10 or t > 10:<br>    print("YES")<br>else:<br>    print("NO")<br>(1, 2); (11, 2); (1, 12); (11, 12); (–11, –12); (–11, 12); (–12, 11); (10, 10); (10, 5).</h3>
            <h4>def func(s, t):<br>    if s > 10 or t > 10:<br>        print("YES")<br>    else:<br>        print("NO")<br><br>spisok = "spisok = (СПИСОК)".replace(";", "-").replace("–", "-")<br>exec(spisok)<br>for s, t in spisok:<br>    func(s, t)</h4>
        </body>
    </html>
        """
        case 3:
            return """
    <html>
        <head>
            <title>задание 5</title>
        </head>
        <body>
            <h1>задание 5</h1>
            <h2>коды:</h2>
            <h3>тип:<br>У исполнителя Альфа две команды, которым присвоены номера:<br>1. прибавь 1;<br>2. умножь на b<br>(b  — неизвестное натуральное число; b ≥ 2).<br>Выполняя первую из них, Альфа увеличивает число на экране на 1, а выполняя вторую, умножает это число на b. Программа для исполнителя Альфа  — это последовательность номеров команд. Известно, что программа 11211 переводит число 6 в число 82. Определите значение b.</h3>
            <h4>for b in range(1, 100):<br>    a = (6 + 1 + 1) * b + 1 + 1<br>    if a == 82:<br>        print(b)</h4>
        </body>
    </html>
        """
        case 4:
            return """
    <html>
        <head>
            <title>задание 1</title>
        </head>
        <body>
            <h1>задание 1</h1>
            <h2>коды:</h2>
            <h3>тип:<br>В одной из кодировок Unicode каждый символ кодируется 16 битами. Вова написал текст (в нем нет лишних пробелов):<br>«еж, лев, слон, олень, тюлень, носорог, крокодил, аллигатор  — дикие животные».<br>Ученик вычеркнул из списка название одного из животных. Заодно он вычеркнул ставшие лишними запятые и пробелы  — два пробела не должны идти подряд.<br>При этом размер нового предложения в данной кодировке оказался на 16 байт меньше, чем размер исходного предложения. Напишите в ответе вычеркнутое название животного.</h3>
            <h4>encoding = int(input("введи наскоко каждый битов символ кодируется: "))<br>a = int(input("введи наскоко меньше стало: "))<br>codirovka = encoding / 8<br>result = (a - (2 * codirovka)) / codirovka<br>print(result)</h4>
        </body>
    </html>"""
