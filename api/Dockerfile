FROM python:3.11-slim
WORKDIR /app
RUN pip install --upgrade fastapi uvicorn langchain openai langchain_community langchain-groq
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
