<p align="center">
  <a href="#quations">Вывод уравнений</a> •
  <a href="#install">Установка</a> •
  <a href="#launch">Запуск</a> •
  <a href="#modification">Модификация</a> •
  <a href="#faq">Вопросы</a> •
</p>


<a id="equations"></a>
<h2 align="center">Вывод уравнений</h2>
 
![](./docs/images/im1.png)
![](./docs/images/im2.png)


<a id="install"></a>
<h2 align="center">Установка</h2>

1. Перейдите в папку со скачанным проектом.
```bash
cd /path/to/your/project
```

2. Далее установите все дополнительные модули, используемые при обработке (находясь в той же самой директории проекта, как и в п.1).
```bash
sudo pip install -r requirments.txt
```

<a id="launch"></a>
<h2 align="center">Запуск</h2>

Из директории проекта запускаем скрипт.
```bash
python main.py
```

<a id="modification"></a>
<h2 align="center">Модификация</h2>

Все параметры (константы, точки, пути сохранения) прописываются в файле `init.json`.
Например, поменять директорию сохранения графиков можно изменив относительный по умолчанию путь. 
```json
{
  ...
  "output" : {
    "directory" : "your/custom/relative/path/",
    "extension": "pdf"
  }
  ...
}
```

<a id="faq"></a>
<h2 align="center">Вопросы</h2>

По всем вопросам писать на `tarlinskyigoresha@gmail.com`