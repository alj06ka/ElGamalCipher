from time import time


def fast_power(base, power):
    result = 1
    while power > 0:
        if power % 2:
            power -= 1
            result *= base
        else:
            power >>= 1
            base *= base
    return result


def fast_power_recur(base, power):
    if power == 0:
        return 1
    if power == -1:
        return 1. / base
    if power % 2 == 1:
        return fast_power_recur(base, power - 1)* base
    else:
        result = fast_power_recur(base, power / 2)
        return result * result


if __name__ == '__main__':
    """
    Unit for testing speed between different power calculating algorithms
    Comparing:
        - Included python algorithm
        - Fast power non-recursive algorithm
        - Fast power recursive algorithm
    Result:
        Python algorithm is the fastest
    """
    def lines(func):
        def wrapper(*args, **kwargs):
            print('-------------------------')
            func(*args, **kwargs)
            print('-------------------------\n')

        return wrapper


    def catch_time(func):
        def wrapper(*args, **kwargs):
            _time = time()
            funciton_result = func(*args, **kwargs)
            _time = time() - _time
            return {'time': _time, 'result': funciton_result}

        return wrapper


    @lines
    def test_power(base, power):
        def _print_time(time, result):
            print(f'Done! Total time: {time}, result: {result}')

        @catch_time
        def _python_power(base, power):
            print('Python power...')
            return base ** power

        @catch_time
        def _fast_power(base, power):
            print('Fast power...')
            return fast_power(base, power)

        @catch_time
        def _fast_power_recur(base, power):
            print('Fast power recursive...')
            return fast_power_recur(base, power)

        print(f'Calculating {base}^{power}...')
        result_python_power = _python_power(base, power)
        _print_time(result_python_power['time'], result_python_power['result'])

        result_fast_power = _fast_power(base, power)
        _print_time(result_fast_power['time'], result_fast_power['result'])

        result_fast_power_recur = _fast_power_recur(base, power)
        _print_time(result_fast_power_recur['time'], result_fast_power_recur['result'])

        time_list = [result_python_power['time'], result_fast_power['time'], result_fast_power_recur['time']]
        min_time = min(time_list)
        if min_time == time_list[0]:
            print('Python\'s power is the fastest')
        elif min_time == time_list[1]:
            print('Fast power is the fastest')
        else:
            print('Fast power (recursive) is the fastest')

    print('Fast power testing:')
    print('Test 1')
    test_power(10, 2)
    print('Test 2')
    test_power(10, 20)
    print('Test 3')
    test_power(10, 200)
    print('Test 4')
    test_power(10, 2000)
    print('Test 5')
    test_power(10, 20000)
    print('Test 6')
    test_power(10, 20000)
    print('Test 7')
    test_power(10000, 20000)
    print('Test 8')
    test_power(1000000000, 2000)
    print('Test 9')
    test_power(1000000000000, 2000)
    print('Test 10')
    test_power(1000000000000, 10000)
