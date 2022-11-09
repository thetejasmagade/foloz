from fastapi import FastAPI
from deta import Deta
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import env

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Initialize with a Project Key
deta = Deta(env.project_key)

# This how to connect to or create a database.
usernames_db = deta.Base("usernames_db")



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/usernames/")
def get_usernames():
    res = usernames_db.fetch()
    all_items = res.items
    while res.last:
        res = usernames_db.fetch(last=res.last)
        all_items += res.items

    return jsonable_encoder(all_items)



# @app.get("/api/username/")
# def get_usernames():
#     res = usernames_db.fetch()
#     username = usernames_db.put({
#         "id": res._count + 1,
#         "username": "thetejasmagade",
#     })

#     return jsonable_encoder(username)
