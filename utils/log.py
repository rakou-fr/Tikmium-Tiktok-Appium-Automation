def log_in_json(message):
    with open('log.txt', 'a', encoding="utf-8") as log_file:
        log_file.write(message + '\n')