import evars

from restservice import create_app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=evars.FLASK_HOST,
        debug=evars.DEBUG,
        port=evars.FLASK_PORT,
        threaded=True
    )
