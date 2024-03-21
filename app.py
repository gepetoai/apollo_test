from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/mailgun/webhook")
async def mailgun_webhook(request: Request):
    try:
        data = await request.form()
        # Process the incoming email data here. `data` is a dictionary.
        print('form ', data)  # Just for demonstration, print the data.
    except Exception as e:
        print('form ', e)
        return {"message": "Error"}
    try:
        data = await request.json()
        # Process the incoming email data here. `data` is a dictionary.
        print('json ', data)  # Just for demonstration, print the data.
    except Exception as e:
        print('json ', e)
        return {"message": "Error"}


    return {"message": "Received"}


#add health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}