from flask import Flask, request, render_template
from collections import defaultdict
import re
import math

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 1. Получаем файл
        file = request.files["file"]
        text = file.read().decode("utf-8").lower()


        text = re.sub(r"[^a-zа-яё\s]", "", text)
        words = text.split()


        tf = defaultdict(int)
        for word in words:
            tf[word] += 1


        total_words = len(words)
        idf = {}
        for word, count in tf.items():
            idf[word] = math.log(total_words / count)


        sorted_words = sorted(tf.items(), key=lambda x: -x[1])


        top_50_words = sorted_words[:50]


        return render_template(
            "result.html",
            words=top_50_words,
            tf=tf,
            idf=idf
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)