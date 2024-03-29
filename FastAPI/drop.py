from sqlalchemy import MetaData, Table, create_engine

engine = create_engine('sqlite:///hospital.db')  # Use your actual database URL
metadata = MetaData()

# Reflect the tables
metadata.reflect(bind=engine)

# Drop the users table
Table('users', metadata, autoload_with=engine).drop(engine)