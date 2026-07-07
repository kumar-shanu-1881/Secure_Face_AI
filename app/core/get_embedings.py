from insightface.app import FaceAnalysis


class FaceEmbedding:

    def __init__(self):

        self.model = FaceAnalysis(
            name="buffalo_sc",  # Use the "buffalo_scale" model for face embeddings
            providers=["CPUExecutionProvider"]
        )

        '''buffalo_scale model is a pre-trained face recognition model that provides high-quality embeddings for face recognition tasks.
            │
            ├── Face Detector (SCRFD)
            ├── Face Landmark Model
            ├── ArcFace Recognition Model
            └── Gender/Age Model (optional)
'''
        self.model.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def get_embedding(self, image):

        faces = self.model.get(image)

        if len(faces) == 0:
            return None

        return faces[0].embedding
    

get_embedder = FaceEmbedding()
    
    
    # result = detector.detect(frame)

    # if result["success"]:

    # embedding = embedder.get_embedding(frame)