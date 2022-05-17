from flask import Flask, render_template, request

import core


app = Flask(__name__)


@app.route("/")
def main():
    data = { }
    return render_template("index.html", data=data)


@app.route('/video')
def video():
    video_id = request.args.get("url")
    data = {}

    try:
        comments = core.video_comments(video_id)
        clean_comments = core.clean_comments(comments)
        lem_comments = core.lemmatize(clean_comments)
        clean_comments = core.clean_stop_words(lem_comments)
        word_count = core.word_count(clean_comments)
        wc = core.wordcloud_from_dict(word_count)

        polarity_data = core.get_polarity(clean_comments)
        core.get_graph(polarity_data)


        #data["comments"] = comments
        #data["word_count"] = word_count

        data['wc_svg'] = wc.to_svg()

        data["graph"] = "images/img.png"

        return render_template("index.html", data=data)
    except Exception as e:
        return render_template("error.html", error=e, str=str)


if __name__ == "__main__":
    app.run()
