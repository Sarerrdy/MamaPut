# import secrets

# Generate a strong secret key
# secret_key = secrets.token_urlsafe(32)
# print(secret_key)

# from werkzeug.security import generate_password_hash

# key = generate_password_hash('hjndh87364485')
# print(key)


from sqlalchemy import create_engine, MetaData

engine = create_engine(
    'sqlite:////home/sarerrdy/Portfolio-Proj/mama_put/mamaput.db')
metadata = MetaData()
metadata.reflect(bind=engine)
alembic_version = metadata.tables.get('alembic_version')
if alembic_version is not None:
    alembic_version.drop(engine)
