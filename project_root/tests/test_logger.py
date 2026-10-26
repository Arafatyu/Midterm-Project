from app.logger import Logger


def test_logger_writes_all_levels(tmp_path):
    log_file = tmp_path / "logs" / "test.log"
    logger = Logger(str(log_file))
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")

    text = log_file.read_text()
    assert "INFO - info message" in text
    assert "WARNING - warning message" in text
    assert "ERROR - error message" in text


def test_creating_logger_twice_does_not_repeat_messages(tmp_path):
    log_file = tmp_path / "test.log"
    Logger(str(log_file))
    logger = Logger(str(log_file))
    logger.info("only once")
    assert log_file.read_text().count("only once") == 1