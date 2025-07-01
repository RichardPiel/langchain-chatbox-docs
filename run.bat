@echo off
docker run --rm -p 8000:8000 ^
  -e OPENAI_API_KEY=sk-proj-lJMkj ^
  -v "%cd%/docs:/app/docs" ^
  pdf-chatbot-ui 