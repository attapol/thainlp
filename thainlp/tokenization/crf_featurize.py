import codecs
import sys

def featurize(pattern_list, seq):
    label_feature_seq = []
    for i in range(len(seq)):
        features = []
        _, _, label = seq[i] 
        for pattern in pattern_list:
            conjoined_features = []
            feature_name = u't{}'.format('t'.join([str(x) for x in pattern]))
            for position in pattern:
                if (i + position) >= 0 and (i + position) < len(seq):
                    character, _, _ = seq[i+position]
                    conjoined_features.append(character)
                else:
                    conjoined_features.append(u'N')
            features.append(
                u'{}_{}'.format(feature_name, u''.join(conjoined_features)))
        label_feature_seq.append( (label, features) )
    return label_feature_seq

def read_template(template):
    patterns = []
    with open(template) as f:
        for line in f:
            if ',' in line: #conjoined feature
                pattern = [int(x) for x in line.strip().split(',')]
            else:
                pattern = [int(line.strip())]
            patterns.append(pattern)
    return patterns

def iterate_seq(f):
    seq = []
    for line in f:
        line = line.strip()
        if line == '' and len(seq) > 0:
            yield seq
            seq = []
        else:
            character, char_type, label = line.split(' ')
            seq.append((character, char_type, label))
