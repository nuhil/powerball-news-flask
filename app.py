import connexion
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR)
# logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
