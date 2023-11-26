import click
import logging
from tqdm import tqdm
from mega import Mega
from mega.errors import RequestError
import datetime
import os
from reports import main as generate_report
from .parser import Parser
from .user import User

# Define the AccountFilter class
class AccountFilter(logging.Filter):
    def filter(self, record):
        return 'Account' in record.getMessage()

# Define directories for logs
log_dir = 'logs/raw'
report_dir = 'logs/reports'

# Create directories if they don't exist
os.makedirs(log_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)

# Generate a current date-time string for the log filename
current_time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"{log_dir}/megakeep_{current_time_str}.log"

# Set up logging
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(message)s')
logging.getLogger('mega').setLevel(logging.WARNING)

# Create and add the filter to the logger
logger = logging.getLogger()
account_filter = AccountFilter()
logger.addFilter(account_filter)

mega = Mega()

@click.command()
@click.option(
    "--file",
    "-f",
    default="mega.txt",
    help="""
              Location of file which contains users and passwords of Mega. Default: mega.txt\n
              File should be formatted in form of [email][spaces/tabs][password].\n
              File may contain multiple accounts separated in ne line.\n
              Supports comment and empty lines (# or //).\n 
              i.e:\n
              bla@secure.com   mypassword\b\n
              mega@secure.com  securedpassword""",
)
@click.option(
    "--skip-fails",
    "-s",
    default=False,
    is_flag=True,
    type=bool,
    help="Don't exit upon failed accounts (wrong credentials, blocked user etc')",
)
def main(file: str, skip_fails: bool) -> None:
    try:
        users = Parser.parse_file(file)
    except Exception as e:
        print(str(e))
        raise click.Abort()

    users_progress_bar = tqdm(users)

    for user in users_progress_bar:
        try:
            users_progress_bar.set_description(f"Processing user {user.email}")
            login_user(user)
        except RuntimeError:
            if not skip_fails:
                raise click.Abort()

    print(f"Done! Generating report...")

    # Call the main function of reports.py
    generate_report()
    
def login_user(user: User) -> None:
    try:
        logged_user = mega.login(user.email, user.password)
        quota = logged_user.get_quota()
        space = logged_user.get_storage_space(mega=True)

        logging.info(f"Account {user.email} touched. Quota: {quota}, Space used: {space} MB")
    except RequestError as e:
        if e.code == -9:
            print(f"{user.email}: wrong email or password")
        elif e.code == -16:
            print(f"{user.email} is blocked")
        else:
            print(f"{user.email}: unknown exception in Mega.")
        raise RuntimeError(e)

if __name__ == '__main__':
    main()