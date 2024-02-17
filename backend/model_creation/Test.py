import string

body = "HEEEllo's my. nice TO meet's you!??"
body = body.lower()
body = body.replace("'s", '')
body = body.translate(str.maketrans("", "", string.punctuation))
print(body)