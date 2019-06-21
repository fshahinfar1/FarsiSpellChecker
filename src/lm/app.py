import sys
from language_model_gen import generate_lang_model, save_model


def main():
    """
    python app.py (corpus_dir|corpus_file) (output_file_prefix) (ngram: 1gram, 2gram, 3gram, ...)
    """
    argv = sys.argv
    argc = len(argv)
    if argc < 3:
        print('arg1: path to corpus \narg2: output prefix \narg3: an integer  (1gram, 2gram, ...)\n')
        return
    lbl_train = argv[1]
    model_prefix = argv[2]
    N = int(argv[3])
    if N < 1:
        print('N should be an integer starting from one')
        return
   
    model = generate_lang_model(N, lbl_train)
    save_model(model, './{0}.{1}gram.lm'.format(model_prefix, N))


if __name__ == '__main__':
    main()

