from swagger_server import app, MODE

# define mode and port
PORT = 8080

if __name__ == "__main__":
    app.run(debug=MODE=='dev', port=PORT)

