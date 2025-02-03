from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
# Create your views here.


# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True



def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = list(map(int, str(n)))
    return n == sum(d ** len(digits) for d in digits)

# Function to calculate the sum of digits of a number
def digit_sum(n):
    return sum(map(int, str(n)))    


@api_view(['GET'])
def classify_number(request):
    number = request.query_params.get('number')
    if not number or not number.isdigit():
        return Response({'number': 'alphabet', 'error': True}, status=400)
    
    number = int(number)
    properties = []
    if is_prime(number):
        properties.append('prime')
    if is_perfect(number):
        properties.append('perfect')
    if is_armstrong(number):
        properties.append('armstrong')
    if number % 2 == 0:
        properties.append('even')
    else:
        properties.append('odd')
    
    response = requests.get(f'http://numbersapi.com/{number}')
    fun_fact = response.text if response.status_code == 200 else 'No fun fact available'

    return Response({'number': number, 'is_prime': is_prime(number), 'is_perfect': is_perfect(number),'properties': properties,'digit_sum': digit_sum(number),  'fun_fact': fun_fact})