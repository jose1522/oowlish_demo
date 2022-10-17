OUTPUT_FOLDER=worker/nlp/assets/long-text-summarizer/
FILE_NAME=pytorch_model.bin
OUTPUT_PATH=$OUTPUT_FOLDER$FILE_NAME
SOURCE=https://huggingface.co/pszemraj/long-t5-tglobal-base-16384-book-summary/resolve/main/pytorch_model.bin

echo "Checking for model weights..."
if ! [[ -f "$OUTPUT_PATH" ]]; then
  echo "Model weights $FILE_NAME not found at $OUTPUT_FOLDER"
  echo "Downloading model weights..."
  wget -O $OUTPUT_PATH -N $SOURCE
else
  echo "Model weights found"
fi