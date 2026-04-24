# Cómo arrancar — Instrucciones paso a paso

**¡Hola José Felipe!** Este archivo te dice exactamente qué hacer en los primeros 90 minutos. El Plan de Acción completo está en el Word que te pasé aparte.

## Paso 1: Crear tu cuenta de Azure (15 min)

1. Ir a https://azure.microsoft.com/free/
2. Sign up con tu correo personal (NO el de Motivus, evita problemas de tenant)
3. Te pide tarjeta de crédito para validar identidad — NO te cobran si no cambias a pay-as-you-go
4. Confirmar por SMS
5. Cuando termines tendrás $200 USD de crédito para 30 días

## Paso 2: Subir este repo a tu GitHub (15 min)

1. Ir a https://github.com → Sign in
2. Click en "+" arriba a la derecha → "New repository"
3. Nombre: `walmart-ai-azure-demo`
4. Descripción: "Retail intelligence system on Azure — forecasting, clustering, and conversational agent"
5. Visibilidad: **Public** (importante — así tu director puede entrar sin invitación)
6. NO marcar "Add README" (ya tienes uno)
7. Click "Create repository"

Ahora desde tu laptop, abre una terminal en la carpeta donde descomprimiste este zip:

```bash
cd walmart-ai-azure-demo
git init
git add .
git commit -m "Initial commit: project skeleton"
git branch -M main
git remote add origin https://github.com/<TU-USUARIO>/walmart-ai-azure-demo.git
git push -u origin main
```

## Paso 3: Instalar Azure CLI (10 min)

**Windows** (PowerShell como administrador):
```powershell
winget install --exact --id Microsoft.AzureCLI
```

**Mac**:
```bash
brew install azure-cli
```

Verificar:
```bash
az --version
az login
```
Se abre un navegador y te pide login. Usa el mismo correo de Azure del Paso 1.

## Paso 4: Configurar el ambiente Python (15 min)

En la carpeta del repo:

```bash
# Crear ambiente virtual
python -m venv .venv

# Activar (Windows):
.venv\Scripts\activate

# Activar (Mac/Linux):
source .venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

Esto tarda 3-5 minutos. Mientras tanto...

## Paso 5: Descargar el dataset de Walmart (10 min)

1. Ir a https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data
2. Si no tienes cuenta Kaggle, regístrate (gratis, 2 min)
3. Click "Late Submission" para aceptar términos de la competencia (no vas a subir nada, solo necesitas aceptar)
4. Descargar los 3 archivos:
   - `train.csv`
   - `features.csv`
   - `stores.csv`
5. Copiarlos a la carpeta `data/raw/` del repo

## Paso 6: Configurar variables (5 min)

```bash
# Copiar el template
cp config/.env.example config/.env
```

Abrir `config/.env` con VS Code y llenar solo estos dos por ahora (los demás los llenas en el Día 1):

```
AZURE_SUBSCRIPTION_ID=<lo ves con el comando de abajo>
AZURE_TENANT_ID=<lo ves con el comando de abajo>
```

Obtener esos valores:
```bash
az account show
```

Copia el valor de `id` al AZURE_SUBSCRIPTION_ID, y el valor de `tenantId` al AZURE_TENANT_ID.

## Paso 7: Probar que todo funciona (15 min)

Desde la raíz del repo, con el `.venv` activado:

```bash
python -m src.ml.train_forecast
```

Si ves algo como:
```
📥 Cargando datos...
   Filas: 421,570
🔧 Feature engineering...
✂️  Split temporal...
🧠 Entrenando RandomForest...
📊 Evaluando...
   MAE:  $1,502.33
   RMSE: $3,045.87
   R²:   0.9634
💾 Modelo guardado en outputs/forecast_model.joblib
```

**¡Funcionó!** Ya tienes un modelo real entrenado. Celebra 30 segundos y sigue.

## Paso 8: Commit del Día 0

```bash
git add .
git commit -m "Day 0: environment setup + baseline model running locally"
git push
```

## Listo

Ya cumpliste el Día 0. Mañana viernes arrancas con el plan completo del Word. La primera hora va a ser crear el Azure ML Workspace ejecutando el script:

```bash
bash scripts/00_setup_infra.sh
```

---

## Si algo falla

**Error `az: command not found`** → reinstalar Azure CLI o reiniciar terminal

**Error `pip: command not found`** → activar el `.venv` primero

**Error `ModuleNotFoundError: src`** → ejecutar desde la raíz del repo, no desde `src/`

**Error con el dataset** → verificar que los 3 CSVs están en `data/raw/` (no en una subcarpeta)

**Cualquier otra cosa** → cópialo a Claude y te ayudo a resolverlo en minutos.

## Recordatorio importante

Apaga el Compute Instance de Azure al final de cada día. El Compute Cluster tiene auto-shutdown a los 5 min idle (ya está configurado en el script), pero los Compute Instances NO — tú los apagas manualmente en el Studio. **Un Compute Instance corriendo 24/7 te consume el crédito en 3 días.**
