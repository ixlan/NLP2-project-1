from utils import tokenize_corpora_to_ids
import special_symbols
from time import gmtime, strftime
import re

def train_model(model, vocab_french, vocab_english, french_file_path, english_file_path, iterations=10,
                word_preprocessor=None):
    # load data
    print 'pre-loading data into RAM'
    parallel_corpus = tokenize_corpora_to_ids(vocab_french, vocab_english,
                                              french_file_path=french_file_path,
                                              english_file_path=english_file_path,
                                              word_preprocessor=word_preprocessor)
    print 'done'
    print '----------'

    # train
    print 'starting training'
    print '----------'
    for iter in range(iterations):
        print "iteration nr %d" % iter
        model.train(parallel_corpus)
        log_likelihood = model.compute_log_likelihood(parallel_corpus)
        print "Log-likelihood is: %.2f" % log_likelihood
        print '----------'


# a function for cleaning tokens/words
def word_preprocessor(word):
    # URL
    if re.match(r"^(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})$", word):
        return special_symbols.URL_TOKEN
    # FLOAT
    if re.match(r'^([0-9]+\.)[0-9]+$', word):
        return special_symbols.FLOAT_TOKEN
    word = re.sub(r'[^\w\'\-]|[\'\-\_]{2,}', "", word)
    if len(word) == 1:
        word = re.sub(r'[^\daiu]', '', word)
    return word

def log_info(log_string):
    time_string = strftime("%H:%M:%S", gmtime())
    print("%s [INFO]: %s" % (time_string, log_string))
