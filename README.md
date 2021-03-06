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
Модели лежат <a href="https://drive.google.com/drive/folders/1heHTSELIvi8OT_Jv-PWU3WYf5cLu2rHv?usp=sharing">здесь</a>
### Вычисление гистограм
1. Нужно, чтобы модели фигур из предыдущего шага лежали в директории ./models
2. Открываем ноутбук <a href="https://github.com/myutman/prod-stories-HW5/blob/master/download_histograms.ipynb">download_histograms.ipynb</a>
<pre>$ jupyter lab download_histograms.ipynb</pre>
3. Нажимаем Run -> Run All Cells
### Обучение embedding-ов
1. Открываем ноутбук <a href="https://github.com/myutman/prod-stories-HW5/blob/master/metric_learning.ipynb">metric_learning.ipynb</a>
<pre>$ jupyter lab metric_learning.ipynb</pre>
2. Нажимаем Run -> Run All Cells
Веса обученной сети лежат <a href="https://drive.google.com/drive/folders/1Ff7NHksSPT1GjlVeavdeSyHAwL9X1sGO?usp=sharing">здесь</a>
### Кластеризация и анализ
1. Нужно, чтобы веса обученной сети лежали в директории ./checkpoints
2. Открываем ноутбук <a href="https://github.com/myutman/prod-stories-HW5/blob/master/random_shapes.blend">random_shapes.blend</a>
3. Нажимаем Run -> Run All Cells
## Эксперимент
### Постановка
* Были получены гистограммы для 401 3D-модели
* Изначальные модифицируемые фигуры были использованы в качестве классов
* 50 записей были отложены в качестве <a href="https://github.com/myutman/prod-stories-HW5/blob/master/dataset/test.tsv">тестового набора</a>
* Остальные записи были поделены в соотношении 1 к 1 на <a href="https://github.com/myutman/prod-stories-HW5/blob/master/dataset/train.tsv">обучающие данные</a> и <a href="https://github.com/myutman/prod-stories-HW5/blob/master/dataset/valid.tsv">валидационные данные</a>
### Используемая модель
* На обучающем наборе были обучены эмбеддинги с помощью подхода metric learning
* В качестве модели была использована FeedForwardNetwork со входом размера 128, 4 скрытыми полносвязными слоями размера 32 и выходом размера 16
* Выходной вектор нормировался до единичной нормы
* На батчах размера 16 считались попарные cosine_loss (1 + dot_product(v1, v2)) / 2 в случае неравенства классов и (1 - dot_product(v1, v2)) / 2 в случае неравенства классов
* Построенные эмбеддинги были использованы для кластеризации тестового множества
### Результаты
* Метрики обучения можно посмотреть здесь: https://wandb.ai/myutman/prod-stories-HW5/runs/1bf05ove?workspace=user-myutman
* После применения алгоритма AgglomerativeClustering для кластеризации на 5 классов при проекции на 2 принципиальные компоненты, получилась следующая картина:
![scatter](https://github.com/myutman/prod-stories-HW5/blob/master/scatter.png)
* В итоге, кластеры не соответствуют изначальным классам
* Также для каждого embedding-а из тестового набора был найден ближайший по косинусной метрике центр класса эмбеддингов из обучающих данных
* Была посчитана точность определения классов, как отношение правильно определнных классов к общему количеству записей в тестовых данных
* Полученное значение метрики оказалось равно 0.34, что не позволяет заявлять о хорошем качестве определения класса с помощью эмбеддингов
### Выводы и направления для дальнейших исследований
* Используемая архитектура модели не позволяет эффективно кластеризовать 3D-модели по гистограммам
* Возможно, для лучшего результата необходимо будет использовать большее количество данных, больший размер модели (в частности, размерность пространства эмбеддингов), а также другие параметры обучения
