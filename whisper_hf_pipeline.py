import torch
from transformers import pipeline
import os
import json

model = ""

pipe = pipeline(
    "automatic-speech-recognition", model=model, chunk_length_s=20, device="cpu"
)

audio = ""

prediction = pipe(audio, batch_size=8, return_timestamps=True)["chunks"]

filename = os.path.basename(audio)

output = json.dumps(prediction, indent=2)

with open(filename, "w") as f:
    f.write(output)
