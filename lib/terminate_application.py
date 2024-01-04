from sys import exit


def signal_handler(interrupt_signal, frame) -> None:
    """
    Signal handler to exit the application
    :param interrupt_signal: interrupt signal
    :param frame: input frame
    :return: None
    """
    print(f'Terminating the program. {interrupt_signal} {frame}')
    exit(0)
