*******************
 The settings file
*******************

The file ``settings.yaml`` defines the properties of a collection.

It is a yaml file with a dict of properties and their values.

``name``:
   the human readable name of the collection.
``lang``:
   the language of the collection; valid values are listed in the
   `xapian stemmer`_ documentation and are usually either the English
   name or the two letter ISO639 code of a language.
``entry_label``:
   a jinja2 template used to show an entry in the interface; beside the
   entry fields two useful variables are ``eid`` for the full entry ID
   and ``short_id`` for the short version.
``default_sort``:
   a list of field names (possibly prefixed by + or -) that are used by
   default to sort results of searches in the collection.
   The fields must be marked as sortable in their definition, see below.
``fields``:
   The list of fields used by the collection, as described below.

.. _`xapian stemmer`: https://xapian.org/docs/apidoc/html/classXapian_1_1Stem.html

Field definitions
=================

``name``:
   a name for the field (computer readable: keeping it lowercase
   alphabetic ascii is probably safer).
``type``:
   the type of the field: valid fields are listed in
   :doc:`/reference/lesana.types` (see the ``name`` property for each
   field)
``index``:
   whether this field should be indexed: valid values are ``free`` for
   fields that should be available in the free text search and ``field``
   for fields that should only be available by specifying the field name
   in the search.
``sortable``:
   boolean; whether this field is sortable. Sortable fields enable
   sorting the results and search by ranges, but having too many
   sortable fields make the search more resurce intensive.
``help``:
   a description for the field; this is e.g. added to new entries as a
   comment.
``default``:
   the default value to use when creating an entry.
``prefix``:
   the optional term prefix used inside xapian: if you don't know what
   this means you should avoid using this, otherwise see `Term
   Prefixes`_ on the xapian documentation for details.

.. _`Term Prefixes`: https://xapian.org/docs/omega/termprefixes.html

Some field types may add other custom properties.

``list`` properties
-------------------

``list``:
   the type of the entries in the list; note that neither lists of non
   uniform values nor lists of lists are supported (if you need those
   you can use the ``yaml`` generic type, or write your own derivative
   with an additional type).

``integer`` properties
----------------------

``auto``:
   automatic manipulation of the field contents.

   The value of ``increment`` will autoincrement the value at every
   update.

   The reference client will run this update before editing an entry,
   allowing further changes from the user; a command line user can then
   decide to abort this change through the usual git commands.

   Other clients may decide to use a different workflow.

``increment``:
   the amount by which an ``auto: increment`` field is incremented
   (negative values are of course allowed).

``date`` and ``datetime`` properties
------------------------------------

``auto``:
   automatic manipulation of the field contents.

   The following values are supported.

   ``creation``
      autofill the field at creation time with the current UTC time
      (``datetime``) or local zone day (``date``).
   ``update``
      autofill the field when it is updated with the current UTC time
      (``datetime``) or local zone day (``date``).

      The reference client will run this update before editing an entry,
      allowing further changes from the user; a command line user can
      then decide to abort this change through the usual git commands.

      Other clients may decide to use a different workflow.

