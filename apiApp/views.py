import math
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# URL for the Numbers API
NUMBERS_API_URL = "http://numbersapi.com/{}?json"


def is_armstrong(n: int) -> bool:
    """
    Check if a number is an Armstrong number (using the absolute value).
    An Armstrong number is one that is equal to the sum of its own digits each raised to the power
    of the number of digits.
    """
    n = abs(n)
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n


def is_perfect(n: int) -> bool:
    """
    Check if a number is perfect.
    A perfect number is one that is equal to the sum of its proper divisors.
    Here, only positive numbers can be perfect.
    """
    if n <= 0:
        return False 
    return sum(i for i in range(1, n) if n % i == 0) == n


class ClassifyNumberAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve the "number" query parameter.
        number_str = request.query_params.get("number")
        if number_str is None:
            return Response(
                {"error": "The 'number' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            number = int(number_str)
        except ValueError:
            # If the conversion fails, echo the non-numeric input.
            return Response(
                {"number": number_str, "message": f"Non-numeric input received. Echoing input: {number_str}"},
                status=status.HTTP_200_OK
            )

        # Calculate the mathematical properties.
        armstrong = is_armstrong(number)
        perfect = is_perfect(number)
        # Check for prime only numbers greater than 1 can be prime.
        is_prime = number > 1 and all(number % i != 0 for i in range(2, int(math.sqrt(number)) + 1))
        is_odd = number % 2 != 0

        properties = []
        if armstrong:
            properties.append("armstrong")
        properties.append("odd" if is_odd else "even")

        # Calculate the digit sum using absolute value so negative sign is ignored.
        digit_sum = sum(int(digit) for digit in str(abs(number)))

        # Fetch a fun fact from the Numbers API.
        try:
            response = requests.get(NUMBERS_API_URL.format(number))
            if response.status_code == 200:
                fact_data = response.json()
                fun_fact = fact_data.get("text", "No fun fact found.")
            else:
                fun_fact = "No fun fact found."
        except requests.RequestException:
            fun_fact = f"No fun fact returned from the numbers API for the number: {number}"

        # response data.
        result = {
            "number": number,
            "is_prime": is_prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
        return Response(result, status=status.HTTP_200_OK)
