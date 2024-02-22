# Utilisez une image Python officielle comme base
FROM python:3.9

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le script Python et le dossier de données dans le conteneur
COPY hello_world.py /app/
COPY data /app/data

# Installez les dépendances (par exemple, si votre script utilise des bibliothèques spécifiques)
# RUN pip install -r requirements.txt
RUN pip install pandas

# Commande pour exécuter le script Python
CMD ["python", "hello_world.py"]
