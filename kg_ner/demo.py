# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller
import os
import hanlp
from hanlp.common.trie import Trie
import json
import re


class HitLtp:
    @staticmethod
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


def hanlp_module():
    tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
    fp = open('test.txt', 'r', encoding='utf-8')
    data = fp.read()
    fp.close()
    print(tokenizer(data))


def split_sents(text: str, trie: Trie):
    words = trie.parse_longest(text)
    sents = []
    pre_start = 0
    offsets = []
    for word, value, start, end in words:
        if pre_start != start:
            sents.append(text[pre_start: start])
            offsets.append(pre_start)
        pre_start = end
    if pre_start != len(text):
        sents.append(text[pre_start:])
        offsets.append(pre_start)
    return sents, offsets, words


def merge_parts(parts, offsets, words):
    items = [(i, p) for (i, p) in zip(offsets, parts)]
    items += [(start, [word]) for (word, value, start, end) in words]
    # items += [(start, [(word, value)]) for (word, value, start, end) in words]
    return [each for x in sorted(items) for each in x[1]]


def dict2json():
    fp = open('dict.json', 'w', encoding='utf-8')
    j = json.dumps({'自定义': 'custom', '词典': 'dict', '聪明人': 'smart'}, ensure_ascii=False)
    fp.write(j)
    fp.close()


def tokenizer_pku():
    f = open('dict.json', 'r', encoding='utf-8')
    dict = json.load(f)
    f.close()
    trie = Trie()
    trie.update(dict)
    print(type(trie))
    text = 'NLP统计模型没有加规则，聪明人知道自己加。英文、数字、自定义词典统统都是规则。'
    print(split_sents(text, trie))
    tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
    tokenizer = hanlp.pipeline() \
        .append(split_sents, output_key=('parts', 'offsets', 'words'), trie=trie) \
        .append(tokenizer, input_key='parts', output_key='tokens') \
        .append(merge_parts, input_key=('tokens', 'offsets', 'words'), output_key='merged')
    print(tokenizer(text))


def bert_ner():
    recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
    fp = open('test2.txt', 'r', encoding='utf-8')
    data1 = fp.read()
    fp.close()
    # list_data = data.split("，")
    list_data = re.split(r'[，。；\s]\s*', data1)
    data2 = []
    for li in list_data:
        data2.append(list(li))
    rec = recognizer(data2)
    print(rec)
    with open('bert_ner.txt', 'w', encoding='utf-8') as f:
        for r in rec:
            for i in r:
                if len(i[0]) > 1:
                    f.writelines(i[0] + '\n')


if __name__ == '__main__':
    # ltp()
    # hanlp_module()
    # dict2json()
    # tokenizer_pku()
    # print(hanlp.pretrained.ALL)
    # tokenizer_pku()
    bert_ner()
