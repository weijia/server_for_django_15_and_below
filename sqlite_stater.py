import logging
from starter import UfsStarterWithSqlite

log = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UfsStarterWithSqlite().start_ufs_sys()