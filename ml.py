import torch
from torch.utils.data import Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

def main():

    # Load pre-trained GPT-2 model and tokenizer
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Load chat data from a text file
    file_path = "sample.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        chat_data = file.readlines()

    tokenizer.pad_token = " "

    # Tokenize and format the chat data
    input_ids = tokenizer(chat_data, return_tensors="pt", padding=True, truncation=True)["input_ids"]

    # Create a custom PyTorch dataset
    class ChatDataset(Dataset):
        def __init__(self, input_ids):
            self.input_ids = input_ids

        def __len__(self):
            return len(self.input_ids)

        def __getitem__(self, idx):
            return {"input_ids": self.input_ids[idx]}

    # Prepare the training dataset
    dataset = ChatDataset(input_ids)

    # Configure training settings
    training_args = TrainingArguments(
        output_dir="./gpt2-finetuned",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=100,
        save_steps=20_000,
        save_total_limit=2,
    )

    # Use DataCollatorForLanguageModeling to handle padding
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Train the model
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()
    
    # Generate text based on user input
    user_input = "User: Hi! How are you?"
    input_ids = tokenizer.encode(user_input, return_tensors="pt").to('cuda')

    # Generate response
    output_ids = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

    # Decode and print the generated response
    generated_response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(generated_response)

if __name__ == "__main__":
    main()
