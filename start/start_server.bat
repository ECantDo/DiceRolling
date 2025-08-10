set DICE_LOG_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
cd ../
python roller_app.py --mode server