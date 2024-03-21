from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/mailgun/webhook")
async def mailgun_webhook(request: Request):
    data = await request.form()
    # Process the incoming email data here. `data` is a dictionary.
    print(data)  # Just for demonstration, print the data.

    return {"message": "Received"}
