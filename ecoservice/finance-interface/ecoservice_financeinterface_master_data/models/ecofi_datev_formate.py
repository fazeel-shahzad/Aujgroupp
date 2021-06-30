# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

import base64
import csv
import io

from odoo import _, fields, models, modules
from odoo.exceptions import UserError


class EcofiDatevFormate(models.Model):
    _name = 'ecofi.datev.formate'
    _description = 'Configuration for Datev master data exports'

    # region Fields

    name = fields.Char(required=True)
    mako_help = fields.Text(readonly=True)
    csv_spalten = fields.One2many(
        comodel_name='ecofi.datev.spalten',
        inverse_name='import_id',
        string='Datev-Spalten',
    )
    datev_domain = fields.Char(
        string='Domain',
        required=True,
    )
    datev_type = fields.Selection(
        selection=[],
        string='Export type',
    )

    # endregion

    def get_csv_headline(self, columns):
        """
        Get the CSV lines for export.
        """

        if 'export_all' not in self.env.context:
            columns = columns.filtered('mako')
        return columns.mapped('feldname')

    def get_csv_columns(self, columns):
        """
        Get the CSV lines for export.
        """

        if 'export_all' in self.env.context:
            return columns
        return columns.filtered('mako')

    def _get_account_type(self, account_type):
        """
        Use to add custom interface to selection of export formats (by inheritance).
        """
        return account_type

    def convert_value(self, column_type, value):
        """
        Convert given Value into the Datev Format.
        """
        casting_method = self._get_casting_dict().get(
            column_type,
            (self.__cast_not_specified, _('unspecified')),
        )
        res = {
            'log': '',
            'value': False,
        }
        if not value:
            res['value'] = ''
        else:
            try:
                value = casting_method[0](value)
                res['value'] = str(value)
            # noqa: B902 as unknown now what the initial purpose was
            # TODO: refactor with specific exception
            except Exception:  # noqa: B902
                res['log'] = _(
                    'Value {value} could not be converted into {message}!'
                ).format(
                    value=value,
                    message=casting_method[1],
                )
        return res

    def _get_casting_dict(self):
        return {
            'Konto': (str, _('text')),
            'Zahl': (int, _('an integer')),
            'Text': (str, _('text')),
            'Datum': (self.__cast_to_date, _('a date')),
            'Betrag': (self.__cast_to_number, _('a decimal')),
        }

    @staticmethod
    def __cast_to_date(value):
        return '{dd}{mm}{yyyy}'.format(dd=value[8:10], mm=value[5:7], yyyy=value[:4])

    @staticmethod
    def __cast_to_number(value):
        return '{}'.format(value).replace('.', ',')

    @staticmethod
    def __cast_not_specified(value):
        raise UserError()

    def generate_export_csv(self, export, ecofi_csv):
        """Fill the CSV-File with DATA."""
        return {
            'log': '',
        }

    def generate_export(self):
        """Generate the CSV File called by the Wizard."""
        buf = io.StringIO()
        ecofi_csv = csv.writer(buf, delimiter=',', quotechar='"')

        for export in self:
            export_info = self.generate_export_csv(
                export=export,
                ecofi_csv=ecofi_csv,
            )

        return {
            'file': base64.encodebytes(str.encode(
                buf.getvalue(),
                encoding='cp1252',
                errors='ignore',
            )),
            'log': export_info['log']
        }

    @staticmethod
    def generate_csv_header_definition():
        """CSV-Template Header Definition Dictionary Definition."""
        key_header_mapping = {
            'mako': 'Mako',
            'datevid': 'Nr.',
            'feldname': 'Feldname',
            'typ': 'Typ',
            'nks': 'NKS',
            'laenge': 'Länge',
            'maxlaenge': 'Max. Länge',
            'beschreibung': 'Beschreibung',
            'mussfeld': 'Muss-Feld',
        }
        return {
            key: {
                'header': value,
                'fieldnumber': False,
            }
            for key, value in key_header_mapping.items()
        }

    def getfields_defaults(self, template):
        """Fill the defaults like template.csv etc."""
        return {}

    def getfields_fromcsv(self):
        """Import the CSV Template for the Export Configurations."""
        for template in self.filtered('datev_type'):
            field_defaults = self.getfields_defaults(template)

            template.write({
                'mako_help': field_defaults.get('mako_help', '')
            })

            if field_defaults.get('csv_template'):
                module = modules.get_module_resource(
                    field_defaults['module'],
                    field_defaults['csv_template'],
                )
                with open(module, 'r', encoding='utf-8') as csv_file:
                    # defaults to delimiter=',' and quotechar='"'
                    importliste = csv.reader(csv_file)
                    importattrs = self.generate_csv_header_definition()
                    for line_count, line in enumerate(importliste):
                        if line_count == 0:
                            for field_count, value in enumerate(line):
                                for attr in importattrs.keys():
                                    if importattrs[attr]['header'] == value:
                                        importattrs[attr]['fieldnumber'] = field_count  # noqa: E501
                            self._validate_header(importattrs)
                        else:
                            column = self.csv_spalten.search([
                                ('import_id', '=', template.id),
                                ('datevid', '=', int(line[importattrs['datevid']['fieldnumber']])),  # noqa: E501
                            ])

                            required = importattrs['mussfeld']['fieldnumber']
                            line[required] = line[required] == 'Ja'

                            values = {
                                'import_id': template.id,
                            }

                            for attr in importattrs.keys():
                                key = importattrs[attr]['fieldnumber']
                                values[attr] = line[key]

                            if len(column) == 1:
                                column.write(values)
                            else:
                                self.csv_spalten.create(values)
        return True

    def _validate_header(self, importattrs):
        missing_header = [
            attr
            for attr in importattrs.keys()
            # 'not' does not work as fieldnumber for first entry is 0 (falsy)
            if importattrs[attr]['fieldnumber'] is False
        ]
        if missing_header:
            header_values = ', '.join([
                importattrs[attr]['header']
                for attr in missing_header
            ])
            raise UserError(_(
                'Importformat not correct, Headervalues "{header}" not found in the csv!'  # noqa: E501
            ).format(
                header=header_values,
            ))
