import re


def replacer(word_string, ngrams_dict):
     word_list = word_string.split()
     # replacing the needed ngrams
     for i in range(len(word_list)):
         for ngram in ngrams_dict:
             word_list[i] = re.sub(ngram, ngrams_dict[ngram], word_list[i])
     new_string = ' '.join(word_list)
     return new_string


def trans_separate(word):
    single_letters_dict = {'\Ab\Z':'би', '\Ac\Z':'си', '\Ad\Z':'ди', '\Af\Z':'эф',
                           '\Ag\Z':'джи', '\Ah\Z':'эйч', '\Aj\Z':'джей', '\Ak\Z':'кей',
                           '\Al\Z':'эль', '\Am\Z':'эм', '\An\Z':'эн', '\Ap\Z':'пи',
                           '\Aq\Z':'кью', '\Ar\Z':'эр', '\As\Z':'эс', '\At\Z':'ти',
                           '\Av\Z':'ви', '\Aw\Z':'дабл ю', '\Ax\Z':'икс', '\Az\Z':'зед',
                           '\Aa\Z':'эй', '\Ao\Z':'оу', '\Ai\Z':'ай', '\Au\Z':'ю',
                           '\Ae\Z':'и', '\Ay\Z':'вай'}
    new_word = replacer(word, single_letters_dict)
    return new_word


def trans_long_ngrams(word):
    long_ngram_dict = {'ya':'я', '\Aand\Z':'энд',
                       'eaux\Z': 'о', 'beaut': 'бьют', 'eau': 'о', 'ogne\Z': 'он',
                       'gnie': 'йн', 'agne': 'ейн', 'ouge': 'уж', 'oix': 'уа', 'iei': 'ье',
                       'oux': 'о',
                       'tsch': 'ч', 'sch': 'ш', 'chs': 'хс',
                       'cch':'чч', 'zz': 'цц',
                       'sh': 'ш', 'you':'ю', 'chr':'кр', 'scq':'ск',
                       'ch': 'х', 'tz': 'ц', 'sp': 'шп',
                       'ck': 'к', 'ph': 'ф', 'qu': 'кв',
                       'eh': 'е', 'je': 'е', 'ju': 'ю', 'ja': 'я'}
    new_word = replacer(word, long_ngram_dict)
    return new_word


def condit_ngrams(word):
    condit_ngrams_dict = {'(?<=[euioay])s(?=[euioay])':'з',
                          'l(?![euioaylk])':'ль',
                          '\Ay(?=[euioa])':'й',
                          '\Ae(?![euioay-])':'э',
                          '(?<=[euioa])y\Z':'й',
                          '(?<![euioa])y\Z':'и',
                          '(?<=\w{3})e\Z': ''}
    new_word = replacer(word, condit_ngrams_dict)
    return new_word


def trans_short_ngrams(word):
    short_ngrams_dict = {'qu':'кв', 'ch':'ч', 'sh':'ш', 'ck':'к', 'th':'т',
                         'ph':'ф', 'sc':'ск', 'you':'ю'}
    new_word = replacer(word, short_ngrams_dict)
    return new_word


def trans_literals(word):
    ngrams_dict = {'b':'б', 'c':'к', 'd':'д', 'f':'ф', 'g':'г', 'h':'х',
                   'j':'й', 'k':'к', 'l':'л', 'm':'м', 'n':'н', 'p':'п',
                   'q':'к', 'r':'р', 's':'с', 't':'т', 'v':'в', 'w':'в',
                   'x':'кс', 'z':'з', 'a+':'а',  'e+':'е',  'i+':'и',
                   'u+':'у', 'o+':'о',  'y+':'и',
                   'é': 'е', 'è': 'е', 'à': 'а', 'ù': 'у',
                   'ê': 'е', 'â': 'а', 'ô': 'о', 'î': 'и', 'û': 'у',
                   'ë': 'е', 'ï': 'и', 'ü': 'у', 'ÿ': 'и', 'ç': 'с'}
    new_word = replacer(word, ngrams_dict)
    return new_word


def process(word):
    sg_letters_replaced = trans_separate(word)
    long_ngrams_replaced = trans_long_ngrams(sg_letters_replaced)
    ends_replaced = condit_ngrams(long_ngrams_replaced)
    short_ngrams_replaced = trans_short_ngrams(ends_replaced)
    simple_ngrams_replaced = trans_literals(short_ngrams_replaced)
    return simple_ngrams_replaced

