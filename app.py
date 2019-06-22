import sys
from operator import itemgetter
from src.lm.language_model_gen import generate_lang_model, save_model, load_train_text
from src.lm.lm_model import LMModel
from src.tools.farsi_tokenizer import tokenize
from src.tools.edit_distant import generate_all_edist_words
from src.farsi_spell_checker import FSpellChecker


def generate_lm():
    """
    python app.py (corpus_dir|corpus_file) (output_file_prefix) (ngram: 1gram, 2gram, 3gram, ...)
    """
    argv = sys.argv
    argc = len(argv)
    if argc < 4:
        print('arg1: path to corpus \narg2: output prefix \narg3: an integer  (1gram, 2gram, ...)\n')
        return
    lbl_train = argv[1]
    model_prefix = argv[2]
    N = int(argv[3])
    if N < 1:
        print('N should be an integer starting from one')
        return
   
    model = generate_lang_model(N, lbl_train)
    save_model(model, N, './{0}.{1}gram.lm'.format(model_prefix, N))


def find_mistaken_words():
    argv = sys.argv
    argc = len(argv)
    if argc < 3:
        print('arg1: path to input files\narg2: output\n')
        return
    input_files = argv[1]
    outfile = argv[2]
    txt = load_train_text(input_files) 
    spell_checker = FSpellChecker()
    spell_checker.max_edit_distance = 1
    corrections = spell_checker.spell_check(txt)
    comulation = dict()
    suggestions = dict()
    for mistake in corrections:
        tkn = mistake.token
        comulation[tkn] = comulation.get(tkn, 0) + 1
        if tkn not in suggestions:
            suggestions[tkn] = mistake.suggestions
    with open(outfile, 'w') as out:
        for tkn, c in comulation.items():
            suggestion = map(str, suggestions[tkn])
            line = f'{tkn}|{c}:' + ';'.join(suggestion)
            out.write(line+'\n')


def interactive():
    argv = sys.argv
    argc = len(argv)
    if argc < 2:
        print('arg1: path to LM\n')
        return
    model_path = argv[1]
    model = LMModel(0)
    model.load_from_file(model_path)
    while True:
        line = input()
        tokens = tokenize(line)
        mistakes = set()
        for tkn in tokens:
            if tkn not in model._model:
                mistakes.add(tkn)
        for misspelled in mistakes:
            possible_words = generate_all_edist_words(misspelled, 2)
            possible_words = filter(lambda x: x in model._model, possible_words)
            line = f'{misspelled}: '
            for suggested in possible_words:
                line += f'{suggested}, '
            print(line)


def main():
    print('1: generate lm\n2: generate mistake words list\n3: interactive')
    cmd = int(input())
    if cmd == 1:
        generate_lm()
    elif cmd == 2:
        find_mistaken_words()
    elif cmd == 3:
        interactive()


if __name__ == '__main__':
    main()

