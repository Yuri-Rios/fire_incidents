# 🐍🚀 Dev Container: PySpark + Airflow

This project uses a Dev Container to automatically set up a development environment with **Apache Airflow**, **PySpark**, and full support in **VS Code**.

---

## ✅ Prerequisites

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

---

## 🚀 Getting Started

1. **Open the project in VS Code and click:**
   ```
   > Reopen in Container
   ```

2. **After build completes:**
   - The Airflow database will be initialized.
   - Both the `scheduler` and `webserver` will start automatically.
   - Access the Airflow UI at [http://localhost:8080](http://localhost:8080)

---

## ⚙️ Key Configuration

- DAG files should be placed in:
  ```
  fire_incidents/dags
  ```