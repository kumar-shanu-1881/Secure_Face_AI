import numpy as np
from numpy.linalg import norm


def compare_faces(embedding1, embedding2):

    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    # Cosine Similarity
    cosine_similarity = np.dot(embedding1, embedding2) / (
        norm(embedding1) * norm(embedding2)
    )

    # Euclidean Distance
    euclidean_distance = np.linalg.norm(embedding1 - embedding2)

    #Decision logic 
    if cosine_similarity >= 0.70 and euclidean_distance <= 1.10 :
        return True,cosine_similarity,euclidean_distance
        
    return False ,cosine_similarity,euclidean_distance

if __name__=='__main__':
    compare_faces