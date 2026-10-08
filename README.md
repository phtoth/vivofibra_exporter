# Vivo Fibra Prometheus Exporter

## Version / Versão
- Current version / Versão atual: 1.0

## Author / Autor
- Created by / Criado por: Pedro Toth
- GitHub: https://github.com/phtoth
- Email: pedrototh@gmail.com

## English

### Purpose
This project is a lightweight Prometheus exporter for Vivo Fibra modems that expose a local web interface. It connects to the modem, authenticates using the modem's login mechanism, reads the status page, extracts the key GPON and PPP values, and exposes them in Prometheus format for scraping.

### Objetivo
Este projeto é um exporter leve para Prometheus, voltado para modems Vivo Fibra que expõem uma interface web local. Ele se conecta ao modem, autentica usando o mecanismo de login do equipamento, lê a página de status, extrai os principais valores de GPON e PPP e os expõe em formato Prometheus para coleta.

The exporter was designed to monitor metrics such as:

- GPON link state
- GPON RX optical power
- GPON TX optical power
- PPP connection state
- exporter scrape success status
- last successful collection timestamp

O exporter foi pensado para monitorar métricas como:

- estado do link GPON
- potência óptica RX do GPON
- potência óptica TX do GPON
- estado da conexão PPP
- status de sucesso da coleta do exporter
- timestamp da última coleta bem-sucedida

It is especially useful for environments using Prometheus + Grafana to monitor Internet connectivity and fiber link health.

Ele é especialmente útil em ambientes que usam Prometheus + Grafana para monitorar conectividade de Internet e saúde do link de fibra.

### Supported use case
This exporter is intended for modems that expose a status page similar to the Vivo Fibra device interface and require login before status is accessible.

### Caso de uso suportado
Este exporter foi desenvolvido para modems que expõem uma página de status semelhante à interface local da Vivo Fibra e exigem login antes que o status fique disponível.

### Manual execution
1. Open a terminal in the project directory.
2. Make sure Python 3 is installed.
3. Set the required environment variables before running the exporter.

### Execução manual
1. Abra um terminal no diretório do projeto.
2. Verifique se o Python 3 está instalado.
3. Defina as variáveis de ambiente necessárias antes de iniciar o exporter.

Example:

Exemplo:

```bash
export VIVO_MODEM_URL="http://192.168.15.1"
export VIVO_USERNAME="admin"
export VIVO_PASSWORD="your-password"
export EXPORTER_PORT="9108"
export POLL_INTERVAL="60"
```

4. Start the exporter:

```bash
python3 vivofibra_exporter.py
```

4. Inicie o exporter:

```bash
python3 vivofibra_exporter.py
```

5. The exporter will perform an initial collection and then expose the metrics at:

5. O exporter fará uma coleta inicial e, em seguida, vai expor as métricas em:

```text
http://0.0.0.0:9108/metrics
```

6. Prometheus can scrape the endpoint using a job similar to:

```yaml
scrape_configs:
  - job_name: 'vivo-fibra-exporter'
    static_configs:
      - targets: ['localhost:9108']
```

6. O Prometheus pode coletar esse endpoint com uma configuração parecida com:

```yaml
scrape_configs:
  - job_name: 'vivo-fibra-exporter'
    static_configs:
      - targets: ['localhost:9108']
```

### Docker build
To build the project as a Docker image and keep it locally on your machine:

### Build com Docker
Para compilar o projeto como imagem Docker e manter a imagem localmente no seu computador:

```bash
docker build -t vivofibra-exporter .
```

This command creates a local image named `vivofibra-exporter` that remains available on your machine until you remove it.

Esse comando cria uma imagem local chamada `vivofibra-exporter` que fica disponível no seu ambiente até que você a remova.

To run it in a container:

Para executar em um container:

```bash
docker run --rm -p 9108:9108 \
  -e VIVO_MODEM_URL=http://192.168.15.1 \
  -e VIVO_USERNAME=admin \
  -e VIVO_PASSWORD=sua-senha \
  -e EXPORTER_PORT=9108 \
  -e POLL_INTERVAL=60 \
  vivofibra-exporter
```

### Notes
- The modem password must be set in the `VIVO_PASSWORD` environment variable.
- Temporary HTML debug files are created in the project directory while the exporter is running.
- These files are cleaned up automatically when the program exits.

### Observações
- A senha do modem deve ser informada na variável de ambiente `VIVO_PASSWORD`.
- Arquivos temporários em HTML de diagnóstico são criados no diretório do projeto enquanto o exporter está em execução.
- Esses arquivos são removidos automaticamente ao encerrar o programa.

---

## Português (Brasil)

### Objetivo
Este projeto é um exporter leve para Prometheus, usado com modems Vivo Fibra que expõem uma interface web local. Ele se conecta ao modem, autentica usando o mecanismo de login do equipamento, lê a página de status, extrai os principais valores de GPON e PPP e os expõe em formato Prometheus para coleta.

O exporter foi pensado para monitorar métricas como:

- estado do link GPON
- potência óptica RX do GPON
- potência óptica TX do GPON
- estado da conexão PPP
- status de sucesso da coleta do exporter
- timestamp da última coleta bem-sucedida

Ele é especialmente útil em ambientes que usam Prometheus + Grafana para monitorar conectividade de Internet e saúde do link de fibra.

### Caso de uso suportado
Este exporter foi desenvolvido para modems que expõem uma página de status semelhante à interface local da Vivo Fibra e exigem login antes que o status fique disponível.

### Execução manual
1. Abra um terminal no diretório do projeto.
2. Verifique se o Python 3 está instalado.
3. Defina as variáveis de ambiente necessárias antes de iniciar o exporter.

Exemplo:

```bash
export VIVO_MODEM_URL="http://192.168.15.1"
export VIVO_USERNAME="admin"
export VIVO_PASSWORD="sua-senha"
export EXPORTER_PORT="9108"
export POLL_INTERVAL="60"
```

4. Inicie o exporter:

```bash
python3 vivofibra_exporter.py
```

5. O exporter fará uma coleta inicial e, em seguida, vai expor as métricas em:

```text
http://0.0.0.0:9108/metrics
```

6. O Prometheus pode coletar esse endpoint com uma configuração parecida com:

```yaml
scrape_configs:
  - job_name: 'vivo-fibra-exporter'
    static_configs:
      - targets: ['localhost:9108']
```

### Build com Docker
Para compilar o projeto como imagem Docker e manter a imagem localmente no seu computador:

```bash
docker build -t vivofibra-exporter .
```

Esse comando cria uma imagem local chamada `vivofibra-exporter` que fica disponível no seu ambiente até que você a remova.

Para executar em um container:

```bash
docker run --rm -p 9108:9108 \
  -e VIVO_MODEM_URL=http://192.168.15.1 \
  -e VIVO_USERNAME=admin \
  -e VIVO_PASSWORD=sua-senha \
  -e EXPORTER_PORT=9108 \
  -e POLL_INTERVAL=60 \
  vivofibra-exporter
```

### Observações
- A senha do modem deve ser informada na variável de ambiente `VIVO_PASSWORD`.
- Arquivos temporários em HTML de diagnóstico são criados no diretório do projeto enquanto o exporter está em execução.
- Esses arquivos são removidos automaticamente ao encerrar o programa.

---

## Tested modem / Modem testado

- Manufacturer / Fabricante: MitraStar Technology Corp
- Model / Modelo: GPT-2742GX4X5v6

English:
This exporter was tested on the MitraStar Technology Corp modem model GPT-2742GX4X5v6.

Português (Brasil):
Este exporter foi testado no modem MitraStar Technology Corp, modelo GPT-2742GX4X5v6.
