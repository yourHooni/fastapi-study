"""
    generator: lazy iterator, 데이터를 미리 만들지 않고 필요할 때마다 하나씩 생성하는 객체
        - yield: generator 생성 키워드
        - generator comprehension: generator 생성 표현식
"""
import time


def return_abc():
    """모든 결과 값을 메모리에 올리고 반환"""
    # return list("ABC")
    abc_list = []
    second = 0
    for ch in "ABC":
        time.sleep(1)
        print(second := second + 1)
        abc_list.append(ch)
    return abc_list


def yield_abc():
    """결과 값을 하나씩 메모리에 올림"""
    # yield "A"
    # yield "B"
    # yield "C"

    second = 0
    for ch in "ABC":
        time.sleep(1)
        print(second := second + 1)
        yield ch

    # yield from ["A", "B", "C"]


def generator_abc():
    """generator 표현식"""
    return (ch for ch in "ABC")


for c in return_abc():
    print("return ", c)

for c in yield_abc():
    print("yield ", c)

print("return ", return_abc())
y = yield_abc()
print("yield ", y)
print("yield next ", next(y))
print("yield next ", next(y))
print("yield next ", next(y))
g = generator_abc()
print("generator ", g)
print("generator next ", next(g))
print("generator next ", next(g))
print("generator next ", next(g))
