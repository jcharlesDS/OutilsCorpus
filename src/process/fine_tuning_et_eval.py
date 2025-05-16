""" Fine-tuning et évaluation

Script de fine-tuning et d'évaluation de la perplexité.
"""

import os
import json
import torch
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from sklearn.model_selection import train_test_split

# Paramètres généraux
MODEL_NAME = "dbddv01/gpt2-french-small"
MAX_LENGTH = 512
BATCH_SIZE = 2
EPOCHS = 3
CORPUS_PATH = input("Chemin du fichier JSON (corpus) : ")
OUTPUT_DIR = input("Chemin du dossier de sortie : ")


# Chargements des données
def load_paroles_from_json(path):
    """
    Charge le corpus en format JSON
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    textes = []
    for item in data:
        titre = item.get("titre", "Sans titre")
        themes = ", ".join(item.get("themes", []))
        paroles = item.get("paroles", "")
        if paroles:
            texte = f"Titre : {titre}\nThèmes : {themes}\n{paroles.strip()}"
            textes.append({"text": texte})
    return Dataset.from_list(textes)

# Initialisation du Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # nécessaire pour éviter une erreur

# Tokenisation
def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, max_length=MAX_LENGTH, padding="max_length")

# Chargement et préparation des jeux d'entraînement et de validation
dataset = load_paroles_from_json(CORPUS_PATH)
dataset = dataset.train_test_split(test_size=0.1, seed=42)
dataset = dataset.map(tokenize_function, batched=True)

# Gestion du modèle
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)

# Gestion de la data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Entraînement
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir=os.path.join(OUTPUT_DIR, "logs"),
    logging_steps=10,
    save_total_limit=2,
    prediction_loss_only=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train()

# Évaluation de la perplexité
eval_results = trainer.evaluate()
perplexity = torch.exp(torch.tensor(eval_results["eval_loss"]))
print(f"\nPerplexité du modèle : {perplexity.item():.2f}")
