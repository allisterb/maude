import abc

class SentenceEmbedding(abc.ABC):
    """Represent sentences as vectors"""

    def __init__(self, name, args=[]):
        self.name = name
        self.args = args

    @abc.abstractmethod
    def get_model_info(self)->str:
        """Get information on the model"""

    @abc.abstractmethod
    def get_vector(s1:str): 
        """Get sentence vector"""

    @abc.abstractmethod
    def similarity(s1:str, s2:str)->float: 
        """Compute similarity of 2 sentences"""
