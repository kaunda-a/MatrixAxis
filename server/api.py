from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from browser_manager import BrowserManager, BrowserProfile

app = FastAPI()
browser_manager = BrowserManager()

class ProfileConfig(BaseModel):
    proxy: Optional[Dict] = None
    viewport: Dict = {"width": 1920, "height": 1080}
    user_agent: Optional[str] = None
    fingerprint_config: Optional[Dict] = None
    stealth_config: Optional[Dict] = None

@app.post("/browser/{profile_id}/create")
async def create_browser(profile_id: str, config: ProfileConfig):
    """Create a new browser instance with the specified profile"""
    profile = BrowserProfile(**config.dict())
    success = await browser_manager.create_browser(profile_id, profile)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to create browser instance")
    return {"status": "success"}

@app.post("/browser/{profile_id}/navigate")
async def navigate(profile_id: str, url: str):
    """Navigate to URL using specified browser profile"""
    instance = browser_manager._browser_instances.get(profile_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Browser instance not found")
        
    success = await instance.navigate(url)
    if not success:
        raise HTTPException(status_code=400, detail="Navigation failed")
        
    content = await instance.get_page_content()
    return {
        "status": "success",
        "content": content
    }

@app.delete("/browser/{profile_id}")
async def delete_browser(profile_id: str):
    """Close and cleanup browser instance"""
    success = await browser_manager.close_browser(profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Browser instance not found")
    return {"status": "success"}