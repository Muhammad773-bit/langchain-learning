from agent import load_csv, ask_llm

df = load_csv("data/sales_data.csv")

question = "what is the maximum quantity of furniture"

print(f"Question: {question}\n")

code = ask_llm(question, df)

print("Raw LLM response length:", len(code))
print("Raw LLM response (repr):", repr(code))

# Let's check for all newline variations
print("\nChecking for various whitespace:")
print("Has \\n:", '\n' in code)
print("Has \\r:", '\r' in code)
print("Has \\t:", '\t' in code)

# Now let's clean it properly
clean_code = code.strip()

# Extract between backticks if they exist
if '```' in clean_code:
    print("\nFound triple backticks")
    parts = clean_code.split('```')
    clean_code = parts[1].strip()
    if clean_code.startswith('python'):
        clean_code = clean_code[6:].strip()

print("\nCleaned code (repr):", repr(clean_code))
print("Cleaned code (normal):", clean_code)

# Remove newlines
clean_code = clean_code.replace('\n', ' ').replace('\r', '')
clean_code = clean_code.strip()

print("\nAfter newline removal (repr):", repr(clean_code))

# Test
local_vars = {"df": df}
try:
    result = eval(clean_code, {}, local_vars)
    print("\nSUCCESS! Result:", result)
except SyntaxError as e:
    print(f"\nSyntaxError: {e}")
    print("Problem likely with newline in string literal")
except Exception as e:
    print(f"\nError: {e}")
