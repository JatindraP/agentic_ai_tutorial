import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Jatindra Nath Pattanaik"

tokens = enc.encode(text)

#Tokens:  [25216, 3274, 0, 3673, 1308, 382, 643, 266, 66594, 125369, 111346, 1480, 507]
print("Tokens: ",tokens)

decoaded = enc.decode(tokens)

print("Decoadec : ",decoaded)