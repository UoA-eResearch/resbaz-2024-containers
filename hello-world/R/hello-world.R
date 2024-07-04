# docker run --rm -it -v ./:/app -w /app rocker/r-base R -f hello-world.R
# docker run --rm -it -e PASSWORD=password -p 8787:8787 rocker/rstudio

print("Hello World!")

num1 = 2
num2 = 3
sum = num1 + num2

print(sprintf("The sum of %d and %d is %d", num1, num2, sum))
