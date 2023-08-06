import csv


with open('Cleaned - ISO-20275 - 2020-11-19.csv', newline='', encoding='utf-8') as input_file:
	with open('Cleaned - ISO-20275 - 2020-11-19 - Trimmed.csv', 'w', newline='', encoding='utf-8') as output_file:
		spamreader = csv.reader(input_file, delimiter=',', quotechar='"')
		spamwriter = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
		for row in spamreader:
			new_row = []
			for i, column in enumerate(row):
				if i == 15:
					new_row.append(column)
					continue
				tokens = column.split(';')
				new_column = []
				for token in tokens:
					token = token.strip()
					if len(token) == 0:
						continue
					else:
						new_column.append(token)
				new_row.append(';'.join(new_column))
			spamwriter.writerow(new_row)
