from jellyfish import levenshtein_distance as levenshtein

def find_alike(odd_trans, rus_list, eng_word):
    dist_dict = {}
    for ru_word in rus_list:
        if ru_word in known:
            continue
        ldist = levenshtein(odd_trans, ru_word)

        dist_dict[ldist] = ru_word
        min_dist = min(list(dist_dict.keys()))
        if min_dist <= 2:
            return True, ru_word
        elif 2 < min_dist <= 4 and (len(ru_word) > 4 and len(eng_word) > 4):
            return False, ru_word


# requires file format as following: eng_words;translit;ru_words_from_site

infile = open('files\\amwine_parsed (2)-trans.csv', 'r', encoding='utf-8')
pair_list = infile.readlines()
infile.close()

del pair_list[0]
pairs, short, unsure_pairs, empty = set(), set(), set(), set()
known = set()
diff_len = []
n = 0

for pair in pair_list:
    eng_str, trans_str, rus_str = pair.strip().split(';')
    eng_list, trans_list, rus_list = eng_str.split(), trans_str.split(), rus_str.split()

    # if words can be associated one-to-one
    if len(eng_list) == len(rus_list) == 1:
        pairs.add((eng_list[0], rus_list[0]))

    # if association is unclear
    else:
        if len(eng_list) == len(trans_list):
            for i in range(len(eng_list)):
                eng_word, odd_word = eng_list[i], trans_list[i]
                search_res = find_alike(odd_word, rus_list, eng_word)
                if search_res:
                    is_firm, ru_word = search_res

                    # check if the levenshtein distance is less than 2
                    if is_firm:
                        if len(eng_word) > 2 and len(ru_word) > 2:
                            pairs.add((eng_word, ru_word))
                            known.add(ru_word)
                        else:
                            short.add((eng_word, ru_word))
                            known.add(ru_word)
                    else:
                        unsure_pairs.add((eng_word, ru_word))
                else:
                    empty.add((eng_word, rus_str))
        else:
            diff_len.append((eng_str, trans_str))

    n += 1
    if n % 200 == 0:
        print('{} lines done'.format(n))

firm_file = open('ready\\amwine_brands-firm(2).csv', 'w', encoding='utf-8')
shortie_file = open('ready\\amwine_brands-short(2).csv', 'w', encoding='utf-8')
doubt_file = open('ready\\amwine_brands-doubt(2).csv', 'w', encoding='utf-8')
notfound_file = open('ready\\amwine_brands-not_found(2).csv', 'w', encoding='utf-8')

firm_file.write('brand,alias\n')
shortie_file.write('brand,alias\n')
doubt_file.write('brand,alias\n')
notfound_file.write('brand,alias\n')

for pair in pairs:
    firm_file.write('{},{}\n'.format(pair[0], pair[1]))

for lil_pair in short:
    shortie_file.write('{},{}\n'.format(lil_pair[0], lil_pair[1]))

for dpair in unsure_pairs:
    doubt_file.write('{},{}\n'.format(dpair[0], dpair[1]))

for emp_pair in empty:
    notfound_file.write('{},{}\n'.format(emp_pair[0], emp_pair[1]))

print()
print('=' * 100)
if diff_len:
    print('words having different lengths'.upper())
    for diff_pair in diff_len:
        print(diff_pair[0], '-', diff_pair[1])
else:
    print('No strings having different lengths found.')

firm_file.close()
doubt_file.close()
notfound_file.close()
