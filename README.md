# prod-stories-HW5
## Подготовка к запуску
<pre>$ conda env create -f environment.yml</pre>
## Запуск
### Генерация 3D-фигур
1. Открываем blender
<pre>$ blender &</pre>
2. Нажимаем File -> Open...
3. Выбираем файл <a href="https://github.com/myutman/prod-stories-HW5/blob/master/random_shapes.blend">random_shapes.blend</a>
4. Запускаем открывшийся скрипт
Модели лежат <a href="">здесь</a>
### Вычисление гистограм
1. Нужно, чтобы модели фигур из предыдущего шага лежали в директории ./models
2. Открываем ноутбук <a href="https://github.com/myutman/prod-stories-HW5/blob/master/download_histograms.ipynb">download_histograms.ipynb</a>
<pre>$ jupyter lab download_histograms.ipynb</pre>
3. Нажимаем Run -> Run All Cells
### Обучение embedding-ов
