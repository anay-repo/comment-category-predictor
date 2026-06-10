import gradio as gr
import joblib
import numpy as np
import re
import pandas as pd
from scipy.sparse import hstack, csr_matrix

model      = joblib.load("lgbm_model.pkl")
tfidf      = joblib.load("tfidf_word.pkl")
tfidf_char = joblib.load("tfidf_char.pkl")
scaler     = joblib.load("scaler.pkl")

LABEL_INFO = {
    0: {
        "emoji": "💬",
        "name": "Normal Comment",
        "simple": "Just a regular, everyday comment.",
        "desc": "This is the most common type (~57% of all comments). A typical reply with nothing particularly special about its engagement or tone — the kind of comment you'd scroll past on any post.",
    },
    1: {
        "emoji": "⭐",
        "name": "Popular Comment",
        "simple": "A well-liked comment the community appreciated.",
        "desc": "This comment received strong positive engagement. Think of it like a 'top comment' on YouTube or Reddit — well-written, useful, or insightful enough that many people upvoted it.",
    },
    2: {
        "emoji": "🔥",
        "name": "Controversial Comment",
        "simple": "A divisive comment — people strongly agree OR disagree.",
        "desc": "This comment triggered strong reactions on both sides. Some people loved it, others hated it. Think of a heated debate comment where the community is split down the middle.",
    },
    3: {
        "emoji": "👻",
        "name": "Ignored Comment",
        "simple": "A short comment that barely got any attention.",
        "desc": "This comment received very little engagement. It's the kind of one-word or throwaway reply that gets lost in the comments section and nobody really reacts to.",
    }
}

NUM_FEATURES = ['emoticon_1','emoticon_2','emoticon_3','upvote','downvote','if_1','if_2','comment_len','word_count','exclaim_count','question_count']

# Engagement level → if_2 mapping (found through model analysis)
# 0 = low engagement → Normal
# 10 = high engagement → Controversial/Popular shift
ENGAGEMENT_MAP = {
    1: 0,   # Low → Normal
    2: 3,   # Below average
    3: 6,   # Average
    4: 9,   # High
    5: 10,  # Very high → Controversial
}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict(comment, engagement):
    if not comment.strip():
        return "⚠️ Please enter a comment.", "", ""

    clean = clean_text(comment)
    if2_val = ENGAGEMENT_MAP[int(engagement)]

    X_tfidf = tfidf.transform([clean])
    X_char  = tfidf_char.transform([clean])

    num_data = pd.DataFrame([{
        'emoticon_1':0,'emoticon_2':0,'emoticon_3':0,
        'upvote':5,'downvote':0,'if_1':0,'if_2':if2_val,
        'comment_len':len(clean),'word_count':len(clean.split()),
        'exclaim_count':comment.count('!'),'question_count':comment.count('?')
    }])

    X_num   = csr_matrix(scaler.transform(num_data[NUM_FEATURES]))
    X_final = hstack([X_tfidf, X_char, X_num])

    pred  = int(model.predict(X_final)[0])
    proba = model.predict_proba(X_final)[0]
    info  = LABEL_INFO[pred]

    conf_lines = []
    labels = ["💬 Normal", "⭐ Popular", "🔥 Controversial", "👻 Ignored"]
    for i, p in enumerate(proba):
        bar_len = int(p * 25)
        bar = "█" * bar_len + "░" * (25 - bar_len)
        conf_lines.append(f"{labels[i]:20s} [{bar}]  {p*100:.1f}%")

    result = f"## {info['emoji']} {info['name']}\n\n**{info['simple']}**\n\n{info['desc']}"
    return result, "\n".join(conf_lines), f"{proba[pred]*100:.1f}%"

with gr.Blocks(
    title="Comment Category Predictor",
    theme=gr.themes.Soft(),
    css="footer { visibility: hidden; } .result-box { font-size: 1.05em; }"
) as demo:

    gr.HTML("""
    <div style='text-align:center; padding:24px 0 8px 0;'>
        <h1 style='font-size:2em; font-weight:700; margin-bottom:6px;'>💬 Comment Category Predictor</h1>
        <p style='color:#888; margin:0;'>Predicts the platform category assigned to a comment using a trained LightGBM model</p>
        <p style='font-size:0.82em; color:#666; margin-top:4px;'>
            Built for the <b>Comment Category Prediction Challenge</b> &nbsp;·&nbsp;
            Model: LightGBM &nbsp;·&nbsp; Features: TF-IDF (word + char n-grams) + Numerical
        </p>
    </div>
    <div style='display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin:16px 0 24px 0;'>
        <div style='background:#111827; border:1.5px solid #4CAF50; border-radius:12px; padding:12px 20px; text-align:center; min-width:130px;'>
            <div style='font-size:1.5em;'>💬</div>
            <div style='font-weight:700; color:#4CAF50;'>Normal</div>
            <div style='font-size:0.75em; color:#aaa; margin-top:2px;'>Regular comment,<br>average engagement</div>
        </div>
        <div style='background:#111827; border:1.5px solid #2196F3; border-radius:12px; padding:12px 20px; text-align:center; min-width:130px;'>
            <div style='font-size:1.5em;'>⭐</div>
            <div style='font-weight:700; color:#2196F3;'>Popular</div>
            <div style='font-size:0.75em; color:#aaa; margin-top:2px;'>High upvotes,<br>community favourite</div>
        </div>
        <div style='background:#111827; border:1.5px solid #FF9800; border-radius:12px; padding:12px 20px; text-align:center; min-width:130px;'>
            <div style='font-size:1.5em;'>🔥</div>
            <div style='font-weight:700; color:#FF9800;'>Controversial</div>
            <div style='font-size:0.75em; color:#aaa; margin-top:2px;'>Divisive — people<br>strongly agree/disagree</div>
        </div>
        <div style='background:#111827; border:1.5px solid #9C27B0; border-radius:12px; padding:12px 20px; text-align:center; min-width:130px;'>
            <div style='font-size:1.5em;'>👻</div>
            <div style='font-weight:700; color:#9C27B0;'>Ignored</div>
            <div style='font-size:0.75em; color:#aaa; margin-top:2px;'>Short, minimal<br>engagement</div>
        </div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=2):
            comment_input = gr.Textbox(
                label="✏️ Type any comment",
                placeholder="e.g. This is the best explanation I have ever read!",
                lines=4
            )
            engagement_slider = gr.Slider(
                minimum=1, maximum=5, value=1, step=1,
                label="📊 How much attention did this comment get?",
                info="1 = Almost none  ·  3 = Moderate  ·  5 = Went viral / very controversial"
            )
            predict_btn = gr.Button("🔍 Predict Category", variant="primary", size="lg")

        with gr.Column(scale=2):
            result_out     = gr.Markdown(label="Result", elem_classes=["result-box"])
            confidence_out = gr.Textbox(label="📊 Model confidence across all categories", lines=6)
            score_out      = gr.Textbox(label="✅ Confidence in top prediction")

    predict_btn.click(
        fn=predict,
        inputs=[comment_input, engagement_slider],
        outputs=[result_out, confidence_out, score_out]
    )

    gr.Examples(
        examples=[
            ["ok", 1],
            ["sure", 1],
            ["This is honestly one of the best posts I have ever read. So detailed and helpful!", 5],
            ["I completely disagree with this. This is misleading and people need to stop sharing it.", 5],
            ["Great post, thanks for sharing!", 2],
            ["This changed my entire perspective on the topic. Incredible work, thank you.", 4],
        ],
        inputs=[comment_input, engagement_slider],
        label="📌 Click any example to try it instantly!"
    )

    gr.HTML("""
    <div style='text-align:center; margin-top:28px; color:#666; font-size:0.83em; padding-bottom:16px;'>
        Built by <b>Anay Singh</b> &nbsp;·&nbsp;
        <a href='https://github.com/anaysingh10' target='_blank' style='color:#888;'>GitHub</a>
    </div>
    """)

demo.launch()