from collections import defaultdict

def calculate_stats(data):
    description_totals = defaultdict(float)
    
    for row in data:
        description = row[4]  # Description is at index 4
        amount = row[5]  # Amount is at index 5
        description_totals[description] += amount
    
    income = []
    outgoings = []
    
    for description, total in description_totals.items():
        if total > 0:
            income.append((description, total))
        else:
            outgoings.append((description, abs(total)))  # Use absolute value for outgoings
    
    # Sort income and outgoings lists
    income.sort(key=lambda x: x[1], reverse=True)
    outgoings.sort(key=lambda x: x[1], reverse=True)  # Sort from highest to lowest
    
    total_income = sum(amount for _, amount in income)
    total_outgoings = sum(amount for _, amount in outgoings)
    
    return total_income, total_outgoings, income, outgoings