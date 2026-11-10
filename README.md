# Iris Flower Classification

Follow these steps to run the project on Windows. The application uses an existing saved model to predict an Iris flower species from four measurements.

## 1. Clone the project or download the ZIP

Open **Command Prompt (CMD)** and clone the repository:

```cmd
git clone "https://github.com/ali-uol/MLDemoProject.git"
cd MLDemo
```

If Git is not installed, use the ZIP option instead:

1. Open the repository: https://github.com/ali-uol/MLDemoProject
2. Select **Code > Download ZIP**.
3. Right-click the downloaded ZIP and select **Extract All**.
4. Open the extracted folder containing `backend`, `frontend`, and `README.md`.

Do not run the project directly from inside the ZIP archive.

## 2. Open the project in VS Code

In VS Code, select **File > Open Folder** and choose the project folder containing both `backend` and `frontend`.

If you cloned using CMD and the `code` command is available, you can also run:

```cmd
code .
```

Open **Terminal > New Terminal**. Select **Command Prompt** from the terminal dropdown so the commands below work as written.

Your terminal must initially be in the **project root**, not inside `backend` or `frontend`. Check with:

```cmd
dir
```

You should see:

```text
MLDemo/
|-- backend/
|-- frontend/
|-- README.md
```

The extracted ZIP folder may be named `MLDemo-main`; that is fine. Use that folder as the project root.

## 3. Create and activate the virtual environment at the root

First check that Python is installed:

```cmd
python --version
```

Use Python 3.11 or newer; this project was tested with Python 3.13. If Python is not recognized, install it and select **Add Python to PATH**, then restart VS Code. If `py --version` works, you can use `py -m venv .venv` to create the environment.

From the project root, run these commands **one at a time**:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Wait for environment creation to finish before activating it. After activation, the terminal prompt should begin with `(.venv)`.

Your folder structure should now look like this:

```text
MLDemo/
|-- .venv/
|-- backend/
|-- frontend/
|-- README.md
```

Create `.venv` only once, at the project root. Activating it keeps it active when you change into `backend`.

In VS Code, press **Ctrl+Shift+P > Python: Select Interpreter** and select the project's root `.venv\Scripts\python.exe`. If it is not listed, use **Enter interpreter path** to browse to that file.

## 4. Install backend dependencies

In the same terminal, with `(.venv)` active:

```cmd
cd backend
pip install -r requirements.txt
```

Wait for installation to finish successfully. If `pip` is not recognized, use:

```cmd
python -m pip install -r requirements.txt
```

The backend expects these existing saved files:

```text
backend/models/iris_decision_tree.joblib
backend/models/model_metadata.json
```

If they are missing, then save the model using joblib library in models or export the fitted model pipeline and matching metadata from your training notebook. The application loads these files; it does not train a model when starting.

## 5. Run the backend

Still inside `backend`, run:

```cmd
uvicorn app.main:app --reload
```

If `uvicorn` is not recognized, check that the environment is active and dependencies installed, then try:

```cmd
python -m uvicorn app.main:app --reload
```

Wait until the terminal shows **Application startup complete**.

Open these URLs:

- **FastAPI documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/api/health

When the model is ready, the health check returns:

```json
{"status": "healthy", "model_loaded": true}
```

**Keep this backend terminal running.** Open a separate terminal for the frontend.

## 6. Check Node.js and npm

In VS Code, open a **second Command Prompt terminal** using the **+** button in the terminal panel.

Check whether Node.js and npm are installed:

```cmd
node --version
npm --version
```

If both commands show version numbers, check that Node.js is compatible. Use **Node.js 24.x** for this project's frontend and test tools.

If either command is not recognized, or you need to install the compatible version:

1. Visit **https://nodejs.org/en/download**.
2. Download and install Node.js 24.x for Windows, including npm.
3. Keep the installer option that adds Node.js to PATH enabled.
4. Close and reopen VS Code so the new PATH is available.
5. Run `node --version` and `npm --version` again.

If restarting VS Code stops the backend terminal, start the backend again using step 9 below.

The frontend does not need the Python virtual environment.

## 7. Install frontend dependencies and run it

In the second terminal, start from the **project root** and run:

```cmd
cd frontend
npm install
npm run dev
```

Run each command separately. Wait for `npm install` to finish successfully before running `npm run dev`. This installs Vite locally; you do not need a global Vite installation.

If the second terminal opens inside `backend`, first run `cd ..` to return to the project root, then run `cd frontend`.

## 8. Open and use the application

Open the frontend address printed by Vite:

**http://127.0.0.1:5173**

1. Enter the four flower measurements in centimeters.
2. Click **Predict**.
3. Read the predicted species below the form.

You can start with these example values:

| Input | Value (cm) |
| --- | --- |
| Sepal length | 5.1 |
| Sepal width | 3.5 |
| Petal length | 1.4 |
| Petal width | 0.2 |

Keep **both terminals running** while using the application:

| Terminal | Working folder | Running command |
| --- | --- | --- |
| Backend | `backend` | `uvicorn app.main:app --reload` |
| Frontend | `frontend` | `npm run dev` |

## 9. Stop the project or run it again later

Press **Ctrl+C** in each terminal to stop the servers. If CMD asks `Terminate batch job (Y/N)?`, type `Y` and press Enter.

You do not need to recreate `.venv` or reinstall dependencies every time.

For future runs, open two CMD terminals at the **project root**.

**Terminal 1 - backend:**

```cmd
.venv\Scripts\activate.bat
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 - frontend:**

```cmd
cd frontend
npm run dev
```

If you need to open the project folder manually, use its actual location. For example:

```cmd
cd /d D:\MLDemo
```

Replace `D:\MLDemo` with your cloned or extracted folder path. The optional sections below use this example path too.

Repeat dependency installation after pulling changes to requirement or package files. Restart the backend after replacing the saved model.

After stopping the backend, you can leave its Python environment with:

```cmd
deactivate
```

## Optional: run the prediction notebook

Install notebook and development dependencies from the project root:

```cmd
cd /d D:\MLDemo
.venv\Scripts\activate.bat
cd backend
python -m pip install -r requirements-dev.txt
```

In VS Code:

1. Open the entire `MLDemo` folder.
2. Install the Python and Jupyter extensions if needed.
3. Use **Ctrl+Shift+P > Python: Select Interpreter > Enter interpreter path** and choose `D:\MLDemo\.venv\Scripts\python.exe` (adjust the path for your clone).
4. Open `backend/notebooks/model_prediction.ipynb`.
5. Use **Select Kernel** to choose that same root virtual environment.
6. Select **Run All**.

The notebook loads the saved model, predicts one sample, and checks that FastAPI returns the same result. Its TestClient check does not require a running backend server. It does not retrain the model.

For students training their own models: select the best fitted model using validation or cross-validation, save the full pipeline into `backend/models/iris_decision_tree.joblib`, and save matching `model_metadata.json`. The application loads these files for prediction.

## Optional: tests and frontend build

After installing `requirements-dev.txt`, run the saved-model API tests:

```cmd
cd /d D:\MLDemo
.venv\Scripts\activate.bat
cd backend
python -m pytest tests/test_saved_model.py -q
```

Frontend tests and production build:

```cmd
cd /d D:\MLDemo\frontend
npm test
npm run build
```

The existing training and EDA files are preserved but are not needed to start this application. `requirements-training.txt` contains optional training dependencies; the full ML test suite trains temporary models.

## Common problems

| Problem | What to do |
| --- | --- |
| `python`, `node`, or `npm` is not recognized | Install the corresponding software, reopen CMD, and repeat the version checks in step 1. |
| `.venv\Scripts\activate.bat` cannot be found | Go to the project root and create the environment there with `python -m venv .venv`. |
| `requirements.txt` cannot be found | Run `cd backend` from the project root before installing backend packages. |
| `uvicorn` is not recognized | Activate the root environment and install backend requirements. Then use `python -m uvicorn app.main:app --reload`. |
| `No module named app` | Run Uvicorn from the `backend` folder. |
| `'vite' is not recognized` | Run `npm install` from `frontend`, wait for success, then run `npm run dev`. If development dependencies were omitted, run `npm install --include=dev`. |
| `npm.ps1 cannot be loaded` | These instructions use CMD. Switch your terminal to Command Prompt, or use `npm.cmd` in PowerShell. |
| Port 8000 or 5173 is already in use, or WinError 10013 occurs | Stop any earlier server you started on that port with Ctrl+C, then retry. If it persists, check Windows port restrictions or ask your instructor; do not stop unrelated processes. |
| Frontend says it cannot reach the backend | Keep the backend terminal running and check http://127.0.0.1:8000/api/health. |
| Health check returns 503 / model unavailable | Check both saved model files in `backend/models/`, inspect the backend terminal error, and restart after correcting the files. |
| `/docs` is not showing | Start the backend and open port **8000** with `/docs`; port 5173 serves the frontend. |
| VS Code uses an old backend environment | Select the root `.venv\Scripts\python.exe` interpreter and the same notebook kernel. |

## Configuration and main files

Default local settings work without creating `.env` files. Existing `.env.example` files describe optional changes:

- Frontend `VITE_API_BASE_URL` defaults to `http://localhost:8000`.
- Backend `CORS_ORIGINS` allows the local frontend origins.
- Backend `IRIS_ARTIFACT_DIR` optionally changes the saved-artifact location; relative paths resolve from `backend`.

Restart the relevant server after changing configuration. The backend loads the model once at startup and never trains during a prediction request.

| File | Purpose |
| --- | --- |
| `backend/app/main.py` | FastAPI application and startup |
| `backend/app/api/routes.py` | API endpoints |
| `backend/app/schemas/prediction.py` | Input validation |
| `backend/app/services/prediction_service.py` | Load the model and predict |
| `backend/notebooks/model_prediction.ipynb` | Saved-model prediction example |
| `frontend/src/components/PredictionForm.jsx` | Measurement inputs |
| `frontend/src/components/PredictionResult.jsx` | Prediction output |
| `frontend/src/services/api.js` | Requests to FastAPI |
