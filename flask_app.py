# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"

@app.route('/')
def hello_world():
    celsius = input('Celsius: ')
    return 'Hello from Flask!' + fahrenheit_from(celsius)