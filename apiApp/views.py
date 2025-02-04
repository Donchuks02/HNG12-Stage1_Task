from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(num: int) -> bool:
    if num < 6:
        return False

    sum_of_divisors = 1
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            sum_of_divisors += i
            if i != num // i:
                sum_of_divisors += num // i

    return sum_of_divisors == num

def is_armstrong(num: int) -> bool:
    length = len(str(num))
    digit_power_sum = 0
    temp = num

    while temp != 0:
        rem = temp % 10
        digit_power_sum += rem ** length
        temp //= 10

    return digit_power_sum == num

def digit_sum(n):
    return sum(map(int, str(n)))

def is_even(num: int) -> str:
    return "even" if num % 2 == 0 else "odd"

def properties(num: int) -> list[str]:
    props = [is_even(num)]
    if is_armstrong(num):
        props.append("armstrong")
    return props

@api_view(['GET'])
def classify_number(request):
    number = request.query_params.get('number', '371')  # Default to 371 if no number is provided
    if not number.isdigit():
        return Response({'number': 'alphabet', 'error': True}, status=400)
    
    number = int(number)
    props = properties(number)
    if is_prime(number):
        props.append('prime')
    if is_perfect(number):
        props.append('perfect')
    
    response = requests.get(f'http://numbersapi.com/{number}/math')
    fun_fact = response.text if response.status_code == 200 else 'No fun fact available'

    return Response({
        'number': number,
        'is_prime': is_prime(number),
        'is_perfect': is_perfect(number),
        'properties': props,
        'digit_sum': digit_sum(number),
        'fun_fact': fun_fact
    })


def home_redirect(request):
    return redirect('/api/classify-number/')