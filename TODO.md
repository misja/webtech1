# TODO - Webtechnologie 1 Documentatie

## Documentatie Issues

### 🔴 Ontbrekende Screenshot: product_123.png (Week 4)

**Prioriteit**: Medium
**Status**: Open
**Aangemaakt**: 2026-02-17

**Probleem**:
MkDocs build waarschuwing:
```
WARNING - Doc file 'week4/flask-deel3.md' contains a link 'imgs/product_123.png',
but the target 'week4/imgs/product_123.png' is not found among documentation files.
```

**Locatie**:
- **Bestand**: `docs/week4/flask-deel3.md` (regel 210)
- **Context**: Sectie over URL parameters met `<int:variabele>`
- **Doel**: Screenshot van browser URL met int parameter

**Acties**:
1. Flask app starten met route `/product/<int:product_id>`
2. Navigeer naar `http://localhost:5000/product/123`
3. Screenshot maken van URL in browser (moet `/product/123` tonen)
4. Screenshot opslaan als `docs/week4/imgs/product_123.png`
5. Verifiëren dat `mkdocs build` zonder warning werkt

---

## Voltooide Items

### ✅ Link fix: projecten directory (Week 5)
**Opgelost**: 2026-02-17
Link gefixt van `../projecten/` naar `../projecten/index.md` in `flask-forms-deel1.md`.
