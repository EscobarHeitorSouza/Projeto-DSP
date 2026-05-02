#!/bin/sh

# O shell irá encerrar a execução do script se um comando retornar um status de saída diferente de zero.
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Aguardando o banco de dados PostgreSQL em $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 2
done

echo "Banco de dados PostgreSQL está disponível. Iniciando a aplicação..."

python manage.py collectstatic --noinput 
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000