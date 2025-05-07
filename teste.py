from secrets import token_urlsafe
from random import shuffle

token = list(token_urlsafe(16))
print(token)

shuffle(token)

slug = ''
for x in token:
      slug+=x

print(slug)