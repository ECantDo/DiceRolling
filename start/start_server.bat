set DICE_LOG_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
cd ../
python -m src.roller_app --mode server