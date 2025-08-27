# AI Web Scraper & Structured Parser

A lightweight **Selenium + BeautifulSoup** web scraper that fetches page HTML through a remote **Chromium** session (e.g., Bright Data SBR) and then **parses structured data with LangChain + Ollama**. The pipeline is optimized for long pages using DOM cleanup and chunked LLM parsing.

> Built for fast prototyping: point it at a URL, describe the fields you want, get clean structured text back.

---

## ✨ Features

- **Headless Chrome via remote WebDriver** (e.g., Bright Data SBR)
- **DOM extraction & cleanup** with BeautifulSoup (strips `<script>`/`<style>`, normalizes whitespace)
- **Chunking** for large pages (`max_length=6000` chars) to avoid token limits
- **LLM parsing with LangChain + Ollama** using a precise, “data-only” prompt
- Simple, readable code you can extend (`scrape.py`, `parse.py`, `main.py`)

---

## 🗂️ Project Structure

```
web-scraping/
├── ai/
│   └── (LLM helper modules, if any)
├── main.py
├── parse.py
├── scrape.py
├── requirements.txt
├── .env
└── chromedriver/   (if you use a local driver instead of remote)
```

Key modules:

- **`scrape.py`**
  - Connects to a **ChromiumRemoteConnection** using an SBR endpoint.
  - `scrape_website(url)` → returns raw HTML (`driver.page_source`).
  - `extract_text_from_html(html)` → extracts `<body>`.
  - `clean_body_content(body)` → removes noisy tags; returns newline-joined text.
  - `split_dom_content(dom, max_length=6000)` → yields text chunks.

- **`parse.py`**
  - `OllamaLLM` (model name configurable) + `ChatPromptTemplate`.
  - Prompt enforces **direct, data-only** responses with these guardrails:
    1) *Extract only what matches the description.*  
    2) *No extra commentary.*  
    3) *Empty string (`""`) if nothing matches.*  
    4) *Return only the requested data.*
  - `parse_with_ollama(dom_chunks, parse_description)` → concatenated parsed output.

- **`main.py`**
  - Orchestrates: scrape → clean → chunk → parse → print/save.

---

## 🚀 Quickstart

### 1) Prerequisites
- **Python 3.9+** (project was developed on 3.9)
- **Ollama** installed and running locally: <https://ollama.com/download>
- A running model in Ollama (you can change the name in `parse.py`):
  ```bash
  ollama pull <your-model>     # e.g., gemma:2b, llama3.1:8b, phi3:3.8b
  ```
- (Optional) **Remote Chromium / SBR** endpoint (e.g., Bright Data).

### 2) Install deps
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Configure environment
Create **.env** in the project root:
```bash
AUTH=brd-customer-<YOUR_KEY_HERE>
SBR_WEBDRIVER=https://$AUTH@brd.superproxy.io:9515
```

> If using another provider, set the Remote WebDriver URL accordingly.

### 4) Run
```bash
python main.py --url "https://example.com" \
               --parse "Extract the product name and price for each item."
```

**What happens:**  
1) Selenium navigates to the URL via remote Chromium and grabs the HTML.  
2) BeautifulSoup removes scripts/styles and normalizes text.  
3) Long pages are **chunked** to stay within model limits.  
4) Each chunk is sent to **Ollama** with your `--parse` description.  
5) Parsed pieces are concatenated and printed/saved.

---

## ⚙️ Configuration

- **Remote WebDriver**
  - In `scrape.py`, the connection looks like:
    ```python
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    Remote(sbr_connection, options=ChromeOptions())
    ```
  - Replace `SBR_WEBDRIVER` with your provider string or switch to a local `Service()`/`Chrome()` if preferred.

- **Chunk size**
  - `split_dom_content(..., max_length=6000)` controls chunking; tune for your model/context window.

- **Model**
  - In `parse.py` set `OllamaLLM(model="<your-model-name>")`. Smaller models are faster; larger ones are more accurate.

- **Prompt**
  - The template in `parse.py` is strict about **no extra text** and **empty string** when nothing matches. Tweak it for JSON or CSV outputs if needed (see Recipes below).

---

## 🧪 Examples

Extract job postings:
```bash
python main.py --url "https://company.com/careers" \
  --parse "For each listing, return 'role', 'location', and 'apply_link'."
```

Pull blog metadata:
```bash
python main.py --url "https://blog.example.com" \
  --parse "Return a list of posts with 'title', 'author', 'date'."
```

---

## 🧩 Recipes

- **JSON output**
  - Modify the prompt in `parse.py` to enforce JSON:
    ```text
    Return a valid JSON array. No comments or prose.
    ```
- **Rate limiting / retries**
  - Wrap `driver.get(url)` with simple backoff; add `time.sleep()` between chunk calls.
- **Saving results**
  - Send the final string to a file (e.g., `outputs/run-YYYYmmdd-HHMM.txt` or `.json`).

---

## 🛠️ Troubleshooting

- **Blank or partial output**
  - Increase chunk size or switch to a model with a larger context window.
  - Ensure your `--parse` description is specific and *data-typed* (e.g., “numbers only”).
- **WebDriver connection fails**
  - Verify `.env` values and network access to your SBR endpoint.
  - If using local Chrome, ensure `chromedriver` version matches your Chrome version.
- **Ollama not found**
  - Confirm `ollama serve` is running and the model is pulled. Try `curl http://localhost:11434/api/tags`.

---

## 🧱 Security & Ethics

Respect robots.txt, site terms, and rate limits. Do not scrape personal data or use this for prohibited purposes. This code is for educational and lawful usage only.

---

## 📄 License

MIT — do whatever you want, but without warranty. See `LICENSE` if included.

---

## 🙌 Contributing

Issues and PRs are welcome. If you improve parsing (e.g., JSON schema, multi-page navigation, or captcha handling), please share!
