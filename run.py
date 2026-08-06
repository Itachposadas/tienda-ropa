from app import create_app

# Crea la aplicación usando la factoría
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)