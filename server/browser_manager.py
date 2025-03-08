import os
from dataclasses import dataclass
from typing import Optional, Dict, List
import asyncio
from playwright.async_api import async_playwright
import logging

@dataclass
class BrowserProfile:
    """Browser profile configuration"""
    proxy: Optional[dict] = None
    viewport: dict = {"width": 1920, "height": 1080}
    user_agent: Optional[str] = None
    fingerprint_config: dict = None
    stealth_config: dict = None

class BrowserManager:
    def __init__(self):
        self._browser_instances: Dict[str, "BrowserInstance"] = {}
        self._logger = logging.getLogger(__name__)

    async def create_browser(self, profile_id: str, profile: BrowserProfile) -> bool:
        """Create a new browser instance with the given profile"""
        try:
            if profile_id in self._browser_instances:
                return False
                
            instance = BrowserInstance(profile)
            await instance.initialize()
            self._browser_instances[profile_id] = instance
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to create browser: {str(e)}")
            return False

    async def close_browser(self, profile_id: str) -> bool:
        """Close a browser instance"""
        try:
            instance = self._browser_instances.get(profile_id)
            if instance:
                await instance.cleanup()
                del self._browser_instances[profile_id]
                return True
            return False
        except Exception as e:
            self._logger.error(f"Failed to close browser: {str(e)}")
            return False

class BrowserInstance:
    def __init__(self, profile: BrowserProfile):
        self.profile = profile
        self._browser = None
        self._context = None
        self._page = None

    async def initialize(self):
        """Initialize browser instance with anti-detection features"""
        playwright = await async_playwright().start()
        
        # Configure browser launch options with enhanced privacy
        launch_options = {
            "headless": True,
            "executable_path": os.environ.get("PLAYWRIGHT_CHROMIUM_PATH"),
            "args": [
                "--enable-playwright-integration",
                "--deep-tls-fingerprinting",
                "--anti-automation-detection",
                "--fingerprinting-canvas-image-data-noise",
                "--disable-search-engine-collection",
                "--set-ipv6-probe-false"
            ]
        }

        # Add proxy configuration if specified
        if self.profile.proxy:
            launch_options["proxy"] = {
                "server": f"{self.profile.proxy['host']}:{self.profile.proxy['port']}",
                "username": self.profile.proxy.get("username"),
                "password": self.profile.proxy.get("password")
            }

        self._browser = await playwright.chromium.launch(**launch_options)

        # Configure context with anti-fingerprinting
        context_options = {
            "viewport": self.profile.viewport,
            "user_agent": self.profile.user_agent,
            "proxy": launch_options.get("proxy"),
            
            # Enhanced privacy features
            "js_enabled": True,
            "bypass_csp": True,
            "ignore_https_errors": True,
            
            # Anti-fingerprinting
            "timezone_id": "UTC",
            "locale": "en-US",
            "permissions": ["geolocation"],
            "geolocation": {"latitude": 0, "longitude": 0},
            
            # Additional hardening
            "proxy_bypass_list": None,
            "accept_downloads": False
        }

        self._context = await self._browser.new_context(**context_options)
        self._page = await self._context.new_page()

    async def cleanup(self):
        """Clean up browser resources"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()

    async def navigate(self, url: str) -> bool:
        """Navigate to URL with stealth"""
        try:
            # Add random delays to appear more human-like
            await asyncio.sleep(0.5 + random.random())
            
            response = await self._page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )
            return response.ok

        except Exception as e:
            logging.error(f"Navigation failed: {str(e)}")
            return False

    async def get_page_content(self) -> Optional[str]:
        """Get current page content"""
        try:
            return await self._page.content()
        except Exception as e:
            logging.error(f"Failed to get content: {str(e)}")
            return None
