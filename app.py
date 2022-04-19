from flask import Flask, render_template, request

import core


app = Flask(__name__)


@app.route("/")
def main():
    data = {
        "Ну, что такое ассоциативные массивы ты, надеюсь, знаешь": "Сюда ты передаёшь данные для шаблона,"
                                                                   " которые потом сможешь в нём использовать.",
        "kek": "Там уже будешь рисовать привычный ХЭТЭЭМЭЛЬ, то в местах где надо использовать данные или какие-либо"
               " питоновские конструкции, будешь использовать специфический синтаксис шаблонизатора Jinja",
        "jinja_doc": "https://docs-python.ru/packages/modul-jinja2-python/sintaksis-shablona-jinja2/",
    }
    return render_template("index.html", data=data)


@app.route('/video')
def video():
    video_id = request.args.get("url")
    data = {
        "Ну, что такое ассоциативные массивы ты, надеюсь, знаешь": "Сюда ты передаёшь данные для шаблона,"
                                                                   " которые потом сможешь в нём использовать.",
        "kek": "Там уже будешь рисовать привычный ХЭТЭЭМЭЛЬ, то в местах где надо использовать данные или какие-либо"
               " питоновские конструкции, будешь использовать специфический синтаксис шаблонизатора Jinja",
        "jinja_doc": "https://docs-python.ru/packages/modul-jinja2-python/sintaksis-shablona-jinja2/",
    }

    try:
        comments = core.video_comments(video_id)
        clean_comments = core.clean_comments(comments)
        lem_comments = core.lemmatize(clean_comments)
        word_count = core.word_count(lem_comments)
        wc = core.wordcloud_from_dict(word_count)

        data["comments"] = comments
        data["word_count"] = word_count
        data['wc_svg'] = wc.to_svg()

        return render_template("index.html", data=data)
    except Exception as e:
        return render_template("error.html", error=e, str=str)


if __name__ == "__main__":
    app.run()
