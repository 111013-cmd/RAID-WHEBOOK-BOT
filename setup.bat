@echo off
REM Vérifier si Python est installé
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé ou n'est pas dans le PATH. Veuillez l'installer depuis https://www.python.org.
    pause
    exit /b
)

REM Créer un environnement virtuel (optionnel mais recommandé)
echo Création d'un environnement virtuel...
python -m venv venv

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installer les dépendances à partir du fichier requirements.txt
echo Installation des dépendances...
pip install -r requirements.txt

REM Informer l'utilisateur que l'installation est terminée
echo Installation terminée ! Vous pouvez maintenant exécuter le script Python.
pause
