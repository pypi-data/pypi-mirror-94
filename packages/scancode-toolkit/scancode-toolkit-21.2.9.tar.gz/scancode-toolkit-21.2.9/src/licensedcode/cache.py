#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#
import os
from functools import partial
from hashlib import md5

from commoncode.fileutils import resource_iter
from commoncode.fileutils import create_dir
from commoncode import ignore

from scancode_config import licensedcode_cache_dir
from scancode_config import scancode_src_dir
from scancode_config import SCANCODE_DEV_MODE

"""
An on-disk persistent cache of LicenseIndex. The index is pickled and
invalidated if there are any changes in the code or licenses text or rules.
Loading and dumping the cached index is safe to use across multiple processes
using lock files.
"""

LICENSE_INDEX_LOCK_TIMEOUT = 60 * 4

# global in-memory cache of the main license index instance
_LICENSES_BY_KEY_INDEX = None


def get_index(
    cache_dir=licensedcode_cache_dir,
    check_consistency=SCANCODE_DEV_MODE,
    return_value=True,
):
    """
    Return and eventually cache an index built from an iterable of rules.
    Build the index from the built-in rules dataset.
    """
    global _LICENSES_BY_KEY_INDEX
    if not _LICENSES_BY_KEY_INDEX:
        _LICENSES_BY_KEY_INDEX = get_cached_index(cache_dir, check_consistency)
    if return_value:
        return _LICENSES_BY_KEY_INDEX


# global in-memory cache of a mapping of key -> license instance
_LICENSES_BY_KEY = {}


def get_licenses_db(licenses_data_dir=None, _test_mode=False):
    """
    Return a mapping of license key -> license object.
    """
    global _LICENSES_BY_KEY
    if not _LICENSES_BY_KEY or _test_mode:
        from licensedcode.models import load_licenses
        if not licenses_data_dir:
            from licensedcode.models import licenses_data_dir as ldd
            licenses_data_dir = ldd
        lics_by_key = load_licenses(licenses_data_dir)

        if _test_mode:
            # Do not cache when testing
            return lics_by_key

        _LICENSES_BY_KEY = lics_by_key
    return _LICENSES_BY_KEY


# global in-memory cache of Licensing object built from all active licenses
_LICENSING = {}


def get_licensing(_test_licenses=None):
    """
    Return and cache a license_expression.Licensing objet built from the all the
    licenses.
    """
    global _LICENSING
    if not _LICENSING or _test_licenses:

        if _test_licenses:
            licenses = _test_licenses
        else:
            licenses = get_licenses_db()

        from license_expression import LicenseSymbolLike
        from license_expression import Licensing

        licensing = Licensing((LicenseSymbolLike(lic) for lic in licenses.values()))

        if _test_licenses:
            # Do not cache when testing
            return licensing

        _LICENSING = licensing

    return _LICENSING


# global in-memory cache for the unknown license symbol
_UNKNOWN_SPDX_SYMBOL = None


def get_unknown_spdx_symbol(_test_licenses=None):
    """
    Return the unknown SPDX license symbol.

    Note: the `_test_licenses` arg is a mapping of key: license used for testing
    instead of the standard license db.
    """
    global _UNKNOWN_SPDX_SYMBOL
    if not _UNKNOWN_SPDX_SYMBOL or _test_licenses:
        from license_expression import LicenseSymbolLike

        if _test_licenses:
            licenses = _test_licenses
        else:
            licenses = get_licenses_db()

        unknown = LicenseSymbolLike(licenses[u'unknown-spdx'])

        if _test_licenses:
            # Do not cache when testing
            return unknown

        _UNKNOWN_SPDX_SYMBOL = unknown
    return _UNKNOWN_SPDX_SYMBOL


# global in-memory cache for SPDX license as a LicenseSymbol->LicenseLikeSymbol
# wrapping a full License object
_LICENSE_SYMBOLS_BY_SPDX_KEY = None


def get_spdx_symbols(_test_licenses=None):
    """
    Return a mapping of {lowercased SPDX license key: LicenseSymbolLike} where
    LicenseSymbolLike wraps a License object

    Note: the `_test_licenses` arg is a mapping of key: license used for testing
    instead of the standard license db.
    """
    global _LICENSE_SYMBOLS_BY_SPDX_KEY
    if not _LICENSE_SYMBOLS_BY_SPDX_KEY or _test_licenses:
        from license_expression import LicenseSymbolLike
        symbols_by_spdx_key = {}

        if _test_licenses:
            licenses = _test_licenses
        else:
            licenses = get_licenses_db()

        for lic in licenses.values():
            if not (lic.spdx_license_key or lic.other_spdx_license_keys):
                continue

            symbol = LicenseSymbolLike(lic)
            if lic.spdx_license_key:
                slk = lic.spdx_license_key.lower()
                existing = symbols_by_spdx_key.get(slk)
                if existing:
                    raise ValueError(
                        'Duplicated SPDX license key: %(slk)r defined in '
                        '%(lic)r and %(existing)r' % locals())

                symbols_by_spdx_key[slk] = symbol

            for other_spdx in lic.other_spdx_license_keys:
                if not (other_spdx and other_spdx.strip()):
                    continue
                slk = other_spdx.lower()
                existing = symbols_by_spdx_key.get(slk)
                if existing:
                    raise ValueError(
                        'Duplicated "other" SPDX license key: %(slk)r defined '
                        'in %(lic)r and %(existing)r' % locals())
                symbols_by_spdx_key[slk] = symbol

        if _test_licenses:
            # Do not cache when testing
            return symbols_by_spdx_key

        _LICENSE_SYMBOLS_BY_SPDX_KEY = symbols_by_spdx_key
    return _LICENSE_SYMBOLS_BY_SPDX_KEY


def get_cached_index(
    cache_dir=licensedcode_cache_dir,
    check_consistency=SCANCODE_DEV_MODE,
    # used for testing only
    timeout=LICENSE_INDEX_LOCK_TIMEOUT,
    tree_base_dir=scancode_src_dir,
    licenses_data_dir=None,
    rules_data_dir=None,
    use_dumps=True,
):
    """
    Return a LicenseIndex: either load a cached index or build and cache the
    index.
    - If the cache does not exist, a new index is built and cached.
    - If `check_consistency` is True, the cache is checked for consistency and
      rebuilt if inconsistent or stale.
    - If `check_consistency` is False, the cache is NOT checked for consistency
      If the cache files exist but ARE stale, the cache WILL NOT be rebuilt
    """
    from licensedcode.index import LicenseIndex
    from licensedcode.models import get_rules
    from licensedcode.models import get_all_spdx_key_tokens
    from licensedcode.models import licenses_data_dir as ldd
    from licensedcode.models import rules_data_dir as rdd

    from scancode import lockfile

    licenses_data_dir = licenses_data_dir or ldd
    rules_data_dir = rules_data_dir or rdd

    lock_file, checksum_file, cache_file = get_license_cache_paths(cache_dir)

    has_cache = os.path.exists(cache_file)
    # bypass check if no consistency check is needed
    if has_cache and not check_consistency:
        return load_index(cache_file)

    has_tree_checksum = os.path.exists(checksum_file)

    # here, we have no cache or we want a validity check: lock, check
    # and build or rebuild as needed
    try:
        # acquire lock and wait until timeout to get a lock or die
        with lockfile.FileLock(lock_file).locked(timeout=timeout):
            current_checksum = None
            # is the current cache consistent or stale?
            if has_cache and has_tree_checksum:
                # if we have a saved cached index
                # load saved tree_checksum and compare with current tree_checksum
                with open(checksum_file, 'r') as etcs:
                    existing_checksum = etcs.read()
                current_checksum = tree_checksum(tree_base_dir=tree_base_dir)
                if current_checksum == existing_checksum:
                    # The cache is consistent with the latest code and data
                    # load and return
                    return load_index(cache_file)

            # Here, the cache is not consistent with the latest code and
            # data: It is either stale or non-existing: we need to
            # rebuild the index and cache it

            # FIXME: caching a pickle of this would be 10x times faster
            license_db = get_licenses_db(licenses_data_dir=licenses_data_dir)

            rules = get_rules(
                licenses_data_dir=licenses_data_dir,
                rules_data_dir=rules_data_dir)

            spdx_tokens = set(get_all_spdx_key_tokens(license_db))

            idx = LicenseIndex(rules, _spdx_tokens=spdx_tokens)

            with open(cache_file, 'wb') as ifc:
                if use_dumps:
                    ifc.write(idx.dumps())
                else:
                    idx.dump(ifc)

            # save the new tree checksum
            current_checksum = tree_checksum(tree_base_dir=tree_base_dir)
            with open(checksum_file, 'w') as ctcs:
                ctcs.write(current_checksum)

            return idx

    except lockfile.LockTimeout:
        # TODO: handle unable to lock in a nicer way
        raise


def load_index(cache_file, use_loads=False):
    """
    Return a LicenseIndex loaded from cache.
    """
    from licensedcode.index import LicenseIndex
    with open(cache_file, 'rb') as ifc:
        # Note: weird but read() + loads() is much (twice++???) faster than load()
        try:
            if use_loads:
                return LicenseIndex.loads(ifc.read())
            else:
                return LicenseIndex.load(ifc)
        except Exception as e:
            import traceback
            msg = (
                '\n'
                'ERROR: Failed to load license cache (the file may be corrupted ?).\n'
                'Please delete "{cache_file}" and retry.\n'
                'If the problem persists, copy this error message '
                'and submit a bug report.\n'.format(**locals())
            )
            msg += '\n' + traceback.format_exc()
            raise Exception(msg)


_ignored_from_hash = partial(
    ignore.is_ignored,
    ignores={
        '*.pyc': 'pyc files',
        '*~': 'temp gedit files',
        '*.swp': 'vi swap files',
    },
    unignores={}
)

licensedcode_dir = os.path.join(scancode_src_dir, 'licensedcode')


def tree_checksum(tree_base_dir=licensedcode_dir, _ignored=_ignored_from_hash):
    """
    Return a checksum computed from a file tree using the file paths, size and
    last modified time stamps. The purpose is to detect is there has been any
    modification to source code or data files and use this as a proxy to verify
    the cache consistency.

    NOTE: this is not 100% fool proof but good enough in practice.
    """
    resources = resource_iter(tree_base_dir, ignored=_ignored, with_dirs=False)
    hashable = (pth + str(os.path.getmtime(pth)) + str(os.path.getsize(pth)) for pth in resources)
    hashable = ''.join(sorted(hashable))
    hashable = hashable.encode('utf-8')
    return md5(hashable).hexdigest()


def get_license_cache_paths(cache_dir=licensedcode_cache_dir):
    """
    Return a tuple of index cache files given a master `cache_dir`
    """
    idx_cache_dir = os.path.join(cache_dir, 'license_index')
    create_dir(idx_cache_dir)

    lock_file = os.path.join(idx_cache_dir, 'lockfile')
    checksum_file = os.path.join(idx_cache_dir, 'tree_checksums')
    cache_file = os.path.join(idx_cache_dir, 'index_cache')

    return lock_file, checksum_file, cache_file
