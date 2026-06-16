# Contributing to AI Receptionist Enterprise

## Development Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Code Style
- Python: Black + Ruff
- TypeScript: ESLint + Prettier

## Testing
```bash
cd backend
pytest tests/ --cov=app --cov-report=xml

cd frontend
npm test -- --coverage
```

## Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request
