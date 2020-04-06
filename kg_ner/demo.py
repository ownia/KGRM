# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller
import os

if __name__ == '__main__':
    LTP_DATA_DIR = 'ltp_data_v3.4.0/'
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
    srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')

    segmentor = Segmentor()
    postagger = Postagger()
    recognizer = NamedEntityRecognizer()
    parser = Parser()
    # labeller = SementicRoleLabeller()

    segmentor.load(cws_model_path)
    postagger.load(pos_model_path)
    recognizer.load(ner_model_path)
    parser.load(par_model_path)
    # labeller.load(srl_model_path)

    words = segmentor.segment('元芳你怎么看')
    postags = postagger.postag(words)
    netags = recognizer.recognize(words, postags)
    arcs = parser.parse(words, postags)
    # roles = labeller.label(words, postags, arcs)
    words_list = list(words)
    postags_list = list(postags)
    segmentor.release()
    postagger.release()
    recognizer.release()
    parser.release()
    # labeller.release()

    for w in words_list:
        print(w)
    for p in postags_list:
        print(p)
    print('\t'.join(netags))
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    # for role in roles:
    #   print(role.index, "".join(
    #        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
