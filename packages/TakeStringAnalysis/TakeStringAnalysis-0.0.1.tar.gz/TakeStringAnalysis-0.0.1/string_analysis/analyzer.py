import io
from pyjarowinkler import distance
class StringAnalysis():
    def __init__(self, string_streaming):
        self.__string_streaming = string_streaming

    def get_most_similar_word(self, word):
        '''This method calculates the similarity between a word and all the other 
        words in a data stream. The similarity used to define how similar two words 
        are in this method is the Jaro-winkler distance that measures an edit distance 
        between two sequences '''
        
        similar_lst = [(current_word, distance.get_jaro_distance(word, current_word)) 
                                            for sentence in self.__iterate_on_streaming() 
                                            for current_word in sentence]
        return list(self.__sorting_dict(dict(similar_lst)).items())[0][0] if similar_lst else []
    
    def __sorting_dict(self, dictionary):
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}

    def __iterate_on_streaming(self):
        for sentence in self.__string_streaming:
            yield sentence.split()
