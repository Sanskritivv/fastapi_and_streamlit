from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), file_name: str = Form(...)):
    df = pd.read_csv(file.file)
    # Perform any required data processing here
    return {
        "file_name": file_name,
        "columns": df.columns.tolist(),
        "data": df.head().to_dict(orient="records")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

