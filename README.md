# siminer

similer > siminer < ner

## How to use

### Knowledge Data

First load your data

```python
from siminer.Knowledge import Knowledge

# load data from folder content json
know = Knowledge.json_folder_factory("data/")

# lemmatiz data
know.lemmatiz_data()
```

you can use csv or json (file or folder)

```python
from siminer.Knowledge import Knowledge

know = Knowledge.json_folder_factory("data/")
know = Knowledge.json_file_factory("data.json")
know = Knowledge.csv_folder_factory("data/")
know = Knowledge.csv_file_factory("data.csv")
```

#### Json Format

```json
{
    "labels": {
        "ab": [
            "AB - Agriculture Biologique",
            "Biologique",
            "Bio",
            "AB",
            "ab"
        ]
    }
}
```

```csv
Valeur,Texte,,,
ab,AB - Agriculture Biologique,Biologique,Bio,AB
```

### Recognize sentence

Recognize sentence to pyton dict

```python
from siminer.Recognizer import Recognize

rec = Recognize.knowledge_factory(know)
result = rec.ner_text(
    "J'ai 270kg de Legumes type Navets variété Navets rond violets en cagette  qui viennent de États-Unis d'Amérique avec le label Transport Bateau")

print(result)
```

```python
{'pays': [{'value': 'US', 'confidence': 1}], 'labels': [{'value': 'by-boat', 'confidence': 1}],
 'quantite': [{'value': '270kg', 'confidence': 1}], 'conditionnement': [{'value': 'box', 'confidence': 1}]}
```

Recognize sentence to json

```python
from siminer.Recognizer import Recognize

rec = Recognize.knowledge_factory(know)
result = rec.ner_text_json(
    "J'ai 270kg de Legumes type Navets variété Navets rond violets en cagette  qui viennent de États-Unis d'Amérique avec le label Transport Bateau")

print(result)
```

```json
{
    "pays": [
        {
            "value": "US",
            "confidence": 1
        }
    ],
    "labels": [
        {
            "value": "by-boat",
            "confidence": 1
        }
    ],
    "quantite": [
        {
            "value": "270kg",
            "confidence": 1
        }
    ],
    "famille": [
        {
            "value": "vegetables",
            "confidence": 0.8333333333333334
        }
    ],
    "sous-famille": [
        {
            "value": "turnip",
            "confidence": 0.8888888888888888
        },
        {
            "value": "turnip",
            "confidence": 0.8888888888888888
        }
    ],
    "conditionnement": [
        {
            "value": "box",
            "confidence": 0.9230769230769231
        }
    ]
}
```

## Authors

- [Doha Sadiq](https://github.com/SADIQdoha)
- [Yassine Mougou](https://github.com/ymougou)
- Lucas Auxachs
- [Alexis Devleeschauwer](https://github.com/devleesch001)
- [Tony Wullepit](https://github.com/wullepit)
