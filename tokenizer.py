import string

class StringTokenizer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self._tokenize()

    def _tokenize(self):
        word = ""
        for char in self.text:
            # If character is letter or digit, add to word
            if char.isalnum():
                word += char
            else:
                # If we hit punctuation/space, store the word
                if word != "":
                    self.tokens.append(word)
                    word = ""
        
        # Add last word if exists
        if word != "":
            self.tokens.append(word)

    def get_tokens(self):
        return self.tokens

    def count_tokens(self):
        return len(self.tokens)


# Example usage
text = "Hello! Python is great, and ML is powerful."
tokenizer = StringTokenizer(text)

print("Tokens:", tokenizer.get_tokens())
print("Total Tokens:", tokenizer.count_tokens())
