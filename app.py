import sys
from time import time
from operator import itemgetter
from src.farsi_spell_checker import FSpellChecker
from src.lm.lm_model import LMModel
from src.lm.language_model_gen import generate_lang_model, save_model, load_model
import src.lm.lm_compressor as compressor 
from src.tools.farsi_tokenizer import tokenize
from src.tools.edit_distant import generate_all_edist_words
from src.tools.text_loader import lazy_load_txt


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


def create_vocab_index():
    argv = sys.argv
    argc = len(argv)
    if argc < 3:
        print('arg1: path to model\n', 'arg2: output path\n')
        return
    path_model = argv[1]
    path_out = argv[2]
    model, n = load_model(path_model)
    vocab_index = compressor.create_vocabulary_index(model)
    compressor.save_vocabulary_index(vocab_index, path_out)


def compress_lm_model():
    argv = sys.argv
    argc = len(argv)
    if argc < 4:
        print ('arg1: path to vocabulary\n', 'arg2: path to model\n', 
                'arg3: output path\n')
        return
    path_vocab = argv[1]
    path_model = argv[2]
    path_out = argv[3]
    vocab_index = compressor.load_vocabulary_index(path_vocab)
    log_space = True
    model, n = load_model(path_model, log_space)
    compressed_model = compressor.compress(vocab_index, model, n)
    compressor.save_model(compressed_model, n, path_out, log_space)


def find_mistaken_words():
    argv = sys.argv
    argc = len(argv)
    if argc < 3:
        print('arg1: path to input files\narg2: output\n')
        return
    input_files = argv[1]
    outfile = argv[2]
    txts = lazy_load_txt(input_files)  # generator
    spell_checker = FSpellChecker(2)  # suggest 2 words
    spell_checker.max_edit_distance = 1  # maximum edit distance 1
    out = open(outfile, 'w')
    for txt in txts:
        corrections = spell_checker.spell_check(txt)
        comulation = dict()
        suggestions = dict()
        for mistake in corrections:
            tkn = mistake.token
            comulation[tkn] = comulation.get(tkn, 0) + 1
            if tkn not in suggestions:
                suggestions[tkn] = mistake.suggestions
        for tkn, c in comulation.items():
            suggestion = map(str, suggestions[tkn])
            line = f'{tkn}|{c}:' + ';'.join(suggestion)
            out.write(line+'\n')
    out.close()


def interactive():
    argv = sys.argv
    argc = len(argv)
    spell_checker = FSpellChecker(2) # suggest 2 words
    spell_checker.max_edit_distance = 2
    while True:
        line = input("> ")
        size = len(line)
        t_start = time()
        corrections = spell_checker.spell_check(line)
        t_end = time()
        for spell_mist in corrections:
            token = spell_mist.token
            suggestions = spell_mist.suggestions
            print (token, suggestions)
        print(f'time: {t_end - t_start} size: {size}')


def main():
    print('1: generate lm\n',
            '2: generate vocab index\n',
            '3: compress model\n',
            '4: generate mistake words list\n',
            '5: interactive')
    cmd = int(input())
    if cmd == 1:
        generate_lm()
    elif cmd == 2:
        create_vocab_index()
    elif cmd == 3:
        compress_lm_model()
    elif cmd == 4:
        find_mistaken_words()
    elif cmd == 5:
        interactive()


if __name__ == '__main__':
    main()

