import uvicorn
from fastapi import FastAPI, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

app = FastAPI(title="Echo Annotation App")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page for file upload"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """Handle file upload and process CSV"""
    # Save the uploaded file
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Add last_update column if it doesn't exist
    if "last_update" not in df.columns:
        df["last_update"] = ""
        df.to_csv(file_path, index=False)
    
    return RedirectResponse(url=f"/table?file={file.filename}", status_code=303)

@app.get("/table", response_class=HTMLResponse)
async def table_view(request: Request, file: str, page: int = 1):
    """Display table of reports with pagination"""
    file_path = f"data/{file}"
    df = pd.read_csv(file_path)
    
    # Pagination
    items_per_page = 20
    total_pages = (len(df) + items_per_page - 1) // items_per_page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(df))
    
    page_data = df.iloc[start_idx:end_idx]
    
    return templates.TemplateResponse(
        "table.html", 
        {
            "request": request,
            "data": page_data.to_dict(orient="records"),
            "file": file,
            "current_page": page,
            "total_pages": total_pages,
            "total_records": len(df)
        }
    )

@app.get("/annotate/{index}", response_class=HTMLResponse)
async def annotate_view(request: Request, index: int, file: str):
    """View for annotating a specific report"""
    file_path = f"data/{file}"
    df = pd.read_csv(file_path)
    
    if index < 0 or index >= len(df):
        return RedirectResponse(url=f"/table?file={file}", status_code=303)
    
    row = df.iloc[index].to_dict()
    
    # Get fields to annotate
    annotation_fields = [
        "LVH", "LV dilated", "LV impaired", "RV dilated", "RV impaired",
        "AS mod severe", "AR mod severe", "MS mod severe", "MR mod severe", 
        "TR mod severe", "Pericardial effusion", "Prosthetic valve"
    ]
    
    return templates.TemplateResponse(
        "annotate.html", 
        {
            "request": request,
            "row": row,
            "file": file,
            "index": index,
            "annotation_fields": annotation_fields,
            "next_index": min(index + 1, len(df) - 1)
        }
    )

@app.post("/save-annotation")
async def save_annotation(
    request: Request,
    file: str = Form(...),
    index: int = Form(...),
    next_action: str = Form(...)
):
    """Save annotation data back to CSV"""
    file_path = f"data/{file}"
    df = pd.read_csv(file_path)
    
    # Get form data for annotation fields
    form_data = await request.form()
    
    # Update annotation fields
    annotation_fields = [
        "LVH", "LV dilated", "LV impaired", "RV dilated", "RV impaired",
        "AS mod severe", "AR mod severe", "MS mod severe", "MR mod severe", 
        "TR mod severe", "Pericardial effusion", "Prosthetic valve"
    ]
    
    for field in annotation_fields:
        value = form_data.get(field, None)
        if value is not None:
            if value == "yes":
                df.at[index, field] = 1
            elif value == "no":
                df.at[index, field] = 0
    
    # Update last_update timestamp
    df.at[index, "last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save back to CSV
    df.to_csv(file_path, index=False)
    
    # Determine where to redirect based on next_action
    if next_action == "next":
        next_index = min(index + 1, len(df) - 1)
        return RedirectResponse(url=f"/annotate/{next_index}?file={file}", status_code=303)
    elif next_action == "table":
        return RedirectResponse(url=f"/table?file={file}", status_code=303)
    else:  # save (stay on same page)
        return RedirectResponse(url=f"/annotate/{index}?file={file}", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
