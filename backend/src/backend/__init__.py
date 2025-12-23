def development():
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

def production():
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7860)