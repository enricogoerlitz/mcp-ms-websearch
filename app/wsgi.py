# import evars

from service import create_app


app = create_app()

if __name__ == "__main__":
    print("blub")
    # app.run(
    #     host=evars.FLASK_HOST,
    #     debug=evars.DEBUG,
    #     port=evars.FLASK_PORT,
    # )
