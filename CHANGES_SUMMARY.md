# PDFhub - Resumo das Correções

## Problemas Corrigidos

### Backend (Flask + PyMuPDF + PyPDF2)

1. **PyPDF2 3.x - Rotação de páginas**
   - `page.rotate()` removido na v3.x
   - Corrigido para: `page.rotation = (page.rotation + rotation) % 360`

2. **Watermark - PyMuPDF**
   - `text_rect.tl + tuple` inválido → Usado `fitz.Point` e `insert_textbox`
   - Opacidade ignorada → Adicionados `fill_opacity` e `stroke_opacity`
   - Rotação não múltipla de 90 → Usado parâmetro `morph` com matriz de transformação

3. **Protect PDF - Permissões**
   - Dict não aceito pelo PyPDF2 → Convertido para bitmask (4=print, 8=modify, 16=copy, 32=annotate)

4. **Health check 404**
   - Adicionado `@conversion_bp.route('/api/health')`

5. **Cleanup excessivo**
   - Executava a cada request → Movido para thread periódica (1h)

6. **Paths de saída hardcoded**
   - Todos os métodos usavam `../output` relativo → Centralizado em `create_output_dir()` via `utils.file_handler`

7. **Upload de arquivos simultâneos**
   - `datetime.now()` causava colisão → Adicionado `uuid.uuid4().hex[:8]` no nome

8. **CORS**
   - Configurado `supports_credentials=True` e `origins: "*"`

### Frontend (Vue 3 + Vite + Tailwind)

1. **App.vue faltando**
   - Criado componente raiz completo com roteamento

2. **Tema escuro inconsistente**
   - Páginas FAQ, Terms, Privacy, Security reescritas com `bg-brand`, `text-white`, `bg-elevated`, `border-brand`

3. **Tailwind config**
   - Cores alinhadas com CSS custom properties (`--color-primary: #ff9f1c`)

4. **FileUploader validação**
   - Verificação de extensão primeiro, depois MIME com suporte a wildcards

5. **API URL dev/prod**
   - `VITE_API_URL || '/api'` para usar proxy Vite em dev

### Docker

1. **Multi-stage build**
   - Stage 1: Node 20 Alpine → build frontend
   - Stage 2: Python 3.13 slim → backend + static files
   - Copia `dist` para `./static` servido por Flask

## Testes Realizados

✅ Health check (`/api/health`)
✅ PDF → TXT
✅ PDF → DOCX
✅ PDF → XLSX
✅ PDF → PNG/JPG
✅ PDF → COMPRESS
✅ Merge PDFs
✅ Split PDF (all/range/every_n)
✅ Rotate PDF (90/180/270)
✅ Watermark (texto, opacidade, ângulo, cor)
✅ Protect PDF (senha, permissões)
✅ Imagem → PDF
✅ DOCX → PDF
✅ TXT → PDF
✅ Frontend servido via Flask (`/`)
✅ Assets servidos via Flask (`/assets/*`)
✅ Proxy Vite funcionando (`/api/*` → `localhost:5000`)

## Como Executar

### Desenvolvimento
```bash
# Backend
cd backend
python app.py  # porta 5000

# Frontend (outro terminal)
cd frontend
npm run dev    # porta 5173, proxy /api → 5000
```

### Produção (Docker)
```bash
docker build -t pdfhub .
docker run -p 5000:5000 pdfhub
# Acesse http://localhost:5000
```

### Build Frontend
```bash
cd frontend
npm run build  # gera ./dist
```
