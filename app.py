import sys
from operator import itemgetter
from src.lm.language_model_gen import generate_lang_model, save_model, load_train_text
from src.lm.lm_model import LMModel
from src.tools.farsi_tokenizer import tokenize
from src.constants import ALPHABET
from src.tools.edit_distant import generate_all_edist_words


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
    if argc < 4:
        print('arg1: path to LM \narg2: path to input files\n3: output\n')
        return
    model_path = argv[1]
    input_files = argv[2]
    outfile = argv[3]
    model = LMModel(0)
    model.load_from_file(model_path)
    txt = load_train_text(input_files) 
    tokens = tokenize(txt) 
    mistakes = dict()
    for tkn in tokens:
        if tkn not in model._model:
            mistakes[tkn] = mistakes.get(tkn, 0) + 1
    suggestions = dict()
    for tkn in mistakes:
        # all words with edit distant of 1
        possible_words = generate_all_edist_words(tkn, 1)
        possible_words = filter(lambda x: x in model._model, possible_words)
        if suggestions.get(tkn) is None:
            suggestions[tkn] = list()
        for suggestion in possible_words:
           suggestions[tkn].append(suggestion) 
    items = sorted(mistakes.items(), key=itemgetter(1), reverse=True)
    with open(outfile, 'w') as out:
        for tkn, c in items:
            line = f'{tkn}|{c}:' + ';'.join(suggestions[tkn])
            out.write(line+'\n')


def main():
    print('1: generate lm\n2: generate mistake words list\n3: interactive')
    cmd = int(input())
    if cmd == 1:
        generate_lm()
    elif cmd == 2:
        find_mistaken_words()


if __name__ == '__main__':
    main()

