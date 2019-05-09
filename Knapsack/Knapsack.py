def knapsack(capacity, weights, values, n):
	if n == 0 or capacity == 0:
		return 0
	if(weights[n-1] > capacity):
		return knapsack(capacity, weights, values, n-1)
	else:
		return max(values[n-1] + knapsack(capacity-weights[n-1], weights, values, n-1), knapsack(capacity, weights, values, n-1))
		
values = [3, 5, 6, 3, 4, 4]
weights = [35, 55, 60, 30, 40, 40]
capacity = 61
n = len(values)
print(str(knapsack(capacity, weights, values, n)))
		