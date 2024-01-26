user_data = []

while True:
    user_input = input("Enter data (type 'end' to finish): ")
    
    if user_input.lower() == 'end':
        break
    
    user_data.append(user_input)

print("User data:", user_data)
