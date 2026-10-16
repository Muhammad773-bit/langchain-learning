# # main.py
# from agent import load_csv, ask_llm
# import re

# df = load_csv("data/sales_data.csv")

# question = input("Ask your question: ")

# code = ask_llm(question, df)

# print("\nGenerated pandas code:")
# print(code)

# # Clean the code - extract content between backticks and remove all newlines
# clean_code = code.strip()

# # If it has backticks, extract content between them
# if '```' in clean_code:
#     parts = clean_code.split('```')
#     if len(parts) >= 2:
#         clean_code = parts[1]
#         if clean_code.startswith('python'):
#             clean_code = clean_code[6:]

# # Remove ALL newlines from the code
# clean_code = clean_code.replace('\n', ' ').replace('\r', '')
# # Normalize multiple spaces
# clean_code = re.sub(r'\s+', ' ', clean_code)
# clean_code = clean_code.strip()

# # SAFE execution context
# local_vars = {"df": df}
# try:
#     # Use exec() for statements (including assignments), eval() only works for expressions
#     exec(clean_code, {}, local_vars)
    
#     # Find the result variable (usually the first new variable created)
#     result_vars = {k: v for k, v in local_vars.items() if k != 'df'}
#     if result_vars:
#         result = list(result_vars.values())[0]
#         print("\nResult:")
#         print(result)
#     else:
#         print("\nCode executed but no result variable created")
# except Exception as e:
#     print(f"Error executing code: {e}")
