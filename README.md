# Antiplagiarism_tinkoff
Вступительный экзамен ML Весна'23 Тинькофф
  
## Пример запуска:  

```bash
$ python3 compare.py input.txt scores.txt
```  

## Пример входного файла input.txt  
```text
files/main.py plagiat1/main.py
files/lossy.py plagiat2/lossy.py
files/lossy.py files/lossy.py
files/auto.py plagiat1/auto.py
files/auto.py plagiat2/auto.py
```

## Пример выходеого файла scores.txt:
```text
0.98
0.4
1.0
1.0
1.0
```
