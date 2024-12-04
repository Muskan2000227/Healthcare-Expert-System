echo "BUILD START"

# Create the static_build directory if it doesn't exist
mkdir -p staticfiles_build

# Install dependencies from the requirements.txt file
python3.12 -m pip install -r requirements.txt

# Run the collectstatic command to gather all static files into the staticfiles_build directory
python3.12 manage.py collectstatic --noinput --clear

# Optionally, move static files into the staticfiles_build directory if needed
mv static/* staticfiles_build/ || { echo "Error: Failed to move static files"; exit 1; }

echo "BUILD END"
