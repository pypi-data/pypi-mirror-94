import numpy as np
from collections import Counter
from wmd import WMD
import nltk
import spacy
import en_core_web_lg

class docWMD(object):

    def __init__(self, doc, list_doc):
        
        self.embedding = en_core_web_lg.load()
        self.stopwords = self.embedding.Defaults.stop_words
        self.doc = doc
        self.list_doc = list_doc


    def get_tokenize_documents(self):
        
        #input: raw input text

        id_docs = []
        

        for doc in self.list_doc:

            text = doc.split('\t')[0].strip()
            sent_list = [sent for sent in nltk.sent_tokenize(text)]
            IDs = [[self.embedding.vocab.strings[t.text.lower()] for t in self.embedding(sent) if t.text.isalpha() and t.text.lower() not in self.stopwords] for sent in sent_list]

            id_list = [x for x in IDs if x != []]  # get rid of empty sents

            id_docs.append(id_list)

        return id_docs


    def get_tokenize_text(self):

        #input: raw input text

        text = self.doc.split('\t')[0].strip()
        sent_list = [sent for sent in nltk.sent_tokenize(text)]
        IDs = [[self.embedding.vocab.strings[t.text.lower()] for t in self.embedding(sent) if t.text.isalpha() and t.text.lower() not in self.stopwords] for sent in sent_list]

        id_list = [x for x in IDs if x != []]  # get rid of empty sents

        return id_list


    def wmd_get_embeddings(self, id_doc):
        
        rep_map = {}

        for sent in range(len(id_doc)):
            
            word_emb_list = []  #list of a sentence's word embeddings
            
            #get word embeddings
            for wordID in id_doc[sent]:
                word_emb = self.embedding.vocab.get_vector(wordID)
                word_emb_list.append(word_emb)

            for w_ind in range(len(word_emb_list)):
                # if the word is not already in the embedding dict, add it
                w_id = id_doc[sent][w_ind]
                if w_id not in rep_map:
                    rep_map[w_id] = word_emb_list[w_ind]
        
        return id_doc, rep_map

    def wmd_get_weights(self, id_doc):
        
        #Note that we only need to output counts; these will be normalized by the sum of counts in the WMD code.

        #1-d lists of all relevant embedding IDs
        id_list = []
        
        #2 arrays where an embedding's weight is at the same index as its ID in id_lists
        d_weight = np.array([], dtype=np.float32)

        # collapse to 1-d
        wordIDs = sum(id_doc, [])

        #get dict that maps from ID to count
        counts = Counter(wordIDs)

        for k in counts.keys():
            id_list.append(k)
            d_weight = np.append(d_weight, counts[k])

        return id_list, d_weight


    def get_closest(self):
        
        texts_rep_map = []
        texts_doc_set_list = []
        texts_rep_map = {}

        token_list_tgt = self.get_tokenize_documents()
        token_list_src = self.get_tokenize_text()

        #transform doc to ID list, both words and/or sentences. get ID dict that maps to emb
        ids, rep_map = self.wmd_get_embeddings(token_list_src)

        # get D values
        id_list, d = self.wmd_get_weights(ids)

        doc_set = ("doc0", id_list, d)

        texts_doc_set_list.append(doc_set)
        texts_rep_map.update(rep_map)  


        for doc_id in range(len(token_list_tgt)):

            doc = token_list_tgt[doc_id]

            #transform doc to ID list, both words and/or sentences. get ID dict that maps to emb
            ids, rep_map = self.wmd_get_embeddings(doc)

            # get D values
            id_list, d = self.wmd_get_weights(ids)

            doc_set = (str(doc_id), id_list, d)

            texts_doc_set_list.append(doc_set)
            texts_rep_map.update(rep_map) 

            

        #on créée un dictionnaire contenant les informations sur le document i et sur les 1000 résumés
        doc_dict = {"doc0": texts_doc_set_list[0]} 
        sum_dict = {str(j-1): texts_doc_set_list[j] for j in range(1, len(texts_doc_set_list))}
        doc_dict.update(sum_dict)
        
        #on créée un objet calc avec ce dictionnaire
        calc = WMD(texts_rep_map, doc_dict, vocabulary_min=1)
        results = calc.nearest_neighbors("doc0", k=1, early_stop=1)[0]

        return results