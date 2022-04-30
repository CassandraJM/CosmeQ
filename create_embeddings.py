import numpy as np
import csv
from sentence_transformers import SentenceTransformer


def load_transformer():
    path="all-mpnet-base-v2/"
    model = SentenceTransformer(path)
    return(model)

def get_embeddings1(model):
    
    #Read harmful chemicals dataset as a list
    print ('reading dataset..')
    with open("dataset/harmful_chemicals_cosmetics.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
    
    #improve the list format (avoid nested lists)
    sentences1=[]
    for i in range(len(data)):
        sentences1.append(data[i][0])

    #Compute embeddings for harmful chemicals dataset
    print ('creating embeddings..')
    emb1 = model.encode(sentences1, convert_to_tensor=True)
    
    print('embeddings created..')

    return(emb1, sentences1)

model = load_transformer()
embeddings1, sentences1 = get_embeddings1(model)
embeddings1 = np.array(embeddings1)
np.save('npy/embeddings.npy', embeddings1)
sentences1 = np.array(sentences1)
np.save('npy/sentences.npy', sentences1)