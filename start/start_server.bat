set DICE_LOG_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
cd ../
python src/roller_app.py --mode server