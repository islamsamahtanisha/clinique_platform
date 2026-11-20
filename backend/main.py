import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(title="ClinicMD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
)


@app.get("/health")
def health():
    return {"api": "ok"}


@app.get("/health/db")
def database_health():
    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            connect_timeout=3,
        ) as connection:
            connection.execute("SELECT 1").fetchone()
    except KeyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Variable de configuration manquante : {error.args[0]}",
        ) from error
    except psycopg.OperationalError as error:
        raise HTTPException(
            status_code=503,
            detail="Connexion à PostgreSQL impossible",
        ) from error

    return {"database": "ok"}