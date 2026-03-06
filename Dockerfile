# The comment below is like that because this is the first time for me to create a Dockerfile, so i need that comment so that i can understand the purpose of this file. This Dockerfile is used to create a Docker image for the book recommendation system. 
# The Docker image will contain all the necessary dependencies and configurations to run the application in a containerized environment.

# 1. Pilih sistem operasi dasar
FROM python:3.9-slim

# 2. Tentukan folder kerja di dalam peti kemas Docker
WORKDIR /app

# 3. Copy file setup, requirements, dan README (LUBANGKAN DULU)
COPY setup.py requirements.txt README.md ./

# 4. Install semua library yang dibutuhkan tanpa menyimpan cache sampah
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy SELURUH sisa kodinganmu ke dalam Docker
COPY . .

# 6. Kasih tahu Docker bahwa website ini akan jalan di port 8501
EXPOSE 8501

# 7. Perintah otomatis yang akan dijalankan saat Docker dinyalakan
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]