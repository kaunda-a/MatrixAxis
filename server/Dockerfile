FROM python:3.9-slim-bullseye

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # Add only runtime dependencies here
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the pre-built Chromium from your local build
COPY ./chromium/ungoogled-chromium/out/Default/chrome /usr/local/chromium/chrome
COPY ./chromium/ungoogled-chromium/out/Default/chromedriver /usr/local/chromium/chromedriver

# Set environment variable for Playwright
ENV PLAYWRIGHT_CHROMIUM_PATH=/usr/local/chromium/chrome

# Copy application code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
