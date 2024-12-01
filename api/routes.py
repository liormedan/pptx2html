from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
import sys

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
from pptx2html.main import convert_to_html

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert")
async def convert_pptx(file: UploadFile = File(...)):
    """Convert PowerPoint to HTML and return JSON response"""
    if not file.filename.endswith('.pptx'):
        raise HTTPException(status_code=400, detail="Only .pptx files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Convert to HTML
        result = convert_to_html(temp_path, output_type='json')
        
        # Clean up
        os.unlink(temp_path)
        
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/convert/standalone")
async def convert_pptx_standalone(file: UploadFile = File(...)):
    """Convert PowerPoint to standalone HTML page"""
    if not file.filename.endswith('.pptx'):
        raise HTTPException(status_code=400, detail="Only .pptx files are supported")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pptx') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Convert to standalone HTML
        result = convert_to_html(temp_path, output_type='standalone')
        
        # Clean up
        os.unlink(temp_path)
        
        return HTMLResponse(content=result['html'], media_type='text/html')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/embed/{presentation_id}")
async def get_embedded_presentation(presentation_id: str):
    """Serve an embedded presentation"""
    try:
        # Here you would typically load the presentation from your storage
        # For now, we'll return a placeholder HTML
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="utf-8">
            <title>מצגת מוטמעת</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto p-4">
                <h1 class="text-2xl mb-4">מצגת {presentation_id}</h1>
                <div class="bg-white rounded-lg shadow-lg p-4">
                    <!-- Presentation content would go here -->
                    <p>המצגת תוצג כאן</p>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Presentation not found")
