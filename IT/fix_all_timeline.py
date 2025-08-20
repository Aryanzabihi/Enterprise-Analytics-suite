import re

# Read the file
with open('it.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original file size:", len(content))

# Find all instances of the old structure
old_pattern = r"'Phase':\s*\[.*?'Timeline':\s*\[.*?'Focus_Area':\s*\[.*?'Priority':\s*\[.*?'Estimated_Effort':\s*\["
matches = re.findall(old_pattern, content, re.DOTALL)
print(f"Found {len(matches)} instances of old structure")

# Replace all instances of the old structure with the new one
new_structure = """'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
        'Start_Date': ['2025-01-01', '2025-04-01', '2025-07-01', '2025-10-01'],
        'End_Date': ['2025-03-31', '2025-06-30', '2025-12-31', '2026-05-31'],
        'Focus_Area': ['Core Systems', 'External APIs', 'Advanced Analytics', 'AI Integration'],
        'Priority': ['High', 'High', 'Medium', 'Medium'],
        'Estimated_Effort': ['3 months', '4 months', '6 months', '8 months']"""

# Replace the old structure
content = re.sub(r"'Phase':\s*\[.*?'Timeline':\s*\[.*?'Focus_Area':\s*\[.*?'Priority':\s*\[.*?'Estimated_Effort':\s*\[.*?\]", 
                new_structure, content, flags=re.DOTALL)

# Also replace any remaining x_start='Timeline' with the correct parameters
content = content.replace("x_start='Timeline'", "x_start='Start_Date', x_end='End_Date'")

# Write back to file
with open('it.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("All timeline issues fixed!")
print("New file size:", len(content))
