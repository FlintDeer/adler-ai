# debug_tokenizer.py
from transformers import AutoTokenizer

def inspect_tokens(tokenizer_name="distilbert-base-uncased", special_tokens=None, test_inputs=None):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    if special_tokens:
        tokenizer.add_tokens(special_tokens)

    print("\n=== Special Tokens ===")
    for tok in special_tokens or []:
        tok_id = tokenizer.convert_tokens_to_ids(tok)
        print(f"{tok:12} -> ID {tok_id}")

    print("\n=== Vocab Size ===")
    print(f"Total tokens in vocab: {len(tokenizer)}")

    if test_inputs:
        print("\n=== Tokenization Test ===")
        for text in test_inputs:
            print(f"\nInput: {text}")
            enc = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=20)
            ids = enc["input_ids"][0].tolist()
            tokens = tokenizer.convert_ids_to_tokens(ids)
            for tid, tok in zip(ids, tokens):
                print(f"  {tid:5} -> {tok}")

if __name__ == "__main__":
    special = ["[reflect]", "[adjust]", "[clarify]", "[expand]", "[summarize]", "[ask]", "[reject]"]
    samples = [
        "hello world",
        "please [reflect] on this",
        "[adjust] my trajectory",
        "[clarify] what I should do next",
        "how to [summarize] information",
    ]

    inspect_tokens("distilbert-base-uncased", special_tokens=special, test_inputs=samples)