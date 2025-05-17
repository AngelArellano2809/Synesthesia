import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class ColorExtractor:
    def __init__(self, n_colors=3, resize_to=(100, 100)):
        self.n_colors = n_colors
        self.resize_to = resize_to
    
    def extract_colors(self, image_path):
        """Adaptación directa de tu Colab"""
        img = Image.open(image_path).resize(self.resize_to)
        img_array = np.array(img)
        pixels = img_array.reshape(-1, 3)
        
        kmeans = KMeans(n_clusters=self.n_colors)
        kmeans.fit(pixels)
        
        return kmeans.cluster_centers_.astype(int)