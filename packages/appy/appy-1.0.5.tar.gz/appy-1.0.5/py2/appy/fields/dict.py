# Copyright (C) 2007-2021 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------
from appy import Object
from appy.px import Px
from appy.fields.list import List
from appy.gen.layout import Table

# ------------------------------------------------------------------------------
class SepRow:
    '''Represents a custom row that is a separator but does not represent
       data.'''
    def __init__(self, text, cellCss=None, rowCss=None):
        self.text = text
        # An optional CSS class to apply to the cell containing p_text
        self.cellCss = cellCss
        # An optional CSS class to apply to the row contaning this cell
        self.rowCss = rowCss

    def get(self, field):
        '''Produces the chunk of XHTML code representing this row'''
        rowCss = self.rowCss and (' class="%s"' % self.rowCss) or ''
        cellCss = self.cellCss and (' class="%s"' % self.cellCss) or ''
        return '<tr valign="top"%s><td colspan="%s"%s>%s</td></tr>' % \
               (rowCss, len(field.fields) + 1, cellCss, self.text)

# ------------------------------------------------------------------------------
class Dict(List):
    '''A Dict value has the form ~{s_key: Object}~. Keys are fixed and given by
       a method specified in parameter "keys". Values are Object instances,
       whose attributes are determined by parameter "fields" that, similarly to
       the List field, determines sub-data for every entry in the dict. This
       field is build on top of the List field.'''
    SepRow = SepRow

    # PX for rendering a single row
    pxRow = Px('''
     <!-- Render a separatation row -->
     <x if="not rowId">::text.get(field)</x>
     <tr if="rowId" valign="top" class=":loop.rowId.odd and 'even' or 'odd'">
      <x>:field.pxFirstCell</x>
      <td class="discreet">::text</td>
      <td for="subName, field in subFields" if="field" align="center"
          var2="fieldName='%s*%s' % (field.name, rowId)">:field.pxRender</td>
     </tr>''')

    # PX for rendering the dict (shared between pxView and pxEdit)
    pxTable = Px('''
     <table var="isEdit=layoutType == 'edit'" if="isEdit or value"
            id=":'list_%s' % name" class="grid" width=":field.width"
            var2="keys=field.keys(obj);
                  subFields=field.getSubFields(zobj, layoutType)">
      <!-- Header -->
      <tr valign="bottom">
       <th width=":field.widths[0]"></th>
       <th for="subName, sub in subFields" if="sub"
           width=":field.widths[loop.subName.nb + 1]">::_(sub.labelId)</th>
      </tr>
      <!-- Rows of data -->
      <x for="rowId, text in keys">:field.pxRow</x>
     </table>''')

    def __init__(self, keys, fields, validator=None, multiplicity=(0,1),
      default=None, defaultOnEdit=None, show=True, page='main', group=None,
      layouts=None, move=0, specificReadPermission=False,
      specificWritePermission=False, width='', height=None, maxChars=None,
      colspan=1, master=None, masterValue=None, focus=False, historized=False,
      mapping=None, generateLabel=None, label=None,
      subLayouts=Table('frv', width=None), widths=None, view=None, cell=None,
      edit=None, xml=None, translations=None):
        List.__init__(self, fields, validator, multiplicity, default,
          defaultOnEdit, show, page, group, layouts, move,
          specificReadPermission, specificWritePermission, width, height,
          maxChars, colspan, master, masterValue, focus, historized, mapping,
          generateLabel, label, subLayouts, widths, view, cell, edit, xml,
          translations)
        # Method in "keys" must return a list of tuples (key, title): "key"
        # determines the key that will be used to store the entry in the
        # database, while "title" will get the text that will be shown in the ui
        # while encoding/viewing this entry.

        # WARNING: a key must be a string, cannot contain digits only and
        # cannot contain char "*". A key is typically an object ID.

        # For a nice rendering of your dict, some of the tuples returned by
        # method "keys" can be "separator rows". The tuple representing such a
        # row must have the form (None, sepRow). "None" indicates that this is
        # not a row of data; "sepRow" must be a SepRow instance (see hereabove)
        # that will determine content and style for the separator row.
        self.keys = keys

    def computeWidths(self, widths):
        '''Set given p_widths or compute default ones if not given'''
        if not widths:
            self.widths = [''] * (len(self.fields) + 1)
        else:
            self.widths = widths

    def getStorableValue(self, obj, value, complete=False):
        '''Gets p_value in a form that can be stored in the database'''
        from persistent.mapping import PersistentMapping
        res = PersistentMapping()
        for k, v in value.iteritems():
            res[k] = self.getStorableRowValue(obj, v)
        return res

    def remove(self, obj, key):
        '''Remove entry corresponding to p_key on the value stored on p_obj'''
        val = getattr(obj.o, self.name, None)
        if not val: return
        if key not in val: return
        del val[key]
        setattr(obj.o, self.name, val)

    def store(self, obj, value, overwrite=False):
        '''Stores the p_value (produced by m_getStorableValue) on p_obj. If some
           entry from p_value already exists in the DB value, it is updated,
           not overwritten.'''
        obj = obj.o
        if not self.persist: return
        dbValue = getattr(obj.aq_base, self.name, None)
        if not dbValue or overwrite:
            setattr(obj, self.name, value)
        else:
            # Update the DB value with p_value
            if not value: return
            for key, data in value.iteritems():
                if key not in dbValue:
                    dbValue[key] = data
                else:
                    dbValue[key].update(data)
                    # Force the mapping to take the change into account
                    dbValue[key] = dbValue[key]
            setattr(obj, self.name, dbValue)

    def subValidate(self, obj, value, errors):
        '''Validates inner fields'''
        for key, row in value.iteritems():
            for name, subField in self.fields:
                message = subField.validate(obj, getattr(row, name, None))
                if message:
                    setattr(errors, '%s*%s' % (subField.name, key), message)
# ------------------------------------------------------------------------------
