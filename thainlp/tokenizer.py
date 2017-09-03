import cPickle
import pkg_resources

from thainlp.tokenization.crf_featurize import featurize, read_template

class Tokenizer(object):

    MODEL_CACHE = {}
    METHODS = ['crf']

    def __init__(self, method='crf'):
        assert (method in Tokenizer.METHODS)
        if method in Tokenizer.MODEL_CACHE:
            self.model = Tokenizer.MODEL_CACHE[method]

        if method == 'crf':
            self.model = CRFTokenizer()
        else:
            return None #TODO: error message ValueError of sort
        Tokenizer.MODEL_CACHE[method] = self.model

    def tokenize(self, text):
        return self.model.tokenize(text)


class CRFTokenizer(object):

    def __init__(self):
        #TODO: use tar file instead to reduce the package size
        data_path = pkg_resources.resource_filename('thainlp', 'tokenization') 
        self.model = cPickle.load(open(data_path + '/crf.model'))
        self.patterns = read_template(data_path + '/crf_template.txt')

    def __str__(self):
        return 'CRF Tokenizer'

    def tokenize(self, text):
        seq = [(x, 'dummy', 'dummy') for x in text]
        label_feature_seq = featurize(self.patterns, seq)
        feature_seq = []
        for _, feature in label_feature_seq:
            feature_seq.append({k:True for k in feature})
        predicted = self.model.predict([feature_seq])[0]
        to_print = u''
        for pred, character in zip(predicted, text):
            if pred == 'B':
                to_print += u' '
            to_print += character
        return to_print.strip().split(' ')
