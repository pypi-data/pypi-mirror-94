# coding: utf-8

from __future__ import division
import os
import re
import logging
import logging.handlers
import shutil
import shlex
import spur
import random
import datetime
import base64
import tarfile
import paramiko
import csv
from six import string_types, binary_type
import binascii
from string import digits, ascii_letters  # pylint: disable=deprecated-module
from deployv.helpers import container, json_helper
from deployv.helpers.decompress_helper import DecompressHelper
from deployv import base
import deployv_static
from jinja2 import Environment, FileSystemLoader
from errno import EEXIST
from deepdiff import DeepDiff
from stat import S_IREAD, S_IWRITE
import socket
import fcntl
import struct
import ipaddress

_AVAILABLES = {
    "production": ['update_production', 'post_process', 'restart_instance',
                   'restart_container', 'reload_config'],
    "test": [],
    "updates": [],
    "develop": [],
}

IMPLEMENTED_MSG_ERROR = ('The class you are instantiating does '
                         'not have this method implemented')

# pylint: disable=C0103
logger = logging.getLogger(__name__)


def copy_list_dicts(lines):
    res = []
    for line in lines:
        dict_t = {}
        for keys in line.keys():
            dict_t.update({keys: line[keys]})
        res.append(dict_t.copy())
    return res


def setup_deployv_logger(name='deployv', level=logging.DEBUG, log_file=None):
    """Configures a logger, setting the level and a stream handler by default.
    If a log file name is passed, a file handler is also created.

    By default it configures the 'deployv' logger, so the config applies
    automatically to every other logger that belongs to a submodule.
    (For example: 'deployv.commands.deployvcmd')

    Important note: To avoid multiple configurations or overriding other loggers,
    the loggers should be called using 'logging.getLogger(__name__)', so the
    logger is named like the file where is being used. This also facilitates that
    every logger inside the 'deployv' module gets the correct parent settings.

    This function returns the configured logger, but it should be used to
    configure the parent logger ('deployv') and only use a child logger from
    another module.
    """
    dv_logger = logging.getLogger(name)
    dv_logger.propagate = False
    dv_logger.setLevel(level)
    dv_logger.handlers = []
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)-5s - "
                                      "%(name)s.%(module)s.%(funcName)s - "
                                      "%(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    dv_logger.addHandler(stream_handler)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        dv_logger.addHandler(file_handler)
    return dv_logger


def is_iterable(obj):
    """ Method that verifies if an object is iterable and not a string, example:

    .. doctest::

        >>> from deployv.helpers import utils
        >>> utils.is_iterable(1)
        False
        >>> utils.is_iterable([1, 2, 3])
        True

    :param obj: Any object that will be tested if is iterable
    :return: True or False if the object can be iterated
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, string_types + (binary_type,))


def load_default_config():
    """ Loads the default configuration file.

    :return: Dictionary with the default configuration
    """
    default_config_path = deployv_static.get_template_path('default_config.json')
    default_config = json_helper.load_json(default_config_path)
    return default_config


def merge_config(config_file, keys_file=False, branches=False):
    """Merges keys_file and branches into config_file and returns a single json
        if no keys_file or branches is given just loads the config file

    :param config_file: Config file in json format
    :param keys_file: Param with the key file name and full path to it
    :param branches: Branches file to be used
    :return: Dict with complete json configuration after saving it into the config_file file
    """
    json_config = json_helper.load_json(config_file)
    if not isinstance(json_config, dict):
        return
    default_config = load_default_config()
    new_config = merge_dicts(default_config, json_config)
    changed = False
    if branches:
        json_branches = json_helper.load_json(branches)
        new_config.get("instance").update({"repositories": json_branches})
        changed = True
    if keys_file:
        encoded_key = generate_attachment(keys_file)
        new_config.get("instance").update({"ssh_key": encoded_key})
        changed = True
    if changed:
        json_helper.save_json(new_config, config_file)
    return new_config


def list_backups(file_dir, prefix):
    """List all files which start with prefix and sort
        them by date

    :param file_dir: Directory where backups are stored
    :param prefix: Prefix files to seek
    :return: sorted list
    """
    items = []
    for each in os.listdir(file_dir):
        if (prefix in each) and os.path.isfile(os.path.join(file_dir, each)):
            items.append(str(each))
    items.sort(reverse=True)
    return items


def clean_files(files):
    """Remove unnecessary and temporary files.

    :param files: A list or a str of absolute or relative paths thar will be erased
    """
    if not files:
        return
    items = files if is_iterable(files) else [files]
    for item in items:
        fname = item[0] if is_iterable(item) else item
        if fname != "/":
            logger.info('Removing %s', fname)
            if os.path.isfile(fname):
                os.remove(fname)
            elif os.path.isdir(fname):
                shutil.rmtree(fname)
        else:
            logger.error(
                "Invalid target path: '/'. Are you trying to delete your root path?")


def resume_log(log_lines):
    """Gets the log lines from -u (modules or all) and parse them to get the totals
        according to the filters dict

    :param log_lines: each element of the list is a log line
    :return: dict with key filters as keys and a list with all matched lines
    """
    def critical(line):
        criteria = re.compile(r'.*\d\sCRITICAL\s.*')
        return criteria.match(line)

    def errors(line):
        criteria = re.compile(r'.*\d\sERROR\s.*')
        return criteria.match(line)

    def warnings_trans(line):
        criteria = re.compile(
            r'.*\d\sWARNING\s.*no translation for language.*')
        return criteria.match(line)

    def import_errors(line):
        criteria = re.compile(r'^ImportError.*')
        return criteria.match(line)

    def warnings(line):
        criteria = re.compile(r'.*\d\sWARNING\s.*')
        return criteria.match(line) and 'no translation for language' not in line

    filters = {
        'critical': critical,
        'errors': errors,
        'warnings': warnings,
        'warnings_trans': warnings_trans,
        'import_errors': import_errors
    }
    res = {name: [] for name in filters}
    for line in log_lines:
        stripped_line = line.strip()
        for name, criteria in filters.items():
            if criteria(stripped_line):
                res.get(name).append(stripped_line)
                break

    return res


def get_strtime():
    """ Returns time stamp formatted as follows::

        %Y%m%d_%H%M%S

        So all backups and files that require this in the name will have the same format,
        if changes will be in one place, here.

    :return: Formatted timestamp
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def get_decompress_object(file_name):
    """ Returns an object to extract file_name*, only tar.gz and tar.bz2 are supported now:

    .. doctest::

        >>> from deployv.helpers import utils
        >>> utils.get_decompress_object('filename.tar.bz2')
        (<bound method TarFile.open of <class 'tarfile.TarFile'>>, 'r:bz2')

    Or if you pass a tar.gz file:

    .. doctest::

        >>> from deployv.helpers import utils
        >>> utils.get_decompress_object('filename.tar.gz')
        (<bound method TarFile.open of <class 'tarfile.TarFile'>>, 'r:gz')

    :param file_name: File name to be extracted
    :return: Tuple with the object and mode
    """
    if file_name.endswith('tar.gz'):
        fobject, modestr = tarfile.open, 'r:gz'
    elif file_name.endswith('tar.bz2'):
        fobject, modestr = tarfile.open, 'r:bz2'
    elif file_name.endswith('tar'):
        fobject, modestr = tarfile.open, 'r:'
    else:
        raise RuntimeError('Unknown file format "{}"'.format(file_name))
    return fobject, modestr


def decompress_files(name, dest_folder):
    """ Decompress a file, set of files or a folder compressed in tar.bz2 format

    :param name: Compressed file name (full or relative path)
    :param dest_folder: Folder where the decompressed files will be extracted
    :return: The absolute path to decompressed folder or file
    """
    assert os.path.exists(name)
    logger.debug("Decompressing file: %s", name)
    if os.path.isdir(name):
        return name
    logger.debug('Extracting %s into %s', name, dest_folder)
    fobject = DecompressHelper(name)
    try:
        fobject.extractall(dest_folder)
    except (EOFError, IOError) as error:
        logger.exception('Error uncompressing file %s', get_error_message(error))
        raise
    name_list = fobject.name_list()
    base_folder = dest_folder
    for fname in name_list:
        if (os.path.basename(fname) in
           ['dump.sql', 'database_dump.b64', 'database_dump.sql', 'database_dump']):
            base_folder = os.path.dirname(fname)
            break

    logger.debug("Destination folder: %s", dest_folder)
    logger.debug("Bakcup folder: %s", base_folder)
    if name.endswith(DecompressHelper.valid_extensions):
        fname = os.path.basename(name)
        dest_folder = os.path.join(dest_folder, base_folder)
    logger.debug("Destination folder: %s", dest_folder)
    return dest_folder


def odoo2postgres(odoo_config):
    """ This is a helper to convert from a odoo configuration dict to a postgres configuration dict
    using libpq
    format: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS,
    and also can map env vars gotten from a container

    :param odoo_config: Odoo database configuration
    :return: Dict with psql configuration
    """
    mapping = {
        'user': ['db_user', 'DB_USER'],
        'host': ['db_host', 'DB_HOST'],
        'port': ['db_port', 'DB_PORT'],
        'password': ['db_password', 'DB_PASSWORD'],
        'dbname': ['db_name', 'DB_NAME']
    }
    res = {}
    for psql_key, psql_value in mapping.items():
        for odoo_key, odoo_value in odoo_config.items():
            if odoo_key in psql_value:
                res.update({psql_key: odoo_value})
    return res


def generate_dbname(config, backup_name=False, prefix=False):
    """ Generates a database name for a test/dev instance based on the container name and
    backup used for the restoration. The created name will have the same timestamp that the one
    used, but if no backup name is supplied or the backup does not have a timestamp in the name
    the actual date will be used

    :param config: Instance configuration object
    :param backup_name: Optional backup name to be restored
    :return:
    """
    if not prefix:
        prefix = container.generate_prefix(config)
    if backup_name:
        name = re.search(r"_(\d{8}_\d{6})", backup_name)
        if name:
            name = name.group(1)
        else:
            name = get_strtime()
    else:
        name = get_strtime()
    res = '{prefix}_{date}'.format(prefix=prefix, date=name)
    return res


def generate_backup_name(database_name, reason=False, prefix=False):
    """Generates the backup name according to the following standard:
       database_name_reason_YYYYmmdd_HHMMSS
       If reason is none:
       database_name_YYYYmmdd_HHMMSS
    """
    if reason and not prefix:
        res = '%s_%s_%s' % \
            (database_name, reason, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    elif prefix and not reason:
        res = '%s_%s' % \
            (prefix, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    elif prefix and reason:
        res = '%s_%s_%s' % \
            (prefix, reason, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    else:
        res = '%s_%s' % (
            database_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    return res


def decode_b64_file(src, dst):
    """ Read src base64 encoded file and output its content to dst file
    :param src: Source file to read
    :param dst: Destination file
    """
    with open(src, 'r') as source_file:
        with open(dst, 'w') as destination_file:
            for line in source_file:
                destination_file.write(decode(base64.b64decode(line)))


def compress_files(name, files, dest_folder=None, cformat='bz2'):
    """ Compress a file, set of files or a folder in the specified cforma

    :param name: Desired file name w/o extension
    :param files: A list with the absolute o relative path to the files
                      that will be added to the compressed file
    :param dest_folder: The folder where will be stored the compressed file
    :param cformat: Desired format for compression, only supported bz2 and gz
    """
    if not dest_folder:
        dest_folder = '.'
    if cformat not in ['bz2', 'gz', 'tar']:
        raise RuntimeError('Unknown file format "{}"'.format(cformat))
    ext = ''
    if cformat == 'gz':
        fobject, modestr = tarfile.open, 'w:gz'
        ext = 'tar.gz'
    elif cformat == 'tar':
        fobject, modestr = tarfile.open, 'w:'
        ext = 'tar'
    elif cformat == 'bz2':
        fobject, modestr = tarfile.open, 'w:bz2'
        ext = 'tar.bz2'
    logger.debug("Generating compressed file: %s in %s folder",
                 name, dest_folder)

    bkp_name = '{0}.{1}'.format(name, ext)
    full_tmp_name = os.path.join(
        dest_folder,
        '._{}'.format(bkp_name)
    )
    full_name = os.path.join(dest_folder, bkp_name)

    with fobject(full_tmp_name, mode=modestr) as tar_file:
        for fname in files:
            if is_iterable(fname):
                tar_file.add(fname[0], os.path.join(name, fname[1]))
            else:
                basename = os.path.basename(fname)
                tar_file.add(fname, os.path.join(name, basename))
    shutil.move(full_tmp_name, full_name)
    return full_name


def generate_attachment(file_name):
    """ Helper that generates a file with base 64 encoded content
    to be used as an attachment in the messages returned by deployv

    :param file_name: Full path and name of the file to be attached
    :return: File content in b64 format
    """
    with open(file_name) as attch_file:
        res = decode(base64.b64encode(encode(attch_file.read())))
    return res


def get_error_message(exception_obj):
    """Get the message error from exception object or dict.

    :param exception_obj: the exception object or dict exception where get the message.
    :type: object, dict
    :return: A string containing the exception message.
    :rtype: str
    """
    error_attrs = ['stderr_output', 'explanation', 'msg', 'strerror',
                   'message', 'error_message', 'data', 'name']

    if isinstance(exception_obj, str):
        return str(exception_obj)
    for attr in error_attrs:
        if isinstance(exception_obj, dict) and exception_obj.get(attr):
            return exception_obj[attr]
        if not hasattr(exception_obj, attr):
            continue
        msg = getattr(exception_obj, attr)
        if not msg:
            continue
        msg = json_helper.load_json(msg, False) or msg
        if isinstance(msg, dict):
            msg = msg.get("error") or msg.get("message") or msg
        if isinstance(msg, bytes):
            msg = msg.decode()
        return msg
    return repr(exception_obj)


def makedir(path_name):
    path_name = os.path.expanduser(path_name)
    try:
        os.makedirs(path_name)
    except OSError as error:
        if error.errno != EEXIST:
            raise
    return path_name


def clone_repo(repo, branch, path):
    shell = spur.LocalShell()
    try:
        shell.run(
            shlex.split('git clone -b {branch} --single-branch --depth=1 {repo} {path}'.format(
                branch=branch, repo=repo, path=path)))
    except spur.results.RunProcessError as error:
        if 'Could not find remote branch' in get_error_message(error):
            raise base.errors.NoSuchBranch(branch, repo)
        if 'already exists and is not an empty directory' not in get_error_message(error):
            raise


def merge_dicts(original, new):
    """ Updates key by key a dictionary (original) with the values from another dictionary (new)
        if the value of a key in the new dictionay and the value of the same key in the original
        dictionary are dictionaries, it merges both dictionaries first, if they are lists, it
        appends the values of both lists, otherwise it will replace the value of the original
        dictionary with the value in the new one
    """
    res = original.copy()
    for new_key, new_value in new.items():
        original_value = original.get(new_key)
        if isinstance(original_value, dict) and isinstance(new_value, dict):
            new_dict = merge_dicts(original_value, new_value)
            res.update({new_key: new_dict})
        else:
            res.update({new_key: new_value})
    return res


def clean_string(string):
    """ When creating an image from a branch containing any special char like ., # or $
        or containing upper case chars docker shows an error because those are not allowed chars

    :param string: The string you want to clean
    :return: A string without the invalid chars and without upper case chars
    """
    logger.debug('Clean string %s', string)
    res = re.sub(r"[\.#\$]", "", string)
    return res.lower()


def validate_external_file(file_path):
    """ Helper method that makes sure the a file is plain text and not too big
    so it can be added to the config json.

    :param file_path: Path to the external file we want to add to the config.
    :return: True if the file is an acceptable candidate to be added to the config,
             False otherwise.
    """
    file_size = os.path.getsize(file_path)
    if os.path.splitext(file_path)[1] == '.json':
        if not json_helper.load_json(file_path):
            return False
    if file_size > 500000:
        logger.error('%s is not a valid file, it\'s size shouldn\'t be more than 500kb,'
                     ' file size: %s', file_path, file_size)
        return False
    return True


def random_string(length):
    """ Generates a random string consisting of numbers and chars with the specified length
    """
    res = u''.join(random.choice(ascii_letters+digits) for letter in range(length))
    return res


def decode(string, errors='replace'):
    if isinstance(string, binary_type) and not isinstance(string, string_types):
        return string.decode(encoding=base.CHARSET, errors=errors)
    return string


def encode(string, errors='replace'):
    if isinstance(string, string_types) and not isinstance(string, binary_type):
        return string.encode(encoding=base.CHARSET, errors=errors)
    return string


def parse_url(url):
    """ Parses an url and returns the parts that we are interested in:
        port, domain, user, destination path

    :param url: the url to be parsed, the following format is expected:
                protocol://[user@]domain.com[:port]/remote/path
    :return: Dict with the parsed values
    """
    match = re.match(
        r'^(?P<prot>\w+)://((?P<user>\w+)@)?(?P<dom>[\w|.|-]+)(:(?P<port>\d+))?/(?P<path>.*)$',
        url)
    res = dict(
        protocol=match.group('prot'),
        user=match.group('user'),
        domain=match.group('dom'),
        port=match.group('port'),
        folder=match.group('path')
    )
    return res


def upload_scp(filename, credentials, retry=3):
    logger.info('Uploading %s using SFTP', filename)
    port = credentials.get('port') if credentials.get('port') else 22
    private_key = paramiko.RSAKey.from_private_key_file(
        os.path.expanduser(os.path.join('~', '.ssh', 'id_rsa')))
    transport = paramiko.Transport((credentials.get('domain'), int(port)))
    sftp = None
    c = 0
    while c <= retry:
        try:
            transport.connect(username=credentials.get('user'), pkey=private_key)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.chdir(credentials.get('folder'))
            sftp.put(filename, os.path.basename(filename))
            c = retry + 1
        except paramiko.ssh_exception.SSHException:
            c += 1
            if c >= retry:
                raise
            logger.warning('Error while uploading the file, retry %s/%s', c, retry)
        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()


def upload_file(file_name, url):
    """ Uploads a file to the desired url using the matching protocol

    :param file_name: The full or relative path to the file that you want to upload
    :param url: the url and path to upload the file to with
                the following format: protocol://[user@]domain.com[:port]/remote/path
                if no port is provided will use 22, and if no user is provided will
                use the O.S. user that is executing the command
    """
    credentials = parse_url(url)
    if credentials.get('protocol') == 'sftp':
        upload_scp(file_name, credentials)
    else:
        raise NotImplementedError('Protocol {protocol} not implemented yet'
                                  .format(protocol=credentials.get('protocol')))


def get_backup_src(config_dict=False, deployv_config=False):
    res = False
    if config_dict and "backup_folder" in config_dict.get("container_config", {}):
        res = os.path.expanduser(config_dict.get("container_config").get("backup_folder"))
    elif deployv_config and deployv_config.has_option("deployer", "backup_folder"):
        res = os.path.expanduser(deployv_config.get("deployer", "backup_folder"))
    return res


def parse_backup_size(size):
    """Parses the backup size provided and returns the value and unit.

    :param size: string with the backup size in the format `5GB`
    :return: dictionary with the key `size_value` that contains the value of the size (int)
        and the `size_unit` key containing the unit (str)
    """
    res = {}
    if not size:
        return res
    size = size.replace(' ', '').upper()
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    exp = r'(?P<size>[\d]*([\.][\d]*)?)(?P<unit>{units})'.format(units="|".join(units))
    match = re.match(exp, size)
    if not match:
        return res
    size = float(match.group('size'))
    unit = match.group('unit')
    res.update({'size_value': size, 'size_unit': unit})
    return res


def byte_converter(from_str, to_unit='B', return_float=False):
    """Converts from one byte unit to another.

    Supported units: B, KB, MB, GB, TB, PB, EB, ZB, YB.

    :param from_str: A measure of bytes in string form. For example: '1KB', '1GB'.
    :type from_str: str
    :param to_unit: The unit you want to convert to. For example: 'GB', 'B' (default).
    :type to_unit: str
    :param return_float: If False (default) it will return the new size (always with two
        decimals) in a string form (for example: '1.00TB'). If True, it will return
        just the size as a float.
    :type return_float: bool

    :returns: The converted measure.
    :rtype: float or str
    """
    to_unit = to_unit.upper()
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    if to_unit not in units:
        return False
    from_size = parse_backup_size(from_str)
    if not from_size or from_size['size_unit'] not in units:
        return False
    base_size = 1024
    steps = units.index(from_size['size_unit']) - units.index(to_unit)
    if steps:
        to_size = from_size['size_value'] * (base_size ** steps)
    else:
        to_size = from_size['size_value'] / (base_size ** abs(steps))
    to_str = '{size:.2f}{unit}'.format(size=to_size, unit=to_unit)
    return to_size if return_float else to_str


def verify_free_disk_space(expected_free_space, directory=False):
    """Verifies that the disk has enough available space.

    :param expected_free_space: A measure of bytes in string form.
      For example: '10GB', '5MB'.
    :type expected_free_space: str
    :param directory: Directory to verify for available space. Defaults to `/`
    :type directory: str

    :returns: Whether the disk has enough space.
    :rtype: bool
    """
    directory = directory or '/'
    stats = os.statvfs(directory)
    available = float(stats.f_frsize * stats.f_bavail)
    expected = byte_converter(expected_free_space, return_float=True)
    return available >= expected


def get_certificates_pac():
    certificate_path = deployv_static.get_template_path(
        'l10n_mx_edi.certificate.csv')
    try:
        csvfile = open(certificate_path, 'r')
        certificates = list(csv.DictReader(csvfile))[0]
    except IOError:
        certificates = {}
    return certificates


def render_template(template, values=False):
    """Renders the provided jinja template with the provided values and
    returns the rendered template.
    """
    values = values or {}
    template_path = deployv_static.get_template_path(template)
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(template)
    rendered_template = template.render(values)
    return rendered_template


def is_base64_encode(string_encode):
    """verifies that the string is a base64 encoding
    """
    if not string_encode:
        return False
    try:
        base64.standard_b64decode(string_encode)
    except (binascii.Error, TypeError):
        return False
    return True


def validate_command(message, server_type):
    if not server_type:
        return {}
    command_name = message.get('command') if message.get('command') != 'ping' else False
    validate = (command_name and _AVAILABLES.get(server_type) and
                command_name not in _AVAILABLES.get(server_type))
    if validate:
        return {'error': ("the command {} is restricted for this server"
                          .format(command_name))}
    return {}


def get_size(path):
    """Gets the size of the provided file or directory in the format `5GB`,
    if an error occurs, this will return False
    """
    shell = spur.LocalShell()
    try:
        res = shell.run(shlex.split('du -sh {path}'.format(path=path)))
    except spur.results.RunProcessError as error:
        error_msg = 'Failed to get the size of {path}: {error}'.format(
            path=path, error=get_error_message(error))
        logger.warning(error_msg)
        return False
    # Get the size only and add `B` so it has the format `5GB` instead of `5G`,
    # so the methods that parse the sizes can accept it
    res = res.output.split()[0].decode() + 'B'
    return res


def get_images_path():
    """Gets the path where the docker images are stored.
    """
    shell = spur.LocalShell()
    res = shell.run(shlex.split('docker info -f "{{.DockerRootDir}}"')).output
    return res.strip(b'\n')


def get_ip_address(ifname):
    tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        tmp_sock.fileno(),
        0x8915,
        struct.pack('256s', encode(ifname[:15]))
    )[20:24])


def is_docker_ip(ip_addr):
    """Recevives an ip and checks if it is in the docker network range"""
    ip_addr = socket.gethostbyname(ip_addr)
    docker0 = re.sub(r"\.\d{1,3}$", ".0/24", get_ip_address('docker0'))
    return ipaddress.ip_address(decode(ip_addr)) in ipaddress.ip_network(decode(docker0))


def find_files(file_path, file_name):
    """Searches for files with the provided name in the provided path and
    return the list (empty if none is found)

    :param file_path: Path where the search will be done
    :param file_name: Name of the file to find
    :return: The contents of the file or False if the file was not found
    """
    shell = spur.LocalShell()
    file_path = shell.run(['find', file_path, '-name', file_name])
    res = []
    if file_path:
        lines = file_path.output.decode('utf8').split('\n')
        res = [l.strip() for l in lines if l.strip()]
    return res


def compare_repositories(repositories, new_repositories):
    """Compare the `new_repositories` with the `repositories`, it compare with
    the `path` where store the repositories, it returns the repositories
    that have any differentiate or the repository doesn't found in `repositories`.

    :param repositories: The repositories that will compare with `new_repositories`.
    :type: list
    :param new_repositories: The repositories that will compare with `repositories`.
    :type: list
    :return: The repositories that don't belong in `repositories` or have some diff.
    :rtype: list
    """
    repos_paths = {repo.get('path'): repo for repo in repositories}
    repos_diff = []
    exclude_keys = ["root['main_repo']", "root['depth']", "root['is_dirty']"]
    for new_repo in new_repositories:
        repo = repos_paths.pop(new_repo.get('path'), {})
        if not repo:
            repos_diff.append(new_repo)
            continue
        for key, value in new_repo.items():
            if key == 'repo_url':
                value.update({'origin': encode(value.get('origin'))})
                continue
            if key == 'commit':
                new_repo.update({key: encode(value[:7])})
                repo.update({key: repo.get(key)[:7]})
                continue
            new_repo.update({key: encode(value)})
        diff = DeepDiff(new_repo, repo, exclude_paths=exclude_keys)
        if diff.get('type_changes'):
            repos_diff.append(new_repo)
    return repos_diff


def parse_variables_to_json(variables):
    """Convert to dict the env variables used to execute a process in the instance.

    :param variables: the enviroment variables used to build/create/restore
        and other things that can do with the instance.
    :type: str
    :return: a dict with the information getted in `variables`.
    :rtype: dict
    """
    if not variables:
        return {}
    if isinstance(variables, list):
        vs = [v.replace('export', '').strip() for v in variables]
    else:
        vs = variables.replace('export', '').strip().split('\n')
    return container.parse_env_vars(vs)


def add_repo(branch, name, repo_path, repo_url, commit=False, config=False,
             overwrite_repos=False, extra=False):
    """Creates a dictionary with the info of the specified repository and
    appends it to the repositories list in the config dictionary or
    return the dict created.

    :param config: Config dict where the new repo will be added
    :param name: Name of the repository
    :param path: Path inside ~/instance where the repository will be cloned
    :param repo_url: ssh or https URL used to clone the repo
    :param branch: branch of the repo we want to clone
    :param commit: the commit of repository
    :param overwrite_repos: Identificator to overwrite the repositories.
    :type overwrite_repos: bool
    :return: Config dict with the new repo
    """
    repo = {
        'branch': branch, 'name': name, 'path': repo_path,
        'commit': commit or '', 'depth': 1,
        'repo_url': {'origin': repo_url}
    }
    repo.update(extra or {})
    if not config:
        return repo
    if overwrite_repos:
        config.get('instance', {}).update({'repositories': [repo]})
    else:
        config.get('instance', {}).get('repositories', []).append(repo)
    return config


def parse_repo_url(repo_url):
    """Parses the provided url to get its parts such as the protocol,
    the org, the repo name, and the domain. The url can be in either format:

    https://github.com/organization/repo
    git@github.com:organization/repo.git

    :param repo_url: URL to be parsed
    :type: string
    :return: dictionary with the parts of the url, if the url contains
        git@ instead of a proper protocol, https:// will be returned
        as the protocol
    """
    if not repo_url:
        return {}
    regex = (
        r'(?P<protocol>git@|http[s]?:\/\/)(?P<domain>[\.\w\d-]*)[:\/]{1}'
        r'(?P<repo>(?P<namespace>[\w\d-]*)/(?P<repo_name>[\w\d-]*))(\.git)?'
    )
    res = re.match(regex, repo_url)
    if not res:
        return {}
    values = res.groupdict()
    if values['protocol'] == 'git@':
        values.update({'protocol': 'https://'})
    return values


def read_lines(filename):
    """Returns a file content as a list, no blank lines and stipped

    :param filename: Fill path to the file
    :return: A list with the file content, empty if no lines
    """
    with open(filename, 'r') as obj:
        file_contents = obj.read()
    lines = file_contents.split('\n')
    res = [l.strip() for l in lines if l.strip()]
    return res


def deploy_key(ssh_key, folder_path):
    """Deploy a SSH private key into the temporal working folder.
    """
    if not is_base64_encode(ssh_key):
        logger.warning("Can not use the specified ssh key. It is not encoded in base64")
        return False
    logger.info('Deploying keys')
    ssh_key = decode(base64.b64decode(ssh_key))
    filename = os.path.join(folder_path, 'id_rsa')
    with open(filename, 'w') as key_file:
        key_file.write(ssh_key)
    os.chmod(filename, S_IREAD + S_IWRITE)
    return filename


def get_main_repo(repos):
    """Get the main repository from a list of repositories.
    """
    main = [r for r in repos if r.get('main_repo')]
    return main and main[0] or {}
