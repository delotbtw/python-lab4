# algopack

Алгоритмический мини-пакет: Fibonacci, две сортировки, приоритетная очередь,
генераторы тестовых наборов и benchmark.

Лабораторная работа 4 по Python.

## Установка и запуск

Нужен Python 3.12+ и [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run pytest
uv run python scripts/demo.py
uv run python scripts/run_benchmark.py
```

`demo.py` — демо для защиты, идёт по критериям оценки (подробнее ниже).

`run_benchmark.py` принимает `--sizes`, `--repeats`, `--seed`, `--out`
и кладёт `benchmark.csv` и `benchmark.md` в `reports/`.

Проверки качества:

```bash
uv run pytest --cov --cov-report=term-missing
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Покрытие около 97%, `ruff` и `mypy` (strict) проходят без замечаний.

## Структура

```
src/algopack/
  consts.py          константы
  enums.py           InputKind, Complexity
  errors.py          исключения
  aliases.py         тип KeyFunc
  recurrence.py      Fibonacci
  sorting.py         insertion_sort, merge_sort
  select.py          quickselect
  priority_queue.py  PriorityQueue
  generators.py      генераторы наборов
  benchmark.py       измерения
  report.py          CSV и Markdown отчёт
  cli.py             запуск benchmark
tests/
scripts/             demo.py (демо для защиты), run_benchmark.py
reports/             результаты benchmark
```

## Сложность

| Что | Время | Доп. память |
|---|---|---|
| `fib_iterative(n)` | O(n) | O(1) |
| `fib_recursive(n)` | O(n) | O(n), стек |
| `insertion_sort` | O(n²), на отсортированном O(n) | O(n) |
| `merge_sort` | O(n log n) | O(n) |
| `quickselect` | O(n) в среднем, O(n²) в худшем | O(n) |
| `PriorityQueue.push`, `pop` | O(log n) | O(n) всего |
| `PriorityQueue.peek`, `len`, `bool` | O(1) | O(1) |

Доп. память сортировок O(n), потому что обе возвращают новый список.

## Fibonacci

- Определение: `F(0) = 0`, `F(1) = 1`, `F(n) = F(n-1) + F(n-2)`. Отсчёт с нуля,
  то есть `F(2) = 1`, `F(10) = 55`.
- `fib_iterative` — цикл, `fib_recursive` — рекурсия с накоплением пары чисел.
- Неверный ввод (не `int`, `bool`, отрицательное число) — `InvalidInputError`.
- **Ограничение рекурсии.** В Python лимит стека по умолчанию около 1000 кадров
  (`sys.getrecursionlimit()`), глубина `fib_recursive(n)` равна `n`. Поэтому
  при `n > 500` (`MAX_RECURSIVE_N`) функция сразу бросает `InvalidInputError`,
  а не падает с `RecursionError`. Итеративная версия такого лимита не имеет.

## Сортировки

Обе сортировки возвращают новый список, исходный не меняется. `sorted` и
`list.sort` внутри не используются.

- Пустой список, один элемент, дубликаты, отрицательные числа и `float`
  поддерживаются.
- **Неверный тип.** Если передан не `list` и не `tuple` (например `None`, `str`,
  `set`, итератор) — `TypeError`. Элементы, которые нельзя сравнить
  (`[1, "a"]`), тоже дают `TypeError`.
- Обе сортировки стабильные, принимают `key`.

## Приоритетная очередь

`PriorityQueue` — dataclass на бинарной куче. Меньший приоритет выходит
первым, при равных приоритетах порядок добавления (FIFO).

| Операция | Что делает |
|---|---|
| `push(item, priority)` | добавить, приоритет должен быть числом |
| `pop()` | убрать и вернуть следующий |
| `peek()` | вернуть следующий, не убирая |
| `len(q)`, `bool(q)` | размер и непустота |
| `is_valid_heap()` | проверка инварианта кучи |

`pop` и `peek` на пустой очереди — `EmptyStructureError`.

```
AlgoError
├── InvalidInputError
└── EmptyStructureError
```

## Генераторы

`generate(kind, size, seed)` — `random`, `sorted`, `reversed`, `nearly_sorted`
(5% случайных обменов), `many_duplicates` (10 разных значений). Свой
`random.Random(seed)` в каждом вызове, глобальное состояние не трогается.
Один `seed` — один и тот же список, разные `seed` — разные списки.

## Benchmark

- 5 повторов (меньше нельзя, проверяется), размеры 100, 1 000 и 10 000, 5 типов
  входа, обе сортировки.
- Вход генерируется один раз на комбинацию, вне замера. Для каждого запуска
  делается своя копия `list(base)`, тоже вне замера.
- Время через `time.perf_counter`, считаются min, mean, median.
- В отчёте колонка `growth` — во сколько раз вырос средний замер
  времени по сравнению с предыдущим размером, и колонка `expected` — худшая
  ожидаемая сложность алгоритма (на отсортированном входе insertion линейный). Отчёт: `reports/benchmark.csv` и `reports/benchmark.md`.

Результат (Python 3.12, arm64), mean, мс:

| Алгоритм | Вход | n=100 | n=1000 | n=10000 |
|---|---|---:|---:|---:|
| insertion | random | 0.081 | 9.9 | 1102 |
| insertion | sorted | 0.004 | 0.05 | 0.57 |
| insertion | reversed | 0.161 | 18.8 | 2325 |
| merge | random | 0.056 | 0.70 | 9.6 |
| merge | reversed | 0.044 | 0.49 | 6.4 |

**Выводы.**
- `insertion_sort` растёт примерно в 100 раз при росте `n` в 10 раз — это O(n²).
  На отсортированном входе рост около 10 раз, то есть O(n). Худший вход —
  обратный, он вдвое медленнее случайного.
- `merge_sort` растёт примерно в 13 раз при росте `n` в 10 раз, что совпадает с
  `n log n` (ожидаемо 13.3). От типа входа почти не зависит.
- На 10 000 элементов на случайном и обратном входе merge быстрее insertion в 115–360 раз.

## Стиль кода

Все аргументы функций пакета передаются по имени, даже когда имя совпадает
со значением: `generate(kind=kind, size=size, seed=seed)`.

## Дополнительные задания

- **`key` (+3).** Параметр `key` у `insertion_sort`, `merge_sort`, `quickselect`;
  вызывается один раз на элемент.
- **Стабильность (+3).** Тест `test_sort_is_stable` в `tests/test_sorting.py`
  проверяет, что элементы с равным ключом идут в исходном порядке, для обеих
  сортировок.
- **Quickselect (+2).** `quickselect(items, k)` — k-й по возрастанию (с нуля),
  трёхстороннее разбиение со случайным опорным элементом (свой `Random(seed)`).
- **Автоотчёт benchmark (+2).** `scripts/run_benchmark.py` сам запускает
  измерения и пишет CSV и Markdown с таблицей, ростом времени и ожидаемой
  сложностью.

## Тесты

```bash
uv run pytest
uv run pytest --cov
```

Тесты не используют реальное время (benchmark проверяется на
подменённом таймере) и глобальный `random` (всегда `random.Random(seed)`).

## Демо для защиты

`uv run python scripts/demo.py` по порядку показывает всё, за что дают баллы:
Fibonacci и неверный ввод, обе сортировки (пустой список, дубликаты,
отрицательные, неизменность входа, `TypeError`, сравнение с `sorted`),
стабильность и `key`, очередь (`push`, `peek`, `pop`, пустая очередь, инвариант),
генераторы и seed, quickselect и небольшой benchmark. Последний блок показывает,
почему нельзя мерить на одном списке. Весь вывод занимает около 10 секунд.

## Защита

### 1. Сложность merge sort

Список делится пополам до длины 1: глубина рекурсии `log n`. На каждом уровне
все элементы сливаются за O(n). Итого O(n log n) всегда, и в лучшем, и в худшем
случае. Память O(n) на слитые списки. Сортировка стабильная: при равных ключах
`_merge` берёт элемент из левой половины.

### 2. Инвариант структуры данных в виде теста

Инвариант кучи: родитель не больше детей. Тест из `tests/test_priority_queue.py`:

```python
def test_heap_invariant_holds_after_every_operation():
    queue = PriorityQueue()
    for i, priority in enumerate(random_list(seed=7, size=100)):
        queue.push(item=i, priority=priority)
        assert queue.is_valid_heap()
    while queue:
        queue.pop()
        assert queue.is_valid_heap()
```

Ещё один пример инварианта: `len` растёт на 1 после `push` и падает на 1 после
`pop`.

### 3. Почему benchmark нельзя гонять на одном изменяемом списке

Сортировка (например, на месте) меняет список. Первый запуск получит случайный
массив, а все следующие уже отсортированный, и замеры будут про другой вход
(для insertion это O(n) вместо O(n²)). Поэтому для каждого запуска нужна свежая
копия `list(base)`, а создание и копирование входа делается вне измеряемого
времени.
