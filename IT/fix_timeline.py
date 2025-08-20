import re

# Read the file
with open('it.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic line
content = content.replace("x_start='Timeline'", "x_start='Start_Date', x_end='End_Date'")

# Write back to file
with open('it.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Timeline issue fixed!")
