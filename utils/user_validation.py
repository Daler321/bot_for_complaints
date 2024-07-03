def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())

def isValidName(name):
  nameArray = name.split(' ')
  if len(nameArray) != 2:
    return False
  if not (nameArray[0][0].isupper() and nameArray[1][0].isupper()):
    return False
  if not (match(nameArray[0][0]) and match(nameArray[1][0])):
    return False
  return True

def isValidNumber(number):
  if not number.startswith('+7'):
    return False
  if len(number) != 12:
    return False
  if not number[1:].isdigit():
    return False
  return True