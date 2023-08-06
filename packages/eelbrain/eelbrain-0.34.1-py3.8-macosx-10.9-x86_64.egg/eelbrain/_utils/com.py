# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
"Internet communication utilities"
from distutils.version import LooseVersion
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import keyring
from keyring.errors import KeyringError
import smtplib
import socket
import sys
import traceback
import xmlrpc.client

from .system import user_activity
from .. import fmtxt
from . import ui


NOOB_DOMAIN = "Eelbrain"
NOOB_ADDRESS = 'n00b.eelbrain@gmail.com'


class KeychainError(Exception):
    "Error retrieving password from Keychain"


def check_for_update():
    """Check whether a new version of Eelbrain is available

    Prints a message if an update is available on the Python package index, does
    nothing otherwise.
    """
    current = sys.modules['eelbrain'].__version__
    if current == 'dev':
        print("Using Eelbrain development version")
        return
    pypi = xmlrpc.client.ServerProxy('https://pypi.python.org/pypi')
    versions = pypi.package_releases('eelbrain')
    newest = versions[-1]
    if LooseVersion(newest) > LooseVersion(current):
        print("New Eelbrain version available: %s (currently installed is %s)" %
              (newest, current))


def get_smtpserver(password, new_password=False):
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    while True:
        try:
            smtpserver.login(NOOB_ADDRESS, password)
            if new_password:
                keyring.set_password(NOOB_DOMAIN, NOOB_ADDRESS, password)
            return smtpserver
        except smtplib.SMTPAuthenticationError:
            password = ui.ask_str("Eelbrain notifier password invalid. Please enter valid password.", "Notifier Password")
            if password:
                new_password = True
            else:
                raise


class Notifier:
    """
    A notification email sender supporting ``with`` statements

    Parameters
    ----------
    to : str
        Email address of the recipient.
    name : str
        Name of the job (will be included in subject line).
    crash_info_func : None | callable
        Will be called upon crash to produce a string that will be included
        in the crash report.
    debug : bool
        If the task crashes, start pdb instead of exiting.

    Examples
    --------
    To receive a message after a task has been executed:

    >>> notifier = Notifier('me@somewhere.com')
    >>> with notifier:
    ...     do_task()
    ...

    """
    def __init__(self, to, name='job', crash_info_func=None, debug=True):
        # get the password
        try:
            password = keyring.get_password(NOOB_DOMAIN, NOOB_ADDRESS)
        except KeyringError as error:
            raise KeychainError(f"""{error}

Notifier password could not be retrieved from Keychain. Try the following:

 - Open the Keychain application
 - Search for an item with the name 'Eelbrain'
 - Open the information on this item (select it and press command-i, or use the
   menu command 'File'/'Get Info')
 - Select the 'Access Control' panel
 - Select 'Allow all applications to access this item'
 - Save changes, exit, and try again
 
If this does not solve the issue, delete the item and repeat.
""")
        if password is None:
            password = ui.ask_str("Please enter the Eelbrain notifier password.", "Notifier Password")
            # test it
            print("Validating password...")
            smtpserver = get_smtpserver(password, True)
            smtpserver.close()

        self.to = to
        self.name = name
        self.crash_info_func = crash_info_func
        self.debug = debug
        self._password = password

    def __enter__(self):
        print("Notification enabled for %s..." % self.name)
        user_activity.__enter__()
        return self

    def __exit__(self, type_, value, traceback_):
        host = socket.gethostname()
        user_activity.__exit__(type_, value, traceback_)
        if isinstance(value, Exception):
            error = type_.__name__
            temp = '{host} encountered {error}: {value} in {task}'
            event = temp.format(host=host, error=error, value=value,
                                task=self.name)
            info = []

            # traceback
            tb_items = traceback.format_tb(traceback_)
            error_message = "%s: %s\n" % (error, value)
            tb_items.append(error_message)
            tb_str = '\n'.join(tb_items)
            info.append(tb_str)

            # object info
            if self.crash_info_func:
                info.extend(self.crash_info_func())

            self.send(event, info)

            # drop into pdb
            if self.debug:
                traceback.print_exc()
                print('')
                try:
                    import ipdb as pdb
                except ImportError:
                    import pdb
                pdb.post_mortem(traceback_)
        else:
            event = '{host} finished {task}'.format(host=host, task=self.name)
            self.send(event)

    def send(self, subject, info=()):
        """Send an email message

        Parameters
        ----------
        subject : str
            Email subject line.
        info : str | list of str | FMText
            Email body; if a list, successive entries are joined with three
            line breaks.
        """
        if isinstance(info, fmtxt.FMTextElement):
            msg = MIMEMultipart('alternative')
            # multipart message - the last part is preferred
            part1 = MIMEText(str(info), 'plain')
            part2 = MIMEText(fmtxt.html(info), 'html')
            msg.attach(part1)
            msg.attach(part2)
        elif isinstance(info, str):
            msg = MIMEText(info)
        else:
            msg = MIMEText('\n\n'.join(map(str, info)))

        host = socket.gethostname()
        msg['Subject'] = subject
        msg['From'] = f'Eelbrain on {host} <{NOOB_ADDRESS}>'
        msg['To'] = self.to

        try:
            smtpserver = get_smtpserver(self._password)
            smtpserver.sendmail(NOOB_ADDRESS, self.to, msg.as_string())
            smtpserver.close()
        except Exception as error:
            print(f"Could not send email because an error occurred, skipping notification\n\n{error}s")


class NotNotifier:
    # Helper to raise proper error message when user has not set owner attribute
    def __enter__(self):
        raise AttributeError("The notifier is disabled because the .owner attribute was not set")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
