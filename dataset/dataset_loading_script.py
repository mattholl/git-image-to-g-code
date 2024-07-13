import json
import datasets
from PIL import Image
import os


class ImageTextDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "file_name": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "image": datasets.Image(),
                }
            )
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"split": "validation"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"split": "test"}
            ),
        ]

    def _generate_examples(self, split):
        split_dir = os.path.join(os.path.abspath(self.config.data_dir), split)
        metadata_path = os.path.join(split_dir, "metadata.jsonl")

        with open(metadata_path, "r") as f:
            for id_, line in enumerate(f):
                data = json.loads(line)
                image_path = os.path.join(split_dir, data["file_name"])
                text_path = os.path.join(split_dir, data["text"])

                with open(text_path, "r") as text_file:
                    text_content = text_file.read()

                yield id_, {
                    "file_name": data["file_name"],
                    "text": text_content,
                    "image": Image.open(image_path),
                }
