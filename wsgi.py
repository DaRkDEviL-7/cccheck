from main import main  # Assuming 'app' is your Telegram bot instance

if __name__ == '__main__':
    main.run()  # For local development

# For Gunicorn
application = main()