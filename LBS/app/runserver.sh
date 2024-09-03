#!/bin/sh
python /app/app.py&

until curl -s http://localhost:5000/health | grep -q "ok"; do
    echo "Waiting for Flask app to be ready..."
    sleep 2
done

python /app/populate_db.py
wait