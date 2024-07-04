#!/usr/bin/env python

# docker run --rm -it -v .:/app python:alpine /app/hello-world.py

print('Hello World!')

num1 = 2
num2 = 3
sum = num1 + num2

print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))
