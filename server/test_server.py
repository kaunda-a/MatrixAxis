import pytest
import asyncio
from browser_manager import BrowserManager, BrowserProfile

@pytest.mark.asyncio
async def test_browser_creation():
    manager = BrowserManager()
    profile = BrowserProfile()
    
    success = await manager.create_browser("test_profile", profile)
    assert success == True
    
    # Test navigation
    instance = manager._browser_instances["test_profile"]
    success = await instance.navigate("https://example.com")
    assert success == True
    
    # Cleanup
    await manager.close_browser("test_profile")

if __name__ == "__main__":
    asyncio.run(test_browser_creation())