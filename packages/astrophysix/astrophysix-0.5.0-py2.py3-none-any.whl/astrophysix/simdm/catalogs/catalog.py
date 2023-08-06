# -*- coding: utf-8 -*-
# This file is part of the 'astrophysix' Python package.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility

import uuid
import pandas as pd

from future.builtins import str, list, int
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable

from .targobj import TargetObject, ObjectProperty, PropertyFilterFlag
from ..datafiles import Datafile
from ..utils import ObjectList, GalacticaValidityCheckMixin, DataType
from ...utils import NumpyUtil

log = logging.getLogger("astrophysix.simdm")


class CatalogField(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    def __init__(self, *args, **kwargs):
        """
        Object catalog field class

        Parameters
        ----------
        obj_prop: :class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty`
            target object property (mandatory)
        values: 1D :class:`numpy.ndarray`
            catalog field value series/1D array (mandatory)
        """
        super(CatalogField, self).__init__(**kwargs)

        # Target object property
        self._obj_property = None
        if len(args) > 0:
            obj_prop = args[0]
        elif "obj_prop" in kwargs:
            obj_prop = kwargs["obj_prop"]
        else:
            raise AttributeError("Undefined 'obj_prop' object property attribute in "
                                 "{cname:s}.".format(cname=self.__class__.__name__))

        if not isinstance(obj_prop, ObjectProperty):
            err_msg = "{cname:s} 'obj_prop' attribute is not a valid ObjectProperty " \
                      "instance.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._obj_property = obj_prop

        # Field values for all catalog items
        self._val_series = None
        self._values_md5sum = None
        self._values_min = None
        self._values_max = None
        self._values_mean = None
        self._values_std = None
        self._nobj = 0

        if not kwargs.get("hdf5_init", False):
            if "values" not in kwargs:
                raise AttributeError("Undefined 'values' property in {cname:s}.".format(cname=self.__class__.__name__))
            self.field_values = kwargs["values"]

    def __eq__(self, other):
        """
        CatalogField comparison method

        other: :class:`~astrophysix.simdm.catalogs.catalog.CatalogField`
            catalog field object to compare to
        """
        if not super(CatalogField, self).__eq__(other):
            return False

        # Compare target object property
        if self._obj_property != other.object_property:
            return False

        # Compare catalog field value MD5 sums
        if self._values_md5sum != other._values_md5sum:
            return False

        return True

    @property
    def property_name(self):
        """Associated target object property name"""
        return self._obj_property.property_name

    @property
    def object_property(self):
        """Associated target object property (:class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty`)"""
        return self._obj_property

    @property
    def field_values(self):
        """
        Catalog field values. Can be edited.

        Returns
        -------
        vals: :obj:`1D numpy.ndarray`
        """
        self._hsp_lazy_read()
        return self._val_series

    @field_values.setter
    def field_values(self, new_vals):
        """
        Set catalog field values arrays. The new array must be of size strictly positive and leave the its size
        unchanged.

        Parameters
        ----------
        new_vals: :obj:`1D numpy.ndarray`
            catalog field value 1D array

        Raises
        ------
        Aerr: :class:`AttributeError`
            an error is raised if the new array does not contain any value or if its size is different from the previous
            value array.

        Example
        -------

            >>> pass
        """
        # Record new catalog field value array
        try:
            # TODO Check numeric type ???
            NumpyUtil.check_is_array(new_vals, ndim=1)
        except AttributeError:
            err_msg = "'values' {cname:s} attribute must be a 1-dimensional " \
                      "array.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        if self._nobj == 0:  # CatalogField initialisation
            # Array size => number of items in catalog
            if new_vals.size == 0:  # No value in catalog field !
                err_msg = "{cname:s} 'values' array need at least 1 value.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._nobj = new_vals.size
        else:  # Field values were previously set. This is an update.
            # Check that array size (number of catalog items) is unchanged
            if self._nobj != new_vals.size:
                err_msg = "The number of items in this {cname:s} is {no:d} and cannot be " \
                          "changed.".format(no=self._nobj, cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
        self._val_series = new_vals.copy()  # Make a copy so that external modification won't impact the catalog field
        self._values_max = self._val_series.max()
        self._values_min = self._val_series.min()
        self._values_mean = self._val_series.mean()
        self._values_std = self._val_series.std()
        self._values_md5sum = NumpyUtil.md5sum(new_vals)

        # Flag the CatalogField instance as 'loaded in memory' to avoid reading data from HDF5 study file in the future
        self._hsp_set_lazy_read()

    @property
    def field_values_md5sum(self):
        return self._values_md5sum

    @property
    def field_value_stats(self):
        """Returns (min., max., mean, std) tuple for this field value array"""
        return self._values_min, self._values_max, self._values_mean, self._values_std

    @property
    def nobjects(self):
        """Returns the number of objects in this catalog field => size of the field value 1D array"""
        return self._nobj

    def to_pandas(self):
        """
        Convert a CatalogField into a :class:`pandas.Series` object
        """
        return pd.Series(data=self.field_values, name=self.object_property.display_name, index=range(1, self._nobj+1))

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a CatalogField object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the CatalogField into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(CatalogField, self)._hsp_write(h5group, **kwargs)

        # Write object property UUID
        self._hsp_write_attribute(h5group, ('object_property_uid', self._obj_property.uid), **kwargs)

        # Write catalog field values + stats attributes
        values_attribute_name = "_val_series"  # => self._val_series
        write_values = self._hsp_write_dataset(h5group, ("field_values", values_attribute_name),
                                               md5sum_params=("field_values_md5sum", self._values_md5sum), **kwargs)

        self._hsp_write_attribute(h5group, ('nobjects', self._nobj), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_min', self._values_min), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_max', self._values_max), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_mean', self._values_mean), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_std', self._values_std), **kwargs)

        if write_values:
            self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a CatalogField object from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        catalog: ``CatalogField``
            Read CatalogField instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(CatalogField, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Try to read/find protocol
        try:
            objprop_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "object_property_uid", "object property UUID",
                                                            raise_error_if_not_found=True))

            # Search for already instantiated object property in dependency object dictionary
            if dependency_objdict is None or ObjectProperty.__name__ not in dependency_objdict:
                err_msg = "Cannot find any object property already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Find protocol according to its UUID
            objprop_dict = dependency_objdict[ObjectProperty.__name__]
            if objprop_uid not in objprop_dict:
                err_msg = "Cannot find object property with uid {uid:s}.".format(uid=str(objprop_uid))
                log.error(err_msg)
                raise IOError(err_msg)

            obj_prop = objprop_dict[objprop_uid]
        except IOError:  # Protocol UUID not found in Catalog field
            raise

        # Create catalog field object
        cf = cls(uid=uid, obj_prop=obj_prop, hdf5_init=True)

        # Read field value array MD5 sum + stats attributes
        cf._values_md5sum = cls._hsp_read_attribute(h5group, "field_values_md5sum", "catalog field value array md5sum",
                                                    raise_error_if_not_found=True)
        cf._nobj = cls._hsp_read_attribute(h5group, "nobjects", "number of objects",
                                           raise_error_if_not_found=True)
        cf._values_min = cls._hsp_read_attribute(h5group, "field_value_min", "field min. value",
                                                 raise_error_if_not_found=True)
        cf._values_max = cls._hsp_read_attribute(h5group, "field_value_max", "field max. value",
                                                 raise_error_if_not_found=True)
        cf._values_mean = cls._hsp_read_attribute(h5group, "field_value_mean", "field mean. value",
                                                  raise_error_if_not_found=True)
        cf._values_std = cls._hsp_read_attribute(h5group, "field_value_std", "field std. value",
                                                 raise_error_if_not_found=True)

        # Set HDF5 group/file info for lazy I/O
        cf._hsp_set_lazy_source(h5group)

        return cf

    def _hsp_lazy_read_data(self, h5group):
        """
        Lazy read method to load field values from HDF5 file (*.h5)

        Parameters
        ----------
        h5group: `h5py.Group`
        """
        # Read field value array
        self._val_series = self._hsp_read_dataset(h5group, "field_values", "catalog field value array",
                                                  raise_error_if_not_found=True)

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        if self._obj_property.filter_flag in [PropertyFilterFlag.BASIC_FILTER, PropertyFilterFlag.ADVANCED_FILTER] and\
                self._obj_property.datatype not in [DataType.REAL, DataType.INTGER]:
            log.warning("Can only filter numerical fields.")

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{pname:s}' catalog field".format(pname=self.property_name)


class Catalog(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Result object catalog class (Simulation data model)

    Parameters
    ----------
    target_object: :class:`~astrophysix.simdm.catalogs.targobj.TargetObject`
        catalog object type (mandatory)
    name: :obj:`string`
        catalog name (mandatory)
    description: :obj:`string`
        catalog description
    """
    def __init__(self, *args, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self._name = ""
        self._description = ""
        self._fields = ObjectList(CatalogField, "property_name")
        self._fields.add_validity_check_method(self._does_field_have_same_number_of_items)
        self._fields.add_validity_check_method(self._does_field_property_is_target_obj_prop)
        self._datafiles = ObjectList(Datafile, "name")
        self._targobj = None

        # Object catalog name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        # ------------------------------------- Target object ------------------------------------- #
        if len(args) > 0:
            targobj = args[0]
        elif "target_object" in kwargs:
            targobj = kwargs["target_object"]
        else:
            raise AttributeError("Undefined target object for {cat!s}.".format(cat=self))

        if not isinstance(targobj, TargetObject):
            err_msg = "Catalog 'target_object' attribute is not a valid TargetObject instance."
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._targobj = targobj

        # Add deletion handler to the target object's property list
        targobj.object_properties.add_deletion_handler(self._can_delete_object_property)
        # ----------------------------------------------------------------------------------------- #

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        Catalog comparison method

        other: :class:`~astrophysix.simdm.catalogs.catalog.Catalog`
            Other catalog instance to compare to
        """
        if not super(Catalog, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        # Compare target object
        if self._targobj != other.target_object:
            return False

        #  Compare datafiles
        if self._datafiles != other.datafiles:
            return False

        if self._description != other.description:
            return False

        # Compare catalog fields
        if self._fields != other.catalog_fields:
            return False

        return True

    @property
    def name(self):
        """Catalog name"""
        return self._name

    @name.setter
    def name(self, new_cat_name):
        try:
            self._name = Stringifiable.cast_string(new_cat_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def datafiles(self):
        """Catalog :class:`~astrophysix.simdm.datafiles.Datafile` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._datafiles

    @property
    def catalog_fields(self):
        """Catalog :class:`~astrophysix.simdm.catalogs.catalog.CatalogField` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._fields

    @property
    def nobjects(self):
        """Returns the total number of objects in this catalog"""
        if len(self._fields) == 0:
            return 0
        return self._fields[0].nobjects

    @property
    def target_object(self):
        """Catalog associated :class:`~astrophysix.simdm.catalogs.targobj.TargetObject`."""
        return self._targobj

    @property
    def description(self):
        """Catalog description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_delete_object_property(self, obj_prop):
        """
        Checks if a target object property is not linked to any catalog field and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        obj_prop: ``:class:~astrophysix.simdm.catalogs.targobj.ObjectProperty``
            target object property about to be deleted

        Returns
        -------
        o: str or None
        """
        # Checks that a given ObjectProperty instance is not associated to any field of this catalog
        for f in self._fields:
            if f.object_property is obj_prop:  # Reference identity, not equality ??? Should work
                return "{s!s} {field!s}".format(s=self, field=f)
        return None

    def _does_field_have_same_number_of_items(self, cat_field):
        """
        CatalogField addition validity check nethod. Verifies that the added field has the same number of items in it
        then other catalog fields, if there is any. Raises an AttributeError in case number of items differ.

        Parameters
        ----------
        cat_field: ``CatalogField``
            new catalog field to add to the Catalog
        """
        if self.nobjects == 0:  # No field yet in catalog
            return

        if cat_field.nobjects != self.nobjects:  # Number of catalog items differ => error
            err_msg = "Cannot add a catalog field with {n:d} item values in a catalog containing {cn:d} " \
                      "items.".format(n=cat_field.nobjects, cn=self.nobjects)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def _does_field_property_is_target_obj_prop(self, cat_field):
        """
        CatalogField addition validity check nethod. Verifies that the added field property is one of the catalog's
        target object property. Otherwise raises an AttributeError.

        Parameters
        ----------
        cat_field: ``CatalogField``
            new catalog field to add to the Catalog
        """
        if cat_field.object_property not in self._targobj.object_properties:
            err_msg = "Cannot add catalog field. {p!s} is not a property of " \
                      "{tobj!s}.".format(tobj=self._targobj, p=cat_field.object_property)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def to_pandas(self):
        """
        Convert a Catalog into a Pandas Dataframe object

        Returns
        -------
        df: pandas.DataFrame
            pandas DataFrame containing the catalog data
        """
        series_dict = {}
        for cat_field in self._fields:
            s = cat_field.to_pandas()
            series_dict[s.name] = s
        return pd.DataFrame(data=series_dict)

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Catalog object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Catalog into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Catalog, self)._hsp_write(h5group, **kwargs)

        # Write catalog name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write catalog description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write datafiles, if any defined
        self._hsp_write_object_list(h5group, "DATAFILES", self._datafiles, "datafile_", **kwargs)

        # Write target object
        if kwargs.get("from_project", False):  # Write target object UUID
            self._hsp_write_attribute(h5group, ('targob_uid', self._targobj.uid), **kwargs)
        else:  # Write complete target object description (full serialization)
            self._hsp_write_object(h5group, "TARGET_OBJECT", self._targobj, **kwargs)

        # Write catalog fields, if any defined
        self._hsp_write_object_list(h5group, "CATALOG_FIELDS", self._fields, "cat_field_", **kwargs)

        self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Catalog object from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        catalog: ``Catalog``
            Read Catalog instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Catalog, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Try to read/find protocol
        try:
            targobj_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "targob_uid", "target object UUID",
                                                            raise_error_if_not_found=True))

            # Search for already instantiated target object in dependency object dictionary
            if dependency_objdict is None:
                err_msg = "Cannot find any target object already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Get dictionary of target object instances of the corresponding class :
            if TargetObject.__name__ not in dependency_objdict:
                err_msg = "Cannot find any {cname:s} instance.".format(cname=TargetObject.__name__)
                log.error(err_msg)
                raise IOError(err_msg)

            # Find target object according to its UUID
            tobj_dict = dependency_objdict[TargetObject.__name__]
            if targobj_uid not in tobj_dict:
                err_msg = "Cannot find {cname:s} instance with uid {uid:s}.".format(cname=TargetObject.__name__,
                                                                                    uid=str(uid))
                log.error(err_msg)
                raise IOError(err_msg)

            tobj = tobj_dict[targobj_uid]
        except IOError:  # Target Object UUID not found in GenericResult
            # Read target object info from "TARGET_OBJECT" subgroup
            tobj = TargetObject._hsp_read_object(h5group, "TARGET_OBJECT", "catalog target object",
                                                 dependency_objdict=dependency_objdict)

        # Read catalog name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Create catalog object
        catalog = cls(uid=uid, target_object=tobj, name=name)

        # Build datafile list and add each datafile into catalog
        for df in Datafile._hsp_read_object_list(h5group, "DATAFILES", "datafile_", "catalog datafile",
                                                 dependency_objdict=dependency_objdict):
            catalog.datafiles.add(df)

        # Build catalog field list and add each field into catalog
        for field in CatalogField._hsp_read_object_list(h5group, "CATALOG_FIELDS", "cat_field_", "catalog field",
                                                        dependency_objdict=dependency_objdict):
            catalog.catalog_fields.add(field)

        # Read catalog description, if defined
        cat_descr = cls._hsp_read_attribute(h5group, 'description', "catalog description",
                                            raise_error_if_not_found=False)
        if cat_descr is not None:
            catalog.description = cat_descr

        return catalog

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check target object name
        if len(self._name) > 64:
            log.warning("{c!s} name is too long for Galactica (max. 64 characters).".format(c=self))

        # Check that the catalog contain some object
        if self.nobjects == 0:
            log.warning("{c!s} does not contain any object.".format(c=self))

        # Check catalog field and datafile list validity
        self._fields.galactica_validity_check(**kwargs)
        self._datafiles.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{cat_name:s}' catalog".format(cat_name=self._name)


__all__ = ["Catalog", "CatalogField"]
