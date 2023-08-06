# -*- coding: utf-8 -*-
"""Tools to deal with HDF5 cache files HDF5 cache files are used to cache
Energy Database files, and Line Database files, and yield a much faster access
time.

Routine Listing
---------------


- :func:`~radis.misc.cache_file.check_cache_file`
- :func:`~radis.misc.cache_file.check_not_deprecated`
- :func:`~radis.misc.cache_file.save_to_hdf`

See Also
--------

:py:func:`~radis.io.hitran.hit2df`,
:py:func:`~radis.io.cdsd.cdsd2df`

-------------------------------------------------------------------------------
"""
# TODO: start using .feather format. Faster than HDF5 for pandas Dataframe,
# and can be multithreaded.
# see:
# https://gist.github.com/gansanay/4514ec731da1a40d8811a2b3c313f836
# and pd.read_feather(file, nthreads=3)


# Note: don't import unicode_literals because it breaks the df.to_hdf of
# save_to_hdf because of a stupid unicode/str error in Python 2.7
import os
from os.path import exists, splitext
from warnings import warn

import pandas as pd
from packaging.version import parse

import radis
from radis import OLDEST_COMPATIBLE_VERSION
from radis.misc.basics import compare_dict, is_float
from radis.misc.printer import printm, printr
from radis.misc.warning import DeprecatedFileWarning, IrrelevantFileWarning

"""str: forces to regenerate cache files that were created in a previous version"""

# Just make sure LAST_BACKWARD_COMPATIBLE_VERSION is valid
assert radis.__version__ >= OLDEST_COMPATIBLE_VERSION

# Utils


def load_h5_cache_file(
    cachefile,
    use_cached,
    valid_if_metadata_is={},
    relevant_if_metadata_above={},
    relevant_if_metadata_below={},
    current_version="",
    last_compatible_version=OLDEST_COMPATIBLE_VERSION,
    verbose=True,
):
    """Function to load a h5 cache file.

    Parameters
    ----------
    cachefile: str
        cache file path
    use_cached: str
        use cache file if value is not ``False``:

        - if ``True``, use (and generate if doesnt exist) cache file.
        - if ``'regen'``, delete cache file (if exists) so it is regenerated
        - if ``'force'``, use cache file and raises an error if it doesnt exist

        if using the cache file, check if the file is deprecated. If it
        is deprecated, regenerate the file unless ``'force'`` was used
        (in that case, raise an error)
    valid_if_metadata_is: dict
        values are compared to cache file attributes. If they dont match,
        the file is considered deprecated. See ``use_cached`` to know
        how to handle deprecated files

        .. note::
            if the file has extra attributes they are not compared
    current_version: str
        version is compared to cache file version (part of attributes).
        If current version is superior, a simple warning is triggered.
    last_compatible_version: str
        if file version is inferior to this, file is considered deprecated.
        See ``use_cached`` to know how to handle deprecated files.
        Default :data:`~radis.OLDEST_COMPATIBLE_VERSION`.
    relevant_if_metadata_above, relevant_if_metadata_below : dict
        values are compared to cache file attributes. If they don't match,
        the function returns a :py:class:`~radis.misc.warning.IrrelevantFileWarning`.
        For instance, load a line database file, only if it contains wavenumbers
        between 2300 and 2500 cm-1 ::

                load_h5_cache_file(..., relevant_if_metadata_above={'wav':2300};
                relevant_if_metadata_below={'wav':2500})

        Note that in such an example, the file data is not read. Only the
        file metadata is. If the metadata does not contain the key (e.g.: ``'wav'``)
        a :py:class:`~radis.misc.warning.DeprecatedFileWarning` is raised.

    Returns
    -------
    df: pandas DataFrame, or None
        None if no cache file was found, or if it was deleted


    See Also
    --------

    :data:`~radis.OLDEST_COMPATIBLE_VERSION`
    """

    # 1. know if we have to load the file
    if not use_cached:
        return None
    elif use_cached == "regen" and exists(cachefile):
        os.remove(cachefile)
        if verbose:
            printm("Deleted h5 cache file : {0}".format(cachefile))
        return None

    # 2. check the file is here
    if not exists(cachefile):
        if use_cached == "force":
            raise ValueError("Cache file {0} doesnt exist".format(cachefile))
        else:
            return None  # File doesn't exist. It's okay.

    # 3. read file attributes to know if it's deprecated
    try:
        check_not_deprecated(
            cachefile,
            metadata_is=valid_if_metadata_is,
            metadata_keys_contain=list(relevant_if_metadata_above.keys())
            + list(relevant_if_metadata_below.keys()),
            current_version=current_version,
            last_compatible_version=last_compatible_version,
        )
    # ... if deprecated, raise an error only if 'force'
    except DeprecatedFileWarning as err:
        if use_cached == "force":
            raise err
        else:
            if verbose:
                printr(
                    "File {0} deprecated:\n{1}\nDeleting it!".format(
                        cachefile, str(err)
                    )
                )
            os.remove(cachefile)
            return None

    # 4. File is not not deprecated: read the the extremum wavenumbers.    raise
    if relevant_if_metadata_above is not None or relevant_if_metadata_below is not None:
        try:
            check_relevancy(
                cachefile,
                relevant_if_metadata_above,
                relevant_if_metadata_below,
            )
        # ... if irrelevant, raise an error only if 'force'
        except IrrelevantFileWarning as err:
            if verbose >= 2:
                from radis.misc.printer import printg

                printg("Database file {0} irrelevant and not loaded".format(cachefile))
            raise err

    # 5. File is relevant: read the content.
    df = None
    if verbose >= 2:
        printm("Reading cache file ({0})".format(cachefile))
    try:
        df = pd.read_hdf(cachefile, "df")
    except KeyError as err:  # An error happened during file reading.
        # Fail safe by deleting cache file (unless we explicitely wanted it
        # with 'force')
        if use_cached == "force":
            raise
        else:
            if verbose:
                printr(
                    "An error happened during cache file reading "
                    + "{0}:\n{1}\n".format(cachefile, str(err))
                    + "Deleting cache file to regenerate it"
                )
            os.remove(cachefile)
            df = None

    return df


def get_cache_file(fcache, verbose=True):
    """Load HDF5 cache file.

    Parameters
    ----------
    fcache: str
        file name

    Other Parameters
    ----------------
    verbose: bool
        If >=2, also warns if non numeric values are present (it would make
        calculations slower)

    Notes
    -----

    we could start using FEATHER format instead. See notes in cache_files.py
    """

    # Load file

    df = pd.read_hdf(fcache, "df")

    # Check file

    # ... 'object' columns slow everything down (not fixed format strings!)
    if verbose >= 2:
        _warn_if_object_columns(df, fcache)

    return df


def check_cache_file(fcache, use_cached=True, expected_metadata={}, verbose=True):
    """Quick function that check status of cache file generated by RADIS:

    The function first checks the existence of ``fcache``. What is does depends
    on the value of ``use_cached``:

    - if ``True``, check it exists and remove the file if it is not valid.
    - if ``'regen'``, delete cache file even if valid, to regenerate it later.
    - if ``'force'``, raise an error if file doesnt exist.

    Then look if it is deprecated (we just look at the attributes, the file
    is never fully read). Deprecation is done by :py:func:`~radis.io.cache_files.check_not_deprecated`
    comparing the ``metadata=`` content.

    - if deprecated, deletes it to regenerate later unless 'force' was used

    Parameters
    ----------
    fcache: str
        cache file name
    use_cached: ``True``, ``False``, ``'force'``, ``'regen'``
        see notes above. Default ``True``.
    expected_metadata: dict
        attributes to check
    verbose: boolean
        print stuff

    Returns
    -------

    None
        whether the file was valid or not (and was removed).
        Raises a :py:class:`~radis.misc.warning.DeprecatedFileWarning` for
        un unvalid file in mode ``'force'``. The error can be caught by the
        parent function.

    See Also
    --------

    :py:func:`~radis.io.cache_files.check_not_deprecated`
    """

    # Test existence of file:
    if not use_cached:
        return  # we dont want a cache file, no need to test it
    elif use_cached == "regen":
        if exists(fcache):
            os.remove(fcache)
            if verbose:
                print(("Deleted h5 cache file : {0}".format(fcache)))
    elif use_cached == "force":
        if not exists(fcache):
            raise ValueError("Cache file {0} doesnt exist".format(fcache))
    else:  # use_cached == True
        pass  # just use the file as is

    # If file is still here, test if it is deprecated:
    # (we just read the attributes, the file is never fully read)
    if exists(fcache):
        if verbose:
            print(("Using cache file: {0}".format(fcache)))
        try:
            check_not_deprecated(
                fcache,
                metadata_is=expected_metadata,
                current_version=radis.__version__,
                last_compatible_version=OLDEST_COMPATIBLE_VERSION,
            )
        except DeprecatedFileWarning as err:
            if use_cached == "force":
                raise
            else:  # delete file to regenerate it in the end of the script
                if verbose:
                    printr(
                        "File {0} deprecated:\n{1}\nDeleting it!".format(
                            fcache, str(err)
                        )
                    )
                os.remove(fcache)

    return


def check_not_deprecated(
    file,
    metadata_is={},
    metadata_keys_contain=[],
    current_version=None,
    last_compatible_version=OLDEST_COMPATIBLE_VERSION,
):
    """Make sure cache file is not deprecated: checks that ``metadata`` is the
    same, and that the version under which the file was generated is valid.

    Parameters
    ----------
    file: str
        a `` .h5`` cache file for Energy Levels
    metadata_is: dict
        expected values for these variables in the file metadata. If the values dont match,
        a :py:func:`~radis.misc.warning.DeprecatedFileWarning` error is raised.
        If the file metadata contains additional keys/values, no error is raised.
    metadata_keys_contain: list
        expected list of variables in the file metadata. If the keys are not there,
        a :py:func:`~radis.misc.warning.DeprecatedFileWarning` error is raised.

    Other Parameters
    ----------------
    current_version: str, or ``None``
        current version number. If the file was generated in a previous version
        a warning is raised. If ``None``, current version is read from
        :data:`radis.__version__`.
    last_backward_compatible_version: str
        If the file was generated in a non-compatible version, an error is raised.
        Default :py:data:`~radis.OLDEST_COMPATIBLE_VERSION`
        (useful parameter to force regeneration of certain cache files after a
         breaking change in a new version)
    """

    # # Get attributes (metadata+version)
    with pd.HDFStore(file, mode="r") as store:
        # Errors due to old files generated with h5py. Remove after 1.0
        try:
            file_metadata = store.get_storer("df").attrs.metadata
        except AttributeError as err:
            if "Attribute 'metadata' does not exist in node: '/df'" in str(err):
                raise DeprecatedFileWarning(
                    "Cache files metadata is read/written with pytables instead of h5py starting from radis>=0.9.28. You should regenerate your file {0}".format(
                        file
                    )
                ) from err
        except TypeError as err:
            if "cannot properly create the storer" in str(err):
                raise DeprecatedFileWarning(
                    "Cache files metadata is read/written with pytables instead of h5py starting from radis>=0.9.28. You should regenerate your file {0}".format(
                        file
                    )
                ) from err

    # Raise an error if version is not found
    try:
        file_version = file_metadata.pop("version")
    except KeyError:
        raise DeprecatedFileWarning(
            "File {0} is deprecated : ".format(file)
            + "RADIS version missing in metadata. Delete it to regenerate it on next run"
        )

    # Get current version
    if current_version is None:
        current_version = radis.__version__

    # If file version is anterior to a major change
    # ... Update here versions afterwhich Deprecated cache file is not safe
    # ... (example: a key name was changed)
    if parse(file_version) < parse(last_compatible_version):
        raise DeprecatedFileWarning(
            "File {0} has been generated in a deprecated ".format(file)
            + "version ({0}). Oldest compatible version is {1}. ".format(
                file_version, last_compatible_version
            )
            + "Delete the file to regenerate it on next run"
        )

    # If file version is outdated: Warning, but no error
    if parse(current_version) > parse(file_version):
        warn(
            DeprecationWarning(
                "File {0} has been generated in ".format(file)
                + "a deprecated version ({0}) compared to current ({1})".format(
                    file_version, current_version
                )
                + ". Delete it to regenerate it on next run"
            )
        )
        out = False
    elif parse(current_version) == parse(file_version):
        out = True
    else:
        raise ValueError(
            "Cache file ({0}) generated with a future version ({1} > {2})? ".format(
                file, file_version, current_version
            )
            + "Do you own a DeLorean? Delete the file manually if you understand what happened"
        )

    # Make sure metadata keys are there:
    for k in metadata_keys_contain:
        if k not in file_metadata:
            raise DeprecatedFileWarning(
                "Metadata in file {0} doesn't contain the expected key `{1}`. ".format(
                    file, k
                )
            )

    # Compare metadata values
    # ignore additional keys in the file attributes.
    metadata_is = _h5_compatible(metadata_is)
    file_metadata = {k: v for k, v in file_metadata.items() if k in metadata_is}
    out, compare_string = compare_dict(
        metadata_is,
        file_metadata,
        verbose=False,
        return_string=True,
        df1_str="Expected",
        df2_str="Got",
    )
    if out != 1:
        raise DeprecatedFileWarning(
            "Metadata in file {0} dont match ".format(file)
            + "expected values. See comparison below:"
            + "\n\tExpected\tFile\n{0}".format(compare_string)
        )

    return out


def _h5_compatible(a_dict):
    """Make dictionary ``a_dict`` h5 compatible."""
    out = {}
    for k, v in a_dict.items():
        if v is None:
            continue  # dont store None
        elif is_float(v):
            out[k] = v
        else:
            out[k] = str(v)  # convert to str
    return out


def check_relevancy(
    file,
    relevant_if_metadata_above,
    relevant_if_metadata_below,
    verbose=True,
    key="df",
):
    """Make sure cache file is relevant.

    Use case: checks that  wavenumber min and
    wavenumber max in ``metadata`` are relevant for the specified spectral
    range.

    Parameters
    ----------
    file: str
        a `` .h5``  line database cache file
    load_only_wavenum_above, relevant_if_metadata_below: dict
        only load the cached file if the metadata values are above/below
        the specific values for each key.
    relevant_if_metadata_above, relevant_if_metadata_below: dict
        file is relevant if the file metadata value for each key of the dictionary
        is above/below the value in the dictionary

    Other Parameters
    ----------------
    key: str
        dataset key in storer.

    Examples
    --------
    You want to compute a spectrum in between 2300 and 2500 cm-1. A line database
    file is relevant only if its metadata says that ``'wavenum_max' > 2300``
    and ``'wavenum_min'`` < 2500 cm-1.

        check_relevancy('path/to/file', relevant_if_metadata_above={'wavenum_max':2300},
                        relevant_if_metadata_below={'wavenum_min':2500})

        the specified value.

    """
    # Add metadata
    with pd.HDFStore(file, mode="r") as store:
        file_metadata = store.get_storer(key).attrs.metadata

    for k, v in relevant_if_metadata_above.items():
        # Note : check_not_deprecated already tested the existence of each key so we are safe
        if file_metadata[k] < v:
            raise IrrelevantFileWarning(
                "Database file {0} irrelevant: {1}={2} [file metadata] < {3} [expected], not loaded".format(
                    file, k, file_metadata[k], v
                )
            )
    for k, v in relevant_if_metadata_below.items():
        # Note : check_not_deprecated already tested the existence of each key so we are safe
        if file_metadata[k] > v:
            raise IrrelevantFileWarning(
                "Database file {0} irrelevant ({1}={2} [file metadata] > {3} [expected]), not loaded".format(
                    file, k, file_metadata[k], v
                )
            )


def _warn_if_object_columns(df, fname):
    """'object' columns slow everything down (not fixed format strings!)"""
    objects = [k for k, v in df.dtypes.items() if v == object]
    if len(objects) > 0:
        warn(
            "Dataframe in {0} contains `object` format columns: {1}. ".format(
                fname, objects
            )
            + "Operations will be slower. Try to convert them to numeric."
        )


def save_to_hdf(
    df, fname, metadata, version=None, key="df", overwrite=True, verbose=True
):
    """Save energy levels or lines to HDF5 file. Add metadata and version.

    Parameters
    ----------
    df: a pandas DataFrame
        data will be stored in the key ``'df'``
    fname: str
        ``.h5`` file where to store.
    metadata: dict
         dictionary of values that were used to generate the DataFrame. Metadata
         will be asked again on file load to ensure it hasnt changed. ``None``
         values are not stored.
    version: str, or ``None``
        file version. If ``None``, the current :data:`radis.__version__` is used.
        On file loading, a warning will be raised if the current version is
        posterior, or an error if the file version is set to be uncompatible.
        See :py:data:`~radis.OLDEST_COMPATIBLE_VERSION`
    key: str
        dataset name. Default ``'df'``
    overwrite: boolean
        if ``True``, overwrites file. Else, raise an error if it exists.

    Other Parameters
    ----------------
    verbose: bool
        If >=2, also warns if non numeric values are present (it would make
        calculations slower)

    Notes
    -----
    ``None`` values are not stored
    """
    # Check file
    assert fname.endswith(".h5")
    assert "version" not in metadata
    # ... 'object' columns slow everything down (not fixed format strings!)
    if verbose >= 2:
        _warn_if_object_columns(df, fname)

    # Update metadata format
    metadata = _h5_compatible(metadata)

    # Overwrite file
    if exists(fname) and not overwrite:
        raise ValueError("File exist: {0}".format(fname))

    # start by exporting dataframe
    df.to_hdf(fname, key, format="fixed", mode="a", complevel=9, complib="blosc")

    # Add metadata

    # ... add RADIS version
    if version is None:
        version = radis.__version__
    metadata.update({"version": version})

    with pd.HDFStore(fname, mode="a") as store:
        store.get_storer(key).attrs.metadata = metadata

    if verbose >= 3:
        print("... saved {0} with metadata: {1}".format(fname, metadata))


def filter_metadata(arguments, discard_variables=["self", "verbose"]):
    """Filter arguments (created with  ``locals()`` at the beginning of the
    script) to extract metadata.

    Metadata is stored as attributes in the cached
    file:

    - remove variables in ``discard_variables``
    - remove variables that start with ``'_'``
    - remove varibles whose value is ``None``

    Parameters
    ----------
    arguments: dict
        list of local variables. For instance::

            arguments = locals()
    discard_variables: list of str
        variable names to discard

    Returns
    -------
    metadata: dict
        a (new) dictionary built from arguments by removing ``discard_variables``
        and variables starting with ``'_'``

    Examples
    --------
    How to get only function argument::

        def some_function(*args):
            metadata = locals()     # stores only function arguments because it's the first line

            ...

            metadata = filter_metadata(metadata)
            save_to_hdf(df, fname, metadata=metadata)

            ...
    """
    # TODO: adding metadata this way is not explicit & hard to maintain, should be removed.
    metadata = {k: v for (k, v) in arguments.items() if not k.startswith("_")}
    metadata = {k: v for (k, v) in metadata.items() if k not in discard_variables}
    metadata = {k: v for (k, v) in metadata.items() if v is not None}

    return metadata


def cache_file_name(fname):
    """Return the corresponding cache file name for fname."""
    return splitext(fname)[0] + ".h5"


if __name__ == "__main__":
    import pytest

    # Run relevant tests (here:  the ones with 'cache' in their name)
    printm("Testing cache files:", pytest.main(["../test/io/", "-k", "cache"]))
    printm("Testing cache files:", pytest.main(["../test/lbl/", "-k", "cache"]))
