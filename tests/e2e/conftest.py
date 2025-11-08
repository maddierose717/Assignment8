import os
import pytest

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None

def _playwright_usable() -> bool:
    # allow manual override: FORCE_E2E=1 pytest ...
    if os.getenv("FORCE_E2E") == "1":
        return True
    if sync_playwright is None:
        return False
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)  # fails if OS libs missing
            b.close()
        return True
    except Exception:
        return False

# Skip all tests in this directory if the host can't run Playwright browsers
pytestmark = pytest.mark.skipif(
    not _playwright_usable(),
    reason="Playwright browser dependencies missing on this machine; run E2E in CI or set FORCE_E2E=1 after installing deps."
)
