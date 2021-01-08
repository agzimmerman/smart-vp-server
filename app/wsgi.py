from app.application import create_app

# from waitress import serve

app = create_app()

# Using waitress for production
#serve(app, )
app.run(debug=False, threaded=True,
        host='0.0.0.0', port=5000)

if __name__ == "main":
    pass
    #app.run(debug=True, threaded=False, host='0.0.0.0')


