# 🧪 User-Agent-Checker

Um scanner rápido e multithread que testa diferentes `User-Agent`s contra uma URL e exibe o status HTTP e métricas da resposta.

Ideal para pentesters que precisam testar **bypass de WAF**, **exposição de `.git`**, ou comportamento de servidores baseado em `User-Agent`.

---

## 🚀 Funcionalidades

- Testa vários User-Agents simultaneamente (via `ThreadPoolExecutor`)
- Suporte a:
  - ✅ Proxy (`--proxy`)
  - ✅ Headers personalizados (`--header`)
  - ✅ Filtros avançados de exclusão (`--code`, `--lines`, `--words`, `--chars`)
- Script simples e direto em Python

---

## 🛠️ Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/user-agent-checker.py.git
cd user-agent-checker.py
pip install -r requirements.txt
```

---

## 📄 Uso

```bash
python3 user-agent-checker.py URL LIST [OPÇÕES]
```

**Parâmetros obrigatórios:**

- `URL` – A URL de destino a ser testada (ex: `https://example.com`)
- `LIST` – Caminho para o arquivo `.txt` com os User-Agents, um por linha

---

## ⚙️ Opções disponíveis

| Opção                  | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| `-t`, `--threads`      | Número de threads simultâneas (padrão: 10)                                |
| `--proxy`              | Define um proxy HTTP/S (ex: `http://127.0.0.1:8080`)                      |
| `--header`             | Header customizado (pode repetir várias vezes)                            |
| `--code`               | **Exclui** respostas com os status codes especificados (ex: `403,404`)    |
| `--lines`              | **Exclui** respostas com essas quantidades de linhas                      |
| `--words`              | **Exclui** respostas com essas quantidades de palavras                    |
| `--chars`              | **Exclui** respostas com essas quantidades de caracteres                  |

> ℹ️ Todos os filtros funcionam como exclusão: os valores passados são ignorados, e apenas os outros são exibidos.

---

## 💡 Exemplos

### ✅ Testar com 20 threads e proxy local:
```bash
python3 user-agent-checker.py https://example.com list.txt -t 20 --proxy http://127.0.0.1:8080
```

### ❌ Excluir respostas com status 403 ou 404:
```bash
python3 user-agent-checker.py https://example.com list.txt --code 403,404
```

### 🔍 Ignorar respostas com 0 ou 1 linha e até 10 caracteres:
```bash
python3 user-agent-checker.py https://example.com list.txt --lines 0,1 --chars 0,10
```

### 🧪 Usar headers customizados:
```bash
python3 user-agent-checker.py https://example.com list.txt \
  --header "X-Test: true" --header "Accept: */*"
```

---

## 🖥️ Exemplo de saída

```
=====================================================================
ID           Response   Lines    Word       Chars       Payload
=====================================================================
000000001:   200        12       26         198         "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
000000002:   403        6        13         110         "curl/7.68.0"
000000003:   302        5        10         85          "Wget/1.21.1"
```

> 💡 A coluna `Response` é colorida automaticamente de acordo com o status:
> - ✅ Verde: 2xx
> - ⚠️ Amarelo: 3xx
> - ❌ Vermelho: 4xx/5xx

---

## 📂 Estrutura esperada do `list.txt`

O arquivo deve conter um `User-Agent` por linha, por exemplo:

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64)
curl/7.68.0
Wget/1.21.1
```

---

## 📜 Licença

MIT License.  
Use com responsabilidade e apenas para fins legais (ex: pentest autorizado).

---

## 🤝 Contribuições

Contribuições são muito bem-vindas!  
Sinta-se à vontade para:

- Criar issues com ideias e bugs
- Abrir pull requests com melhorias, filtros, exportações, etc.

---

## 📦 requirements.txt

```text
requests
colorama
```
