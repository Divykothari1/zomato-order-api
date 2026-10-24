# 1. Official Python lightweight image use kar rahe hain
FROM python:3.12-slim

# 2. Container ke andar working directory set kar rahe hain
WORKDIR /app

# 3. Pehle requirements.txt copy karo aur dependencies install karo (Caching optimize karne ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Baaki ka poora code container mein copy kar do
COPY . .

# 5. Port expose karo jahan FastAPI run hoga
EXPOSE 8000

# 6. Container start hote hi uvicorn server chalane ki command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]