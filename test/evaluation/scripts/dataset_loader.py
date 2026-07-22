from pathlib import Path


class DatasetLoader:

    def __init__(self):

        BASE = Path(__file__).resolve().parent.parent

        self.lfw_path = (
            BASE /
            "dataset" /
            "lfw" /
            "lfw_funneled"
        )

        self.wider_path = (
            BASE /
            "dataset" /
            "widerface"
        )

    # LFW

    def load_lfw(self):

        data = []

        for person in self.lfw_path.iterdir():

            if not person.is_dir():
                continue

            for image in person.glob("*.jpg"):

                data.append(
                    {
                        "person": person.name,
                        "image_path": image
                    }
                )

        return data

    # WIDER FACE
    
    def load_wider(self):

        data = []

        for image in self.wider_path.rglob("*.jpg"):

            data.append(image)

        return data


loader = DatasetLoader()