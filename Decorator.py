import os
from datetime import datetime
from functools import wraps

def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        with open('main.log', 'a') as f:
            if os.path.getsize('main.log') == 0:
                f.write(f"Дата и время вызова, имя функции, аргументы, результат \n")
            result = old_function(*args, **kwargs)
            data_time = datetime.now()
            data_func = old_function.__name__
            args_list = []
            for arg in args:
                args_list.append(str(arg))
            for key, value in kwargs.items():
                args_list.append(f"{key}={value}")
            data_arg = ", ".join(args_list) if args_list else None
            data_result = result
            f.write(f"{str(data_time)}, {data_func}, {data_arg}, {data_result} \n")
        return result
    return new_function

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
