import math
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def is_prime(num):
    """Check if a number is prime."""
    if num < 2:
        return False
    # Check divisibility up to half the number (simple approach)
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            return False
    return True


def is_perfect(num):
    """Check if a number is a perfect number (i.e., equals the sum of its proper divisors)."""
    if num < 6:
        return False
    sum_of_divisors = 1  # Start with 1, which is a proper divisor.
    # Loop through potential divisors up to sqrt(num)
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            sum_of_divisors += i
            complement = num // i
            if complement != i:
                sum_of_divisors += complement
    return sum_of_divisors == num


def is_armstrong(num):
    """Check if a number is an Armstrong (narcissistic) number."""
    digits = str(num)
    length = len(digits)
    total = sum(int(digit) ** length for digit in digits)
    return total == num


def is_even(num):
    """Return 'even' or 'odd' depending on the parity of the number."""
    return "even" if num % 2 == 0 else "odd"


def get_properties(num):
    """Return a list of properties for the given number."""
    properties = [is_even(num)]
    if is_armstrong(num):
        # If Armstrong, insert "armstrong" at the beginning.
        properties.insert(0, "armstrong")
    return properties


def get_digit_sum(num):
    """Calculate and return the sum of the digits of the number."""
    return sum(int(digit) for digit in str(num))


def get_fun_fact(num):
    """
    Fetch a fun fact about the number from the Numbers API.
    This function makes a synchronous HTTP GET request.
    """
    try:
        url = f"http://numbersapi.com/{num}/math"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"No fun fact returned from the numbers API for the number: {num}"
    except requests.RequestException:
        return f"No fun fact returned from the numbers API for the number: {num}"



class ClassifyNumberView(APIView):
    def get(self, request, format=None):
        # Retrieve the "number" query parameter; default to "371" if not provided.
        number_str = request.query_params.get('number', '371')

        # Validate and convert the parameter to an integer.
        try:
            num = int(number_str)
        except ValueError:
            return Response(
                {"number": "alphabet", "error": True},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assemble the response dictionary.
        result = {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": get_properties(num),
            "digit_sum": get_digit_sum(num),
            "fun_fact": get_fun_fact(num)
        }

        return Response(result, status=status.HTTP_200_OK)