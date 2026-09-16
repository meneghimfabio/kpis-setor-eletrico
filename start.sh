#!/bin/bash
echo "Iniciando Painel do Setor Elétrico Brasileiro..."

# Ativar e iniciar backend
cd backend
./venv/bin/python run.py &
BACKEND_PID=$!

# Iniciar frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
