# Healthy CSIT
Это приложение, которое поможет вам составить дневник здоровья,
опираясь на некоторые исходные данные о вас (такие, как
рост, вес, время отхода ко сну, время пробуждения и т.д.).

Конечно же полученный дневник здоровья не будет даже близко
соответствовать вашему самочувствию в дни наблюдения.

Поэтому сразу обозначу
> Результаты работы этого приложения нельзя считать медицински
> достоверными или ставить в соответствие какой-то личности.
> Это приложение может помочь вам получить зачет по физкультуре
> (и даже это не гарантировано), но оно точно не составит
> за вас достоверный дневник здоровья.
> Если у вас есть реальные проблемы со здоровьем, обратитесь
> ко врачу.

## Требования
- Python 3.10 или новее

## Быстрый старт
Клонируйте репозиторий в любое удобное место на вашем компьютере:
```bash
git clone https://github.com/vinc3nzo/healthy-csit.git
```

Перейдите в локальную копию репозитория (где лежат файлы LICENCE и README.md):
```bash
cd healthy-csit
```

Вызовите главный скрипт. Например,
```bash
python .\healthy-csit\hcsit.py healthy-someone.csv --height 186 \
    --weight 67 --heart-beat-rate 68 --blood-pressure 125/86 \
    --appetite 1 --sleep-start 23:30 --sleep-end 06:30 \
    --date-start 16.09.2022 --date-end 16.10.2022
```
Эта команда сгенерирует случайные данные и сохранит их в файл
`healthy-someone.csv`, который будет находиться в корневой папке
репозитория.

## Список параметров
Список параметров, которые возможно передать приложению,
можно вывести при помощи
```bash
python .\healthy-csit\hcsit.py -h
``` 

Некоторые данные надо обязательно передать приложению, а вместо каких-то
приложение возьмет значения по умолчанию.