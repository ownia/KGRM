# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller
import os
import hanlp


def ltp_module():
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


def hanlp_module(data):
    tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
    print(tokenizer(data))


if __name__ == '__main__':
    # ltp()
    data = '受旺季高温天气刺激和电商618大促双重影响，本月空调市场规模再攀新高，根据奥维云网（AVC）推总数据显示，2018年6月空调零售额规模为331.5亿元，同比增长19.5%，零售量规模为1004.4万套，同比增长13.7%。其中线上市场top品牌格局出现分化，奥克斯占比大幅度提升，零售额占比达到28.9%，领先第二名品牌7.1%；而线下市场品牌格局依然稳定，格力、美的的份额继续提升，挤压二线品牌的生存空间。'
    hanlp_module(data)
