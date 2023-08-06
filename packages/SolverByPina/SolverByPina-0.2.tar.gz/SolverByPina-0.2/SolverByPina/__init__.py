global all_variants
all_variants = []


def generate_cycle(count, word, count_letters, save, variant=''):
	if count > 1:
		for i in word:
			variant += i
			generate_cycle(count-1, word, count_letters, save, variant)
			variant = variant[:-1]
	else:
		for i in word:
			all_variants.append(variant+i)
		return 0

def first_letter(letters):
	global all_variants
	count = 0
	for i in all_variants:
		if i[0] in letters:
			count += 1
	return count

def count_of_variat_first_letter(count_letters, word, letters):
	save= ''
	for i in range(count_letters):
		save+=word[0]
	generate_cycle(count_letters, word, count_letters, save)
	print(first_letter(letters))

def first_and_last_letter(start_letters, end_letters):
	global all_variants
	count = 0
	for i in all_variants:
		if i[0] in start_letters and i[-1] in end_letters:
			count += 1
	return count

def count_of_variat_first_and_last_letter(count_letters, word, start_letters, end_letters):
	save= ''
	for i in range(count_letters):
		save+=word[0]
	generate_cycle(count_letters, word, count_letters, save)
	print(first_and_last_letter(start_letters, end_letters))

def number_of_letter_repetitions(letter, count_letters_repeat):
	global all_variants
	count = 0
	for i in all_variants:
		if i.count(letter) == count_letters_repeat:
			count += 1
	return count

def count_of_variat_number_of_letter_repetitions(count_letters, word, letter, count_letters_repeat):
	save= ''
	for i in range(count_letters):
		save+=word[0]
	generate_cycle(count_letters, word, count_letters, save)
	print(number_of_letter_repetitions(letter, count_letters_repeat))

def help():
	print('count_of_variat_first_letter(кол-во букв в коде, слово, первые буквы в виде массива)')
	print('count_of_variat_first_and_last_letter(кол-во букв в коде, слово, первые буквы в виде массива, последние буквы в виде массива)')
	print('count_of_variat_number_of_letter_repetitions(кол-во букв в коде, слово, буква, кол-во повторений)')



