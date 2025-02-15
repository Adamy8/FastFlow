from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],    # only nextjs frontend url
    # allow_origins=["*"],                      # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
# def health_check():
#     return "Health check complete"

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}