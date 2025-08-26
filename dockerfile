# Utiliser Python officiel
FROM python:3.9-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Créer répertoire de travail
WORKDIR /app

# Copier requirements
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier ton code
COPY . .

# Exposer le port Flask
EXPOSE 5000

# Lancer l'app
CMD ["python", "app.py"]