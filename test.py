import re
import json
string="""
```json
[
  {
    "mcq": "Who coined the term 'machine learning'?",
    "options": {
      "a": "Donald Hebb",
      "b": "Walter Pitts",
      "c": "Arthur Samuel",
      "d": "Tom M. Mitchell"
    },
    "correct": "c"
  },
  {
    "mcq": "Which of the following is NOT mentioned as an application of Machine Learning in the provided text?",
    "options": {
      "a": "Email filtering",
      "b": "Agriculture",
      "c": "Quantum Computing",
      "d": "Speech recognition"
    },
    "correct": "c"
  },
  {
    "mcq": "What is the focus of Data mining, a field related to machine learning?",
    "options": {
      "a": "Prediction based on training data",
      "b": "Exploratory data analysis via unsupervised learning",
      "c": "Development of statistical algorithms",
      "d": "Minimization of loss functions"
    },
    "correct": "b"
  }]
 ``` 
"""

json_text = re.sub(r"```json|", "", string).strip()
json_text = re.sub(r"```", "", json_text).strip()
print(json.loads(json_text))