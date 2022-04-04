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
        data["comments"] = comments
        return render_template("index.html", data=data)
    except Exception as e:
        return render_template("error.html", error=e, str=str)  # Если хочешь использовать функции, их тоже нужно передать


if __name__ == "__main__":
    app.run()
