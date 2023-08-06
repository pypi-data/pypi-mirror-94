from sentence_transformers import SentenceTransformer

from wmd import WMD
import numpy as np

import nltk
nltk.download('punkt')


class SMD(object):

	"""
	The main class to work with Sentence Mover's Distance with Sentence Transformers.
	.. automethod:: __init__
	""" 

	def __init__(self, document, documents_list):

		"""
		Initializes a new instance of SMD with Sentence Transformers.

		:param document: 
		:param documents_list:
		:type document: string
		:type documents_list: list of string
		:raises TypeError: if some of the arguments are invalid.
		:raises ValueError: if some of the arguments are invalid.
		"""

		self.document = document
		self.documents_list = documents_list
		self.model = SentenceTransformer('paraphrase-distilroberta-base-v1')

	def tokenize_documents(self):

		token_vecs_sum = []
			
		for doc in self.documents_list:
			
			doc_token_vecs_sum = []

			for sentence in nltk.sent_tokenize(doc):
				doc_token_vecs_sum.append(self.model.encode(sentence))
			
			token_vecs_sum.append(doc_token_vecs_sum)
	
		return token_vecs_sum

	def tokenize_text(self):

		doc_token_vecs_sum = []

		for sentence in nltk.sent_tokenize(self.document):
			doc_token_vecs_sum.append(self.model.encode(sentence))

		return doc_token_vecs_sum


	def get_sent_embeddings(self, tokens, new_id):

		id_list = []
		rep_map = {}
		sents_ids = []
		
		
		for sent in range(len(tokens)):

			new_id +=1

			#add sentence embedding to the embedding dict
			rep_map[new_id] = np.array(tokens[sent])
			sents_ids.append(new_id)

		id_list += sents_ids

		return id_list, rep_map, new_id

	def get_weights(self, token):

		#2 arrays where an embedding's weight is at the same index as its ID in id_lists
		d_weight = np.array([], dtype=np.float32)

		#make sure to check no empty ids
		d_weight = np.append(d_weight, np.array([float(1) for tensor in token], dtype=np.float32))

		return d_weight


	def get_closest_doc(self):

		doc_set_list = []
		doc_rep_map = {}
		new_id = 0

		documents_vec_list = self.tokenize_documents()
		document_vec = self.tokenize_text()

		id_list, rep_map, new_id = self.get_sent_embeddings(document_vec, new_id)
		d_weights = self.get_weights(document_vec)

		doc_set = ("0", id_list, d_weights)
				
		doc_set_list.append(doc_set)
		doc_rep_map.update(rep_map)

		for doc_id in range(len(documents_vec_list)):

			id_list, rep_map, new_id = self.get_sent_embeddings(documents_vec_list[doc_id], new_id)
			d_weights = self.get_weights(documents_vec_list[doc_id])

			doc_set = (str(doc_id), id_list, d_weights)
				
			doc_set_list.append(doc_set)
			doc_rep_map.update(rep_map)


		doc_dict = {"doc0": doc_set_list[0]} 
		sum_dict = {str(j-1): doc_set_list[j] for j in range(1, len(documents_vec_list))}
		doc_dict.update(sum_dict)
		
		calc = WMD(doc_rep_map, doc_dict, vocabulary_min=1)
		result = calc.nearest_neighbors("doc0", k=1, early_stop=1)[0]
		
		return result