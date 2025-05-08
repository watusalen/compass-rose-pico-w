# Rosa dos Ventos com Raspberry Pi Pico W

Este projeto mostra como usar o **Raspberry Pi Pico W** para ler um joystick analógico, enviar via HTTP para um servidor **Flask** em Python e exibir uma bússola interativa no navegador.

---

## 📦 Estrutura do Projeto

```
.
├── include/                  # Headers C do Pico SDK / LWIP / mbedTLS
│   ├── example_http_client_util.h
│   ├── lwipopts_examples_common.h
│   ├── lwipopts.h
│   ├── mbedtls_config_examples_common.h
│   └── mbedtls_config.h
│
├── src/                      # Código-fonte em C para o Pico W
│   ├── example_http_client_util.c
│   ├── picow_http_client.c
│   └── picow_http_verify.c
│
├── server/                   # Backend Flask + dashboard HTML/CSS/JS
│   ├── server.py
│   └── requirements.txt
│
├── CMakeLists.txt            # Script principal de build CMake
├── pico_sdk_import.cmake     # Import do Pico SDK
├── .gitignore                # Ignorar build artifacts, venv, etc.
└── README.md                 # Este arquivo
```

---

## 🛠️ Requisitos

### Hardware  
- **Raspberry Pi Pico W**  
- Joystick analógico com saídas VRx → GP26 (ADC0) e VRy → GP27 (ADC1)  
- Cabo micro-USB  

### Software  
- **Pico SDK** (v1.5.1 ou superior)  
- **CMake** (v3.13 ou superior)  
- **arm-none-eabi-gcc** toolchain  
- **Python 3.8+**  
- Pacotes Python:
  ```bash
  pip install flask flask-cors
  ```

---

## 🚀 Como Usar

### 1. Clonar o repositório  
```bash
git clone https://github.com/seu-usuario/rosa-dos-ventos-iot.git
cd rosa-dos-ventos-iot
```

### 2. Compilar o firmware  
```bash
mkdir build && cd build
cmake -DPICO_SDK_PATH=/caminho/para/pico-sdk ..
make
```
- Copie `picow_http_client.uf2` para o Pico W em modo BOOTSEL.

### 3. Configurar Wi-Fi  
No `CMakeLists.txt`, edite:  
```cmake
set(WIFI_SSID       "Seu_SSID")
set(WIFI_PASSWORD   "Sua_Senha")
set(HOST            "IP_do_servidor")  # Ex: 192.168.0.100
```
Recompile se necessário.

### 4. Iniciar o servidor Flask  
```bash
cd server
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
python server.py
```
O dashboard estará em → **http://localhost:5000**

### 5. Testar endpoint  
```bash
curl "http://localhost:5000/data?x=1000&y=3000"
# {"direction":"Sudeste","x":1000,"y":3000}
```

---

## 📡 Protocolo HTTP

O Pico W faz requisições GET no formato:
```
/data?x=<valor_adc_x>&y=<valor_adc_y>
```
O servidor armazena internamente os últimos valores e os serve ao frontend.

---
