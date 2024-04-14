import re
import argparse

class SentenceChunkReader:
    def __init__(self, filename, chunk_size=4096):
        self.filename = filename
        self.chunk_size = chunk_size
        self.file = open(filename, 'r', encoding="utf")
    
    def __iter__(self):
        return self
    
    def __next__(self):
        chunk = self.file.read(self.chunk_size)
        if not chunk:
            self.file.close()
            raise StopIteration
        
        if chunk[-1] != '.':
            last_period_index = chunk.rfind('.')
            while last_period_index != len(chunk) - 1:
                next_char = self.file.read(1)
                if not next_char:
                    return chunk
                chunk += next_char
                last_period_index = chunk.rfind('.')
        return chunk

class CorpusCleaner:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.input_filename = self.extract_filename_from_path()
        self.cleaned_output_file_path = f"{self.input_filename}_cleaned.txt"

    def extract_filename_from_path(self):
        if '/' in self.input_file_path:
            filename_ext = self.input_file_path.split('/')[-1]
        elif '\\' in self.input_file_path:
            filename_ext = self.input_file_path.split('\\')[-1]
        else:
            filename_ext = self.input_file_path
        if '.' in filename_ext:
            input_filename = filename_ext.split('.')[0]
        else:
            input_filename = filename_ext
        return input_filename

    def append_to_file(self, file_path, string):
        with open(file_path, 'a', encoding="utf") as f:
            f.write(string)

    def clean(self, string):
        pattern = r"[^ஂ-௺.]"
        string = re.sub(pattern, " ", string)
        pattern = r" {1,}"
        string = re.sub(pattern, " ", string)
        self.append_to_file(self.cleaned_output_file_path, string)
        return string
    
class SentenceTokenizer(CorpusCleaner):
    def __init__(self, input_file_path):
        super().__init__(input_file_path)
        self.tokenized_output_file_path = f"{self.input_filename}_tokenized.txt"

    def append_to_file_by_line(self, file_path, list):
        with open(file_path, 'a', encoding="utf") as f:
            for each in list:
                f.write(each + '\n')

    def strip(self, list):
        stripped_list = []
        for each in list:
            stripped = each.strip()
            if stripped:
                stripped_list.append(stripped)
        return stripped_list

    def tokenize(self, string):
        tokens = string.split('.')
        tokens = self.strip(tokens)
        self.append_to_file_by_line(self.tokenized_output_file_path, tokens)
        return tokens

    def clear_output_files(self):
        with open(self.cleaned_output_file_path, 'w') as f:
            pass
        with open(self.tokenized_output_file_path, 'w') as f:
            pass

    def run(self):
        self.clear_output_files()
        sentence_chunk_reader = SentenceChunkReader(self.input_file_path)
        for sentence_chunk in sentence_chunk_reader:
            cleaned_chunk = self.clean(sentence_chunk)
            tokens = self.tokenize(cleaned_chunk)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Sentence tokenizer for the Tamil language.")
    arg_parser.add_argument("input_file", type=str, help="Name of the file on which to perform sentence tokenization")
    args = arg_parser.parse_args()
    sentence_tokenizer = SentenceTokenizer(args.input_file)
    sentence_tokenizer.run()