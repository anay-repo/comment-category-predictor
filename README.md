# 💬 Comment Category Prediction Challenge

> Text classification pipeline using LightGBM + TF-IDF to predict comment categories from 198K+ samples — **91% accuracy**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Hugging_Face-orange)](https://huggingface.co/spaces/Anaysingh10/comment-category-predictor)
[![GitHub Pages](https://img.shields.io/badge/🌐_Project_Site-GitHub_Pages-blue)](https://anay-repo.github.io/comment-category-predictor)
[![Kaggle](https://img.shields.io/badge/📓_Notebook-Kaggle-20BEFF)](https://kaggle.com/code/anaysingh10/23f3000736-notebook-t12026)

---

## 🔗 Quick Links

| | Link |
|---|---|
| 🚀 **Live Demo** | [huggingface.co/spaces/Anaysingh10/comment-category-predictor](https://huggingface.co/spaces/Anaysingh10/comment-category-predictor) |
| 🌐 **Project Showcase Page** | [anay-repo.github.io/comment-category-predictor](https://anay-repo.github.io/comment-category-predictor) |
| 📓 **Kaggle Notebook** | [View Full Notebook](https://kaggle.com/code/anaysingh10/23f3000736-notebook-t12026) |

---

## 📌 Problem Statement

Given a dataset of **198,000+ user comments** from an online platform — including text content, interaction metadata, and internal system signals — predict which of 4 internal categories the platform assigns to each comment.

---

## 🏷️ Categories

| Label | Name | Description |
|---|---|---|
| 💬 0 | **Normal** | Most common (~57%). Regular everyday comment with average engagement. |
| ⭐ 1 | **Popular** | High upvote engagement. Well-liked by the community — like a "top comment" on Reddit. |
| 🔥 2 | **Controversial** | High upvotes AND downvotes. Divisive comment that splits the community. |
| 👻 3 | **Ignored** | Short, minimal engagement. Throwaway reply nobody reacted to. |

---

## ⚙️ Pipeline

```
Raw Text + Metadata
       ↓
Text Cleaning (lowercase, remove URLs, special chars)
       ↓
Feature Engineering (comment_len, word_count, exclaim_count, question_count)
       ↓
TF-IDF Vectorization
  ├── Word-level (10K features, ngram 1-2)
  └── Char-level (8K features, ngram 3-4)
       ↓
Combine with Numerical Features (upvote, downvote, emoticons, internal signals)
       ↓
Model Training & Comparison
  ├── Naive Bayes     → 72%
  ├── Logistic Reg.   → 81%
  └── LightGBM        → 91% ✅ Best
       ↓
Hyperparameter Tuning (RandomizedSearchCV)
       ↓
Final Model: LightGBM (n_estimators=300, lr=0.08, class_weight='balanced')
```

---

## 📊 Results

| Model | Accuracy |
|---|---|
| Naive Bayes | 72% |
| Logistic Regression | 81% |
| **LightGBM** | **91% ✅** |

---

## 🛠️ Tech Stack

- **Language:** Python
- **ML:** LightGBM, Scikit-learn
- **NLP:** TF-IDF (word + char n-grams)
- **Data:** Pandas, NumPy, SciPy
- **Visualization:** Matplotlib, Seaborn
- **Deployment:** Hugging Face Spaces, Gradio
- **Platform:** Kaggle

---

## 📁 Repository Structure

```
comment-category-predictor/
├── index.html                          # GitHub Pages showcase site
├── app.py                              # Hugging Face Gradio app
├── requirements.txt                    # Dependencies
└── 23f3000736-notebook-t12026.ipynb   # Full Kaggle notebook
```

---

## 🚀 Try the Live Demo

Visit the live demo and type any comment to see the model classify it in real time:

👉 **[huggingface.co/spaces/Anaysingh10/comment-category-predictor](https://huggingface.co/spaces/Anaysingh10/comment-category-predictor)**

---

## 👤 Author

**Anay Singh**
- GitHub: [@anay-repo](https://github.com/anay-repo)
- Hugging Face: [@Anaysingh10](https://huggingface.co/Anaysingh10)
