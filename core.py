import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/hello-world-<variant>", methods=["GET"])
def home(variant):
    """Endpoint return variant"""
    return f"Hello world {variant}"


if __name__ == "__main__":
    app.run()