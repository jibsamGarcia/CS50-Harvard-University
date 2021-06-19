import nltk
import sys
import os
import string
import math

nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = {}

    for file in os.listdir(directory):
        with open(os.path.join(directory, file), encoding="utf-8") as ofi:
            dictionary[file] = ofi.read()

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tokenized = nltk.tokenize.word_tokenize(document.lower())

    fn_list = [x for x in tokenized if x not in string.punctuation and x not in nltk.corpus.stopwords.words("english")]

    return fn_list

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    # Get unique vocabulary
    unique = []
    for vocab in documents.values():
        unique.extend(set(vocab))
    unique = set(unique)

    # calculate idf's
    num_docs = len(documents)
    for word in unique:
        doc_count = 0
        for vocab in documents.values():
            if word in vocab:
                doc_count += 1
        idfs[word] = math.log(num_docs / doc_count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    for filename, filecontent in files.items():
        file_score = 0
        for word in query:
            if word in filecontent:
                file_score += filecontent.count(word) * idfs[word]
        if file_score != 0:
            scores[filename] = file_score

    sorted_by_score = [k for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
    return sorted_by_score[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Calculate matching word measures and query term densities
    scores = {}
    for sentence, sent_words in sentences.items():
        score = 0
        for word in query:
            if word in sent_words:
                score += idfs[word]

        if score != 0:
            density = sum([sent_words.count(x) for x in query]) / len(sent_words)
            scores[sentence] = (score, density)

    sorted_by_score = [k for k, v in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]

    return sorted_by_score[:n] # Only return first n values


if __name__ == "__main__":
    main()