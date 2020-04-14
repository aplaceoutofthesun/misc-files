#!/usr/bin/env python3
#
"""N-Grams and Markov Chains.

Notes from Allison Parrish's Jupyter Notebook:
https://github.com/aparrish/rwet/blob/master/ngrams-and-markov-chains.ipynb
"""


from collections import Counter
import random

# pylint: disable=C0103

# Small 'pretty printer' function
def neat_print(lst):
    "Small function to neaten up the output. Nothing fancy..."
    if isinstance(lst, dict):
        for i in lst.items():
            print(i)
    else:
        for i in lst:
            print(i)
    print('-' * 80)


# N-gram functions
def ngrams(text, n=2):
    "Originally defined in 'useful.py' from Chiphuyen."
    ngram_list = []
    for i in range(len(text) - 1 + n):
        if len(text[i:i+n]) > 1:
            ngram_list.append(text[i:i+n])
    return ngram_list

def ngrams_for_seq(n, seq):
    "Function from Parrish, using a tuple for the values."
    return [tuple(seq[i:i+n]) for i in range(len(seq) - n + 1)]

# Markov model functions.

def add_to_model(model, n, seq):
    """Iterates over every index in seq, producing n-gram of desired
        length before adding the keys and values to the dictionary as
        necessary.
    """
    # Copy seq and append None to the end.
    seq = list(seq[:]) + [None]

    for i in range(len(seq) - n):
        # Tuple because it is the dict's key.
        gram = tuple(seq[i:i+n])
        next_item = seq[i+n]

        if gram not in model:
            model[gram] = []
        model[gram].append(next_item)

def markov_model(n, seq):
    model = {}
    add_to_model(model, n, seq)
    return model

def gen_from_model(n, model, start=None, max_gen=100):
    if start is None:
        start = random.choice(list(model.keys()))
    output = list(start)
    for _ in range(max_gen):
        start = tuple(output[-n:])
        next_item = random.choice(model[start])
        if next_item is None:
            break
        output.append(next_item)
    return output

def markov_model_from_sequences(n, sequences):
    """Creates a model, adding each iterm from a list to the model as a
    separate item. Returns the combined model.
    """
    model = {}
    for item in sequences:
        add_to_model(model, n, item)
    return model

def markov_generate_from_seqs(n, seqs, count, max_gen=100):
    starts = [item[:n] for item in seqs if len(item) >= n]
    model = markov_model_from_sequences(n, seqs)
    return [gen_from_model(n, model, random.choice(starts), max_gen)
            for i in range(count)]

def markov_generate_from_lines_in_file(ngram_len, filehandle,
                                       count, level='char', max_gen=100):
    glue = '' if level == 'char' else ' '
    if level == 'char':
        sequences = [item.strip()
                     for item in filehandle.readlines()]
    elif level == 'word':
        sequences = [item.strip().split()
                     for item in filehandle.readlines()]

    generated = markov_generate_from_seqs(ngram_len,
                                          sequences,
                                          count,
                                          max_gen)
    return [glue.join(item) for item in generated]

# ----------------------------------------------------------------------------

def about_tuples():
    """Where possible, consider using the tuple.
    A data structure similar to lists, created with parentheses or the 'tuple'
    function.

    Tuples are, however, immutable: Their values cannot be changed once the
    tuple has been created.
    """
    example = ("alpha", "beta", "gamma", "delta")
    print(example, type(example))

    # Values can be accessed via indexing (like lists):
    print(f"Last Item: {example[-1]}\nSlice: {example[1:3]}")

    # Immutability
    # The following will raise an AttributeError if executed:
    # example.append('hello')
    # This will raise a TypeError:
    # example[2] = "bravo"

    # Tuples are useful because they are smaller and faster than lists. Because
    # lists are mutable, they may become larger after initialisation, thus
    # Python must allocate more memory than is strictly necessary whenever a
    # list is created. If the size of the list exceeds this amount, more memory
    # must be allocated. Allocating memory, copying values, and freeing memory
    # are all slow processes.
    #
    # Tuples, as immutable data types, cannot grow or shrink after creation. As
    # such, Python is able to allocate the necessary memory when the tuple is
    # created, thus less time is spent on the 3 operations mentioned above. The
    # tradeoff is less versitility.
    #
    # Further, unlike lists, tuples can be used as keys in dictionaries, as
    # demonstrated below:
    my_dict = {}

    # A string as key:
    my_dict["Cheese"] = 1

    # An integer:
    my_dict[17] = "hello"

    print(my_dict)

    # A list as key is not, however, permitted:
    # my_dict[["a", "b"]] = "asdf" # TypeError raised.
    # This is due to the mutability of a list; if the values changed then the
    # key would no longer be valid. A tuple can solve this:
    my_dict[("a", "b")] = "Success!"
    print(my_dict)

    # This behaviour is useful when a data structure is desired that maps
    # sequences as keys to corresponding values.
    # NB: Python can also turn a tuple into a list or vice-versa via the
    # tuple() function or list() function.

def ngram_analysis():
    """N-Gram: Sequence of units drawn from a longer sequence. For text, it is
    often a word.

    The unit of the n-gram can also be called its 'level', while the length of
    the n-gram is its 'order'.
    """
    # Example: list of all unique char level order-2 n-grams in the word
    # condescendences:
    # print(set(ngrams('condescendences'))) # NB: not necessarily in order

    # Example on a text:
    # with open(r'.\texts_nlp\austen.txt', 'r', encoding='utf-8') as f:
    #     text = f.read().split()
    #     g = ngrams(text, 5)
    #     # Get unique 'lists' inside the ngram list:
    #     u = [list(x) for x in set(tuple(x) for x in g)][:10]

    #     for i in u:
    #         print(i, end='\n')
    #     # print(g[:10])

    # N-grams are a tool used frequently in NLP and text analysis. This includes
    # spelling correction, visualisation, compression algorithms, stylometrics,
    # and generative text.
    # They can also be used as the basis of a Markov-chain algorithm.
    print('-' * 80)

    # Finding and counting word pairs
    #
    text = ''
    words = ''
    with open(r'.\texts_nlp\genesis.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        words = text.split()
    print(len(words))
    print('-' * 80)
    # The goal of this exercise is to obtain a list of tuples, each having two
    # elements (successive word pairs). There are several ways to do this:

    # Using slicing
    # NB: Must use 'len(words) - 1' because the final element of the list can
    # only be the second element in a pair.
    pairs = [(words[i], words[i+1]) for i in range(len(words) - 1)]
    # print(pairs[:25])

    # THey can be counted using the Counter object from the collections
    # module:
    pair_counts = Counter(pairs)
    # print(pair_counts.most_common(10))
    neat_print(pair_counts.most_common(10))
    # print('-' * 80)

    # From this, it appears that "And God" occurs 21 times in the genesis.txt
    # and comprises 3% of all word pairs found in the text:
    and_god = pair_counts[("And", "God")] / sum(pair_counts.values())
    print(and_god)


    # The same calculation can be made using the chars of the text:
    char_pairs = [(text[i], text[i+1]) for i in range(len(text) - 1)]
    char_pair_counts = Counter(char_pairs)
    # print(char_pair_counts.most_common(10))
    # for i in char_pair_counts.most_common(10):
        # print(i)
    neat_print(char_pair_counts.most_common(10))
    # print('-' * 80)

    # This kind of analysis can be beneficial, especially in determining the
    # similarity between two texts. If the texts have the same n-grams in
    # similar proportions then thos texts are likely to have similar
    # compositions. They can also assist in text searching.

    # N-Grams of Arbitrary Lengths
    seven_grams = [tuple(words[i:i+7]) for i in range(len(words) - 6)]
    neat_print(seven_grams[:10])

    # In the above example, 'tuple' is called on the 'words[i:i+7]' variable to
    # convert the list slice into a tuple. The range(len(words) - 6) is for the
    # same reason as the pairs; to prevent exceeding the length of the list and
    # to ensure a 7 word n-gram is captured.
    # This can be converted to a function as followed:
    # def ngrams_for_seq(n, seq):
    #   return [tuple(seq[i:i+n]) for i in range(len(n) - n + 1)]

    # The 'random' module can be used to get a random char level n-gram of
    # order 9 from genesis.txt:
    genesis_file = r'.\texts_nlp\genesis.txt'
    # frost_file = r'.\texts_nlp\frost.txt'
    # with open(genesis_file, 'r', encoding='utf-8') as f:
    #     genesis_9 = ngrams_for_seq(9, f.read())
    #     neat_print(random.sample(genesis_9, 10))

    # with open(frost_file, 'r', encoding='utf-8') as f:
    #     frost_5gram = ngrams_for_seq(5, f.read().split())
    #     neat_print((frost_5gram))

    neat_print(ngrams_for_seq(2, 'condescendences'))

    # Non-string sequences:
    neat_print(ngrams_for_seq(4, [5, 10, 15, 20, 25, 30]))

    # Used with a Counter object to find the most-common n-grams in a text:
    with open(genesis_file, 'r', encoding='utf-8') as f:
        gentext = f.read()
        neat_print(Counter(ngrams_for_seq(3, gentext)).most_common(10))
        neat_print(Counter(ngrams_for_seq(3, gentext.split())).most_common(10))

def markov_models():
    """Further analysis and working with the n-grams from prior"""
    # Given a particular n-gram in a text, what is most likely to come next?
    # The code should be similar to retrieve the n-grams however, it will
    # need to keep track of both n-grams and all the units (chars, words, etc.)
    # that *follow* those n-grams.

    # Example using 'condescendences'
    # Manuel examination yields the following table:
    #     n-grams 	next?
    #      co 	    n
    #      on 	    d
    #      nd 	    e, e
    #      de 	    s, n
    #      es 	    c, (end of text)
    #      sc 	    e
    #      ce 	    n, s
    #      en 	    d, c
    #      nc 	    e
    #
    # This table indicates that while the n-gram 'co' is followed by 'n' 100%
    # of the time, the ngram 'de' is followed by 's' 50% of the time and 'n'
    # the rest of the time.

    # To represent this model, a dictionary with n-grams as keys and values as
    # possible 'nexts' can be used. The '$' symbol will be used to represent
    # the end of the text:
    src = 'condescendences'
    src += '$'
    model = {}
    length_src = len(src)
    for i in range(length_src - 2):
        # Get slice of length 2 from current position.
        ngram = tuple(src[i:i+2])

        # next item is current index plus 2 (i.e. after the slice)
        next_item = src[i+2]

        # Check if ngram has been seen.
        if ngram not in model:
            model[ngram] = []   # Value for this key is empty list.

        model[ngram].append(next_item)
    # print(model)
    # neat_print(model.items())
    # # print('-' * 80)

    # This can be generalized as a function to produce n-grams of an arbirary
    # length, with the keyword 'None' used to indicate the end of a sequence.
    #
    # The function 'markov_model()' creates an empty dict and takes n-gram
    # length and a sequence (string or list) and calls the 'add_to_model()'
    # function on that sequence. This function does the same thing as the
    # code above: it iterates over every index of the sequence and grabs an
    # n-gram of the desired length, adding keys and values to the dict as
    # necessary:
    # def add_to_model(model, n, seq):
    #     """Iterates over every index in seq, producing n-gram of desired
    #         length before adding the keys and values to the dictionary as
    #         necessary.
    #     """
    #     # Copy seq and append None to the end.
    #     seq = list(seq[:]) + [None]

    #     for i in range(len(seq) - n):
    #         # Tuple because it is the dict's key.
    #         gram = tuple(seq[i:i+n])
    #         next_item = seq[i+n]

    #         if gram not in model:
    #             model[gram] = []
    #         model[gram].append(next_item)

    # def markov_model(n, seq):
    #     model = {}
    #     add_to_model(model, n, seq)
    #     return model

    neat_print(markov_model(2, "condescendences"))
    genesis_file = r'.\texts_nlp\genesis.txt'

    with open(genesis_file, 'r', encoding='utf-8') as f:
        genesis_markov = markov_model(3, f.read().split())
    # neat_print(genesis_markov)

    # The markov model can now be used to make predictions. Given the
    # information in the markov model of 'genesis.txt', what words are likely
    # to follow the sequence of words 'and over the'?
    #
    # This can be found simply by getting the value for the key of that
    # sequence:
    print(genesis_markov[('and', 'over', 'the')])

    # Returns: ['night', 'fowl', 'cattle', 'fowl']
    # This tells us that the sequence is followed by 'fowl' 50% of the time,
    # 'night', 25% of the time, and 'cattle' 25% of the time.

def markov_chains():
    """Generating Text from a Markov Model.
    New text can be generated from the above markov models. This may be
    achieved via 'chaining together predictions'. As an example, starting
    with the order-2 char-level Markov model of 'condescendences':
        1) Start with the initial n-gram (co) representing the first 2
            chars of the output,
        2) Then look at the last 'n' chars of output, where 'n' is the order
            of the n-grams in the table, finding those chars in the 'n-grams'
            column;
        3) Choose randomly among the possibilities in the corresponding 'next'
            column and append that letter to the output (sometimes, as with
            'co', there is only one option);
        4) If 'end of text' is chosen, the algorithm completes. Otherwise,
            repeat the process starting with 2).
    """
    # Example output from Parrish:
    # co
    # con
    # cond
    # conde
    # conden
    # condend
    # condendes
    # condendesc
    # condendesce
    # condendesces

    # As can be seen, the algorithm returns a word that looks like the original,
    # and could be passed of as a genuine English word. Statistically, the outpu
    # of the algorithm is nearly indistinguishable from the input. This kind of
    # algorithm - moving from one state to the next, according to a list of
    # probabilities - is known as a markov chain.

    # Example: "condescendences"
    cmodel = markov_model(2, "condescendences")
    neat_print(cmodel)

    # Generate some output. Initialize with desired starting chars e.g. 'co':
    # output = "co"

    # Now, get the last two chars of the output, look them up in the model, and
    # select randomly among the chars in the value for that key (should be a
    # list). Finally, append the randomly selected value to the end of the
    # # string.
    # ngram = tuple(output[-2:])
    # next_item = random.choice(cmodel[ngram])
    # output += next_item
    # print(output)

    # Trying the above multiple times. Output gets longer until an error occurs.
    # output = "co"
    # for _ in range(100):
    #     ngram = tuple(output[-2:])
    #     next_item = random.choice(cmodel[ngram])
    #     output += next_item
    #     print(output)
    # Eventually raises a 'TypeError' when the end of text condition is reached.
    # This is because 'None' was chosen to represent the end, and it cannot be
    # concatenated with the 'str' value.
    # Statistically, it also indicates that the end of the text has been
    # reached, and so generation can halt. This directive can be handled by
    # using the 'break' keyword  to exit the loop early:
    # print('-' * 80)

    # output = "co"
    # for _ in range(100):
    #     ngram = tuple(output[-2:])
    #     next_item = random.choice(cmodel[ngram])
    #     if next_item is None:
    #         break
    #     output += next_item
    #     print(output)

    # print('-' * 80)
    # NB: The range of 100 is simply used as a reasonable number of times the
    # Markov chain should produce an attempt to append to the output. As there
    # is a loop in this particular model (nd -> e, de -> n, en -> d), any time
    # text is generated from this chain, it could go on indefinitely. Limiting
    # the number to 100 avoids this problem. The number can be adjusted,
    # depending on the desired goal of the chain.

    # Functions to generate from a Markov Model
    # def gen_from_model(n, model, start=None, max_gen=100):
    # if start is None:
    #     start = random.choice(list(model.keys()))
    # output = list(start)
    # for _ in range(max_gen):
    #     start = tuple(output[-n:])
    #     next_item = random.choice(model[start])
    #     if next_item is None:
    #         break
    #     output.append(next_item)
    # return output

    # The first parameter is the length of n-gram, the second the Markov model
    # as returned from 'markov_model()', the third parameter is the 'seed'
    # n-gram from which to start generating.
    # The function always returns a list. If using char level n-grams, the
    # 'join' function can be used to concatenate the list values.
    print('-' * 80)
    print(''.join(gen_from_model(2, cmodel, ('c', 'o'))))

    # If the "seed" is omitted, the function will choose a random n-gram
    # to start:
    sea_model = markov_model(3, "she sells sea shells by the seashore")
    for _ in range(12):
        print(''.join(gen_from_model(3, sea_model, )))

def advanced_markov_style():
    """Generating Lines.
    The gen_from_model() function can also be used to generate word-level
    Markov chains.
    """
    # genesis_file = r'.\texts_nlp\genesis.txt'

    # with open(genesis_file, 'r', encoding='utf-8') as f:
    #     genesis_word_model = markov_model(2, f.read().split())

    # generated_words = gen_from_model(2, genesis_word_model, ('In', 'the'))
    # print(' '.join(generated_words))
    # print('-' * 80)
    # While it may appear to work well, there is an issue with this approach.
    # As noted, generation continues until either the 'end of text' marker is
    # selected or the maximum number of iterations has been reached. For
    # example, supplying a larger number for 'max_gen' parameter leads to
    # (generally) a longer output:
    # generated_words = gen_from_model(2, genesis_word_model, ('In', 'the'), 500)
    # print(' '.join(generated_words))
    print('-' * 80)

    # Generally, the longer the text, the less likely that the 'end of text'
    # token will be reached.

    # In some circumstances this could be desirable, however, the underlying
    # text has some structure because each line is actually a verse. As such,
    # it may be possible to generate actual verses by treating each line
    # separately, producing an end of text token for each line.

    # To avoid this, modifications can be made.
    # def markov_model_from_sequences(n, sequences):
    #     """Creates a model, adding each iterm from a list to the model as a
    #     separate item. Returns the combined model.
    #     """
    #     model = {}
    #     for item in sequences:
    #         add_to_model(model, n, item)
    #     return model
    # The function expects a list of sequences, such as lists or strings,
    # depending on whether a word level or char level model is desired.
    genesis_file = r'.\texts_nlp\genesis.txt'

    with open(genesis_file, 'r', encoding='utf-8') as f:
        genesis_lines = f.readlines()

    # list of lists of words (stripped) in each line
    # genesis_lines_words = [line.strip().split() for line in genesis_lines]
    # genesis_lines_model = markov_model_from_sequences(2, genesis_lines_words)

    # The 'genesis_lines_model' variable now contains a Markov model with end
    # of text tokens where they should be: at the end of each line.
    # for i in range(10):
    #     gen_line = ' '.join(gen_from_model(2, genesis_lines_model))
    #     # print("verse:", i, "-", gen_line)
    # print('-' * 80)
    # This is better output with the lines ending at appropriate places. It is,
    # however, not quite right as generation is from random keys in the
    # Markov model.
    # To make this absolutely correct, it needs to *start* each line with an
    # n-gram that also occurred at the start of each line in the original file.

    # Get the list of lists of words:
    # with open(genesis_file, 'r', encoding='utf-8') as f:
    #     genesis_lines = f.readlines()
    # genesis_lines_words = [line.strip().split() for line in genesis_lines]

    # Get the N-grams at the start of each line:
    # genesis_starts = [item[:2] for item in genesis_lines_words
                    #   if len(item) >= 2]
    # Create the Markov model:
    # genesis_lines_model = markov_model_from_sequences(2, genesis_lines_words)

    # Generate from it picking a 'start' at random:
    # for i in range(10):
    #     start = random.choice(genesis_starts)
    #     generated = gen_from_model(2, genesis_lines_model, start)
        # print(f"verse: {i} - {' '.join(generated)}")

    # print('-' * 80)

    # Putting it together - Wrapping things up neatly
    #
    # The following function takes an n-gram length, a list of sequences, and
    # a number of lines to generate, and that many generated lines. It starts
    # the generation only with n-grams that begin lines in the source file:
    # def markov_generate_from_seqs(n, seqs, count, max_gen=100):
    #     starts = [item[:n] for item in seqs if len(item) >= n]
    #     model = markov_model_from_sequences(n, seqs)
    #     return [gen_from_model(n, model, random.choice(starts), max_gen)
    #             for i in range(count)]

    # An example:
    # frost_file = r'.\texts_nlp\frost.txt'
    # with open(frost_file, 'r', encoding='utf-8') as f:
    #     frost_lines = [line.strip() for line in f.readlines()]

    # for item in markov_generate_from_seqs(5, frost_lines, 20):
    #     print(''.join(item))

    # print('-' * 80)

    # Word level Markov model of Shakepeare's Sonnets:
    sonnets = r'.\texts_nlp\sonnets.txt'
    with open(sonnets, 'r', encoding='utf-8') as f:
        sonnets_words = [line.strip().split() for line in f.readlines()]
    for item in markov_generate_from_seqs(5, sonnets_words, 20):
        print(' '.join(item))

    print('-' * 80)

    # Combination of sources:
    # E.g. frost and genesis

    frost_file = r'.\texts_nlp\frost.txt'
    genesis_file = r'.\texts_nlp\genesis.txt'

    with open(genesis_file, 'r', encoding='utf-8') as g, \
        open(frost_file, 'r', encoding='utf-8') as f:

        genesis_lines = [line.strip() for line in g.readlines()]
        frost_lines = [line.strip() for line in f.readlines()]

    frosty_genesis = frost_lines + genesis_lines

    print('\n', '-' * 80)
    for item in markov_generate_from_seqs(5, frosty_genesis, 14, max_gen=150):
        print(''.join(item))

    print('-' * 80)
    # with open(frost_file, 'r', encoding='utf-8') as f:
    #     frost_lines = [line.strip() for line in f.readlines()]

def final_experiments():
    """Following function does all the work.

    takes an n-gram length, an open filehandle to read from, the number of
    lines to generate, and the string char for a character-level Markov model
    and word for a word-level model. It returns the requested number of lines
    generated from a Markov model of the desired order and level.

    """
    # def markov_generate_from_lines_in_file(ngram_len,
    #                                        filehandle,
    #                                        count,
    #                                        level='char',
    #                                        max_gen=100):
    #     if level == 'char':
    #         glue = ''
    #         sequences = [item.strip()
    #                      for item in filehandle.readlines()]
    #     elif level == 'word':
    #         glue == ' '
    #         sequences = [item.strip().split()
    #                      for item in filehandle.readlines()]

    #     generated = markov_generate_from_seqs(ngram_len,
    #                                           sequences,
    #                                           count,
    #                                           max_gen)
    #     return [glue.join(item) for item in generated]
    print('-' * 80)
    searose = r'.\texts_nlp\sea_rose.txt'
    with open(searose, 'r', encoding='utf-8') as sea:
        for item in markov_generate_from_lines_in_file(3, sea, 20, 'char'):
            print(item)

    print('-' * 80)
    # Or word level genesis:
    genesis_txt = r'.\texts_nlp\genesis.txt'
    with open(genesis_txt, 'r', encoding='utf-8') as g:
        for item in markov_generate_from_lines_in_file(3, g, 5, 'word'):
            print(item)
            print("")

    print('-' * 80)

def main():
    "A controller function for calling other functions, etc."
    # about_tuples()
    # ngram_analysis()
    # markov_models()
    # markov_chains()
    # advanced_markov_style()
    # final_experiments()
    print("Undo commented out sections to run.")

if __name__ == "__main__":
    # pass
    main()
