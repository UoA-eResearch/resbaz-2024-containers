// docker run --rm -it -v .:/app node:alpine node /app/hello-world.js

var util = require('util');

console.log('Hello World!');

num1 = 2;
num2 = 3;
sum = num1 + num2;

console.log(util.format('The sum of %d and %d is %d', num1, num2, sum));
