from pyfiglet import Figlet

def print_logo(font):
    f = Figlet(font=font)
    logo = f.renderText('ESSL')
    print(logo, end='')