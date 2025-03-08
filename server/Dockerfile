FROM python:3.9-slim-bullseye

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
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

# Create directory for Chromium
RUN mkdir -p /usr/local/chromium

# Copy the custom built Chromium
COPY ./chromium/ungoogled-chromium/build/src/out/Default/chrome /usr/local/chromium/chrome
COPY ./chromium/ungoogled-chromium/build/src/out/Default/chromedriver /usr/local/chromium/chromedriver

# Set permissions
RUN chmod +x /usr/local/chromium/chrome /usr/local/chromium/chromedriver

# Set environment variable for Playwright
ENV PLAYWRIGHT_CHROMIUM_PATH=/usr/local/chromium/chrome

# Copy application code and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
