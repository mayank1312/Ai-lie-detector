import pandas as pd
from sklearn.metrics import accuracy_score
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from transformers import Trainer, TrainingArguments
import torch


cols = [
"id","label","statement","subject","speaker","speaker_job_title",
"state_info","party_affiliation","barely_true_counts","false_counts",
"half_true_counts","mostly_true_counts","pants_on_fire_counts","context"
]


train = pd.read_csv("dataset/train.tsv", sep="\t", names=cols, header=None)
test = pd.read_csv("dataset/test.tsv", sep="\t", names=cols, header=None)

train = train[["statement","label"]]
test = test[["statement","label"]]

false_labels = ["pants-fire", "false", "barely-true"]
true_labels = ["half-true", "mostly-true", "true"]

train["label"] = train["label"].apply(lambda x: 0 if x in false_labels else 1)
test["label"] = test["label"].apply(lambda x: 0 if x in false_labels else 1)


tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

train_encodings = tokenizer(list(train["statement"]), truncation=True, padding=True)
test_encodings = tokenizer(list(test["statement"]), truncation=True, padding=True)


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, train["label"].tolist())
test_dataset = Dataset(test_encodings, test["label"].tolist())


model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)


training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_dir="./logs",
    logging_steps=100
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)


trainer.train()


predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(axis=1)

accuracy = accuracy_score(test["label"], preds)
print("Accuracy:", accuracy)


model.save_pretrained("model/bert_model")
tokenizer.save_pretrained("model/bert_model")

print("BERT model saved successfully")