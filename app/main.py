from app import app, db
import view
from stands.stands_blueprint import stands
from article.article_blueprint import article


app.register_blueprint(article, url_prefix='/article')
app.register_blueprint(stands, url_prefix='/museumstands')


if __name__ == "__main__":
    app.run()
