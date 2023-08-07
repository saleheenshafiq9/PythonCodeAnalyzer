def large_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

# Example usage:
numbers_list = [1000000, 2000000, 3000000, 4000000, 5000000]
result = large_sum(numbers_list)
print("The sum of the numbers is:", result)
