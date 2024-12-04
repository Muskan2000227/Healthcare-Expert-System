

echo "Running collectstatic to gather static files..."
python3.12 manage.py collectstatic --noinput || exit 1

echo "Creating the staticfiles_build directory..."
mkdir -p staticfiles_build || exit 1

echo "Build process completed successfully."
