# 🤖 Chatbot PDF avec LangChain

Une application de chatbot intelligente qui permet de poser des questions sur vos documents PDF en utilisant LangChain, OpenAI et FastAPI.

## 📋 Fonctionnalités

- **Interface de chat moderne** : Interface web intuitive avec Vue.js
- **Traitement intelligent des PDF** : Analyse et indexation automatique des documents
- **Mémoire conversationnelle** : Le chatbot se souvient du contexte de la conversation
- **Cache optimisé** : Les embeddings sont mis en cache pour des performances optimales
- **Déploiement Docker** : Conteneurisation complète pour un déploiement facile
- **Support multilingue** : Interface en français avec support pour différentes langues de documents

## 🛠️ Prérequis

- **Clé API OpenAI** : Vous devez avoir une clé API OpenAI valide
- **Docker** : Pour l'option de déploiement containerisé (recommandé)
- **Python 3.11+** : Pour l'installation locale
- **Git** : Pour cloner le repository

## 📁 Structure du projet

```
langchain-chatbox-docs/
├── main.py              # Application FastAPI principale
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Configuration Docker
├── run.bat             # Script de lancement Windows
├── docs/               # Dossier contenant les fichiers PDF à analyser
├── static/
│   └── index.html      # Interface web du chatbot
└── embeddings_cache/   # Cache des embeddings (créé automatiquement)
```

## 🚀 Installation et Configuration

### Option 1: Déploiement avec Docker (Recommandé)

#### Windows

1. **Cloner le repository**
   ```cmd
   git clone <votre-repository>
   cd langchain-chatbox-docs
   ```

2. **Configurer la clé API OpenAI**
   - Éditez le fichier `run.bat`
   - Remplacez la valeur de `OPENAI_API_KEY` par votre clé API réelle
   ```bat
   -e OPENAI_API_KEY=votre_cle_api_openai_ici ^
   ```

3. **Ajouter vos documents PDF**
   ```cmd
   # Copiez vos fichiers PDF dans le dossier docs/
   copy "vos_fichiers.pdf" docs/
   ```

4. **Construire l'image Docker**
   ```cmd
   docker build -t pdf-chatbot-ui .
   ```

5. **Lancer l'application**
   ```cmd
   run.bat
   ```

#### Linux

1. **Cloner le repository**
   ```bash
   git clone <votre-repository>
   cd langchain-chatbox-docs
   ```

2. **Configurer la clé API OpenAI**
   ```bash
   export OPENAI_API_KEY="votre_cle_api_openai_ici"
   ```

3. **Ajouter vos documents PDF**
   ```bash
   # Copiez vos fichiers PDF dans le dossier docs/
   cp vos_fichiers.pdf docs/
   ```

4. **Construire et lancer l'application**
   ```bash
   # Construire l'image Docker
   docker build -t pdf-chatbot-ui .
   
   # Lancer le conteneur
   docker run --rm -p 8000:8000 \
     -e OPENAI_API_KEY="$OPENAI_API_KEY" \
     -v "$(pwd)/docs:/app/docs" \
     pdf-chatbot-ui
   ```

### Option 2: Installation locale avec Python

#### Windows

1. **Installer Python 3.11+**
   - Téléchargez depuis [python.org](https://www.python.org/downloads/)

2. **Configurer l'environnement**
   ```cmd
   # Cloner le repository
   git clone <votre-repository>
   cd langchain-chatbox-docs
   
   # Créer un environnement virtuel
   python -m venv venv
   venv\Scripts\activate
   
   # Installer les dépendances
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   ```cmd
   set OPENAI_API_KEY=votre_cle_api_openai_ici
   ```

4. **Ajouter vos PDF et lancer**
   ```cmd
   # Copiez vos fichiers PDF dans docs/
   copy "vos_fichiers.pdf" docs/
   
   # Lancer l'application
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

#### Linux

1. **Installer Python 3.11+**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip
   
   # CentOS/RHEL
   sudo yum install python3.11 python3-pip
   ```

2. **Configurer l'environnement**
   ```bash
   # Cloner le repository
   git clone <votre-repository>
   cd langchain-chatbox-docs
   
   # Créer un environnement virtuel
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Installer les dépendances
   pip install -r requirements.txt
   ```

3. **Configurer les variables d'environnement**
   ```bash
   export OPENAI_API_KEY="votre_cle_api_openai_ici"
   ```

4. **Ajouter vos PDF et lancer**
   ```bash
   # Copiez vos fichiers PDF dans docs/
   cp vos_fichiers.pdf docs/
   
   # Lancer l'application
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 📖 Utilisation

1. **Accéder à l'interface**
   - Ouvrez votre navigateur et allez sur `http://localhost:8000`

2. **Premier démarrage**
   - L'application analysera automatiquement tous les fichiers PDF du dossier `docs/`
   - Les embeddings seront créés et mis en cache (cela peut prendre quelques minutes)

3. **Poser des questions**
   - Tapez votre question dans la zone de texte
   - Le chatbot répondra en se basant sur le contenu de vos documents
   - L'historique de conversation est maintenu durant la session

## ⚙️ Configuration avancée

### Variables d'environnement

- `OPENAI_API_KEY` : **Obligatoire** - Votre clé API OpenAI
- `EMBEDDINGS_DIR` : Dossier de cache des embeddings (par défaut: `embeddings_cache`)

### Personnalisation

- **Ajouter/Modifier des PDF** : Placez vos fichiers dans le dossier `docs/`
- **Cache automatique** : Les embeddings sont recalculés seulement si les fichiers PDF changent
- **Mémoire** : La conversation est maintenue pendant la session active

## 🔧 Dépannage

### Problèmes courants

**"La variable d'environnement OPENAI_API_KEY est requise"**
- Vérifiez que votre clé API est correctement configurée
- Assurez-vous qu'elle commence par `sk-`

**"Aucun fichier PDF trouvé dans le dossier docs/"**
- Vérifiez que des fichiers `.pdf` sont présents dans le dossier `docs/`
- Les noms de fichiers ne doivent pas contenir de caractères spéciaux

**Erreurs de port 8000 déjà utilisé**
```bash
# Linux/Mac
sudo lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Problèmes de permissions Docker (Linux)**
```bash
sudo usermod -aG docker $USER
# Puis redémarrez votre session
```

### Logs et débogage

- Les logs de l'application s'affichent dans le terminal
- Pour plus de détails, ajoutez `--log-level debug` à uvicorn

## 🛡️ Sécurité

- **Clé API** : Ne jamais commiter votre clé API dans le code source
- **Fichiers PDF** : Assurez-vous que vos documents ne contiennent pas d'informations sensibles
- **Réseau** : L'application écoute sur `0.0.0.0:8000` - configurez un firewall si nécessaire

## 📚 Technologies utilisées

- **Backend** : FastAPI, LangChain, OpenAI
- **Frontend** : Vue.js 3, HTML/CSS
- **Base vectorielle** : FAISS
- **Traitement PDF** : PyPDF
- **Containerisation** : Docker
- **Embeddings** : OpenAI text-embedding-ada-002

## 🤝 Support

Pour obtenir de l'aide ou signaler des problèmes :
1. Vérifiez la section dépannage ci-dessus
2. Consultez les logs de l'application
3. Créez une issue sur le repository GitHub

## 📄 Licence

Ce projet est sous licence [MIT/GPL/autre] - voir le fichier LICENSE pour plus de détails. 