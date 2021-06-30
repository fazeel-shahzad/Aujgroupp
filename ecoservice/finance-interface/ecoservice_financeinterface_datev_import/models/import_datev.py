# -*- coding: utf-8 -*-
# Part of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

import base64
import csv
import sys
import traceback
import io
from datetime import date, datetime
from decimal import Decimal
from functools import reduce

from odoo import _, api, exceptions, fields, models


class ImportDatev(models.Model):
    """
    The class import.datev manages the reimport of datev buchungsstapel (account.moves)
    """
    _name = 'import.datev'

    name = fields.Char(string='Name', readonly=True, default=lambda self: self.env['ir.sequence'].get('datev.import.sequence') or '-')
    description = fields.Char(string='Description', required=True)
    company_id = fields.Many2one(comodel_name='res.company', string='Company', required=True)
    datev_ascii_file = fields.Binary(string='DATEV ASCII File')
    datev_ascii_filename = fields.Char(string='DATEV ASCII Filename')
    journal_id = fields.Many2one(comodel_name='account.journal', string='Journal', required=True)
    one_move = fields.Boolean(string='In one move?')
    start_date = fields.Date(string='Start Date', required=True, default=lambda *a: fields.Date.today())
    end_date = fields.Date(string='End Date', required=True, default=lambda *a: fields.Date.today())
    log_line = fields.One2many(comodel_name='import.datev.log', inverse_name='parent_id', string='Log')
    account_moves = fields.One2many(comodel_name='account.move', inverse_name='import_datev', string='Account Moves')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('error', 'Error'),
            ('imported', 'Imported'),
            ('booking_error', 'Booking Error'),
            ('booked', 'Booked')
        ],
        string='Status', select=True, readonly=True, default='draft')

    # Extended configuration
    config_delimiter = fields.Char(string='Delimiter', size=1, default=';')
    config_quotechar = fields.Selection(string='Quote', selection=[('"', '"'), ("'", "'")], default='"')
    config_extended_datev_header = fields.Boolean(
        string='Extended Datev Header',
        default=True,
        help="The first line of a standard export from DATEV contains meta information."
             " If this is the case the line headers needed for the import are in the"
             " second line and this option needs to be checked."
    )
    config_encoding = fields.Selection(
        string='Encoding',
        selection=[
            ('utf_8', 'UTF-8'),
            ('latin_1', 'ISO-8859-1'),
            ('iso8859_15', 'ISO-8859-15'),
            ('cp1252', 'Windows-1252'),
        ],
        default='cp1252',
    )

    def _lookup_erpvalue(self, field_config, value):
        """ Method to get the ERP ID for the Object and the given Value

        :param field_config: Dictionary of the field containing the erpobject and the erpfield
        :param value: Domain Search Value
        """
        value = False

        try:
            if field_config['erpfield'] == 'l10n_de_datev_code':
                if value in ['SD', '40']:
                    return value
                else:
                    try:
                        value = int(value)
                    except:
                        return False
            args = 'domain' in field_config and field_config['domain'] or []
            args.append((field_config['erpfield'], '=', value))
            value = self.env[field_config['erpobject']].search(args=args, limit=1)
        except:
            return False

        return value or False

    def convert_value(self, importcsv, import_config, import_struct, errorlist, start_date, end_date):
        """ Tries to convert given Value into the Datev Format"""
        data_list = []
        input_file = io.StringIO(importcsv.decode(encoding=import_config['encoding']))

        if import_config['extended_header']:
            input_file.readline()

        importliste = csv.DictReader(input_file, delimiter=import_config['delimiter'], quotechar=import_config['quotechar'])

        for linecounter, line in enumerate(importliste, start=1):
            spaltenvalues = {}

            for key in import_struct.keys():
                val = False
                csv_names = import_struct[key]['csv_name']
                try:
                    for csv_name in csv_names:
                        if csv_name in line and line[csv_name]:
                            if import_struct[key]['type'] == 'string':
                                val = line[csv_name]
                            elif import_struct[key]['type'] == 'integer':
                                val = int(line[csv_name])
                            elif import_struct[key]['type'] == 'decimal':
                                decimalvalue = line[csv_name]
                                if import_struct[key]['decimalformat'][0]:
                                    decimalvalue = decimalvalue.replace(import_struct[key]['decimalformat'][0], '')
                                val = Decimal(decimalvalue.replace(import_struct[key]['decimalformat'][1], '.'))
                            elif import_struct[key]['type'] == 'date':
                                val = datetime.strptime(line[csv_name], import_struct[key]['dateformat']).date()
                                val = val.replace(year=date.today().year)

                                if start_date > val < end_date:
                                    errorlist.append({
                                        'line': linecounter,
                                        'name': _('Date is not in the selected date range!'),
                                        'beschreibung': _('Date {date} in line {name} is not in the selected date range!').format(
                                            date=val,
                                            name=import_struct[key]['csv_name']
                                        )
                                    })
                                    val = False
                            else:
                                errorlist.append({
                                    'line': linecounter,
                                    'name': _('Attribute type could not be resolved'),
                                    'beschreibung': _('Attribute type {type} could not be resolved!').format(
                                        type=import_struct[key]['type']
                                    )
                                })
                except:
                    errorlist.append({
                        'line': linecounter,
                        'name': _('Attribute could not be converted!'),
                        'beschreibung': _(u"Attribute {name} in line {counter} could not be converted to type '{type}'!").format(
                            name=import_struct[key]['csv_name'], counter=linecounter,
                            type=import_struct[key]['type']
                        )
                    })
                if val:
                    spaltenvalues[key] = val
            data_list.append(spaltenvalues)
        return data_list, errorlist

    def unlink(self):
        """ Import can only be unlinked if State is draft
        """
        if any([s != 'draft' for s in self.mapped('state')]):
            raise exceptions.Warning(_('Import can only be deleted in state draft!'))
        return super(ImportDatev, self).unlink()

    def reset_import(self):
        """ Method to reset the import
        #. Unreconcile all reconciled imported Moves
        #. Cancel all imported moves not in state draft
        #. Delete all imported moves
        #. Delete all Importloglines
        #. Set Import state to draft
        """
        for datev_import in self:
            try:
                datev_import.account_moves.mapped('line_ids').filtered('reconciled').remove_move_reconcile()
                datev_import.account_moves.filtered(lambda r: r.state != 'draft').button_cancel()
                datev_import.account_moves.with_context(force_delete=True).unlink()
                datev_import.log_line.unlink()
                datev_import.write({'state': 'draft'})
            except:
                self.log_line.create({
                    'parent_id': datev_import.id,
                    'name': _('Odoo ERROR: {error}').format(error=traceback.format_exc()),
                    'state': 'error',
                })
        return True

    def search_partner(self, konto):
        """ Get the partner for the specified account

        :param konto: ID of the account
        """
        sql = """SELECT id from res_partner where id in
                    (SELECT split_part(res_id, ',', 2)::integer from ir_property
                    WHERE res_id like 'res.partner%' and value_reference = 'account.account,{account_id}') LIMIT 1;""".format(account_id=str(konto))
        self.env.cr.execute(sql)
        fetch = self.env.cr.fetchone()
        return fetch and int(fetch[0])

    def get_partner(self, line):
        """ Search Partner for the line

        :param line: Move Line
        """
        partner_id = False
        if line['konto_object'].user_type_id.type in ('receivable', 'payable'):
            partner_id = self.search_partner(line['konto_object'].id)
        if not partner_id:
            if line['gegenkonto_object'].user_type_id.type in ('receivable', 'payable'):
                partner_id = self.search_partner(line['gegenkonto_object'].id)
        return partner_id

    def get_import_defaults(self, datev_import):
        """ Default import_config and import_struct
        """
        import_config = {
            'delimiter': str(datev_import.config_delimiter) or ';',
            'quotechar': str(datev_import.config_quotechar) or '"',
            'encoding': datev_import.config_encoding or 'utf_8',
            'extended_header': datev_import.config_extended_datev_header,
            'header_row': 1 + int(datev_import.config_extended_datev_header),
            'journal_id': datev_import.journal_id.id,
            'company_id': datev_import.company_id.id,
            'company_currency_id': datev_import.company_id.currency_id,
            'skonto_account': 499,
            'date': datev_import.start_date
        }
        import_struct = {
            'gegenkonto': {
                'csv_name': ['Gegenkonto (ohne BU-Schlüssel)'],
                'csv_row': False,
                'type': 'string',
                'required': True,
                'erplookup': True,
                'erpobject': 'account.account',
                'erpfield': 'code',
                'domain': [],
                'zfill': 4,
            },
            'konto': {
                'csv_name': ['Konto'],
                'csv_row': False,
                'type': 'string',
                'required': True,
                'erplookup': True,
                'erpobject': 'account.account',
                'erpfield': 'code',
                'domain': [],
                'zfill': 4,
            },
            'wkz': {
                'csv_name': ['WKZ Umsatz'],
                'csv_row': False,
                'type': 'string',
                'required': False,
                'erplookup': True,
                'erpobject': 'res.currency',
                'erpfield': 'name',
            },
            'buschluessel': {
                'csv_name': ['BU-Schlüssel'],
                'csv_row': False,
                'type': 'string',
                'required': False,
                'erplookup': True,
                'erpobject': 'account.tax',
                'erpfield': 'l10n_de_datev_code'
            },
            'belegdatum': {
                'csv_name': ['Belegdatum'],
                'csv_row': False,
                'type': 'date',
                'required': True,
                'dateformat': '%d%m',
            },
            'beleg1': {
                'csv_name': ['Belegfeld 1'],
                'csv_row': False,
                'type': 'string',
                'required': False,
            },
            'beleg2': {
                'csv_name': ['Belegfeld 2'],
                'csv_row': False,
                'type': 'string',
                'required': False,
            },
            'umsatz': {
                'csv_name': ['Umsatz (ohne Soll/Haben-Kz)', 'Umsatz', 'Umsatz (ohne Soll-/Haben-Kennzeichen)'],
                'csv_row': False,
                'type': 'decimal',
                'required': True,
                'decimalformat': ('.', ',')
            },
            'skonto': {
                'csv_name': ['Skonto'],
                'csv_row': False,
                'type': 'decimal',
                'required': False,
                'decimalformat': (False, ',')
            },
            'buchungstext': {
                'csv_name': ['Buchungstext'],
                'csv_row': False,
                'type': 'string',
                'required': False,
                'skipon': ['Gruppensumme', 'Abstimmsumme'],
            },
            'sollhaben': {
                'csv_name': ['Soll/Haben-Kennzeichen', 'Soll-/Haben-Kennzeichen', 'S/H'],
                'csv_row': False,
                'type': 'string',
                'required': True,
                'default': 'S'
            },
        }
        return import_config, import_struct

    def create_account_move(self, datev_import, import_config, line, linecounter, move_id=False, manual=False):
        """ Create the move for the import line

        :param datev_import: Datev Import
        :param import_config: Import Config
        :param line: Move Line
        :param linecounter: Counter of the move line
        """
        partner_id = self.get_partner(line)

        if not move_id:
            ref = ', '.join([x for x in [line.get('beleg1'), line.get('beleg2')] if x])
            move = {
                'import_datev': datev_import.id,
                'name': line['name'],
                'ref': ref,
                'journal_id': datev_import.journal_id.id,
                'company_id': import_config['company_id'],
                'date': line['belegdatum'],
                'ecofi_buchungstext': line.get('buchungstext', ''),
                'ecofi_manual': manual,
                'partner_id': partner_id,
            }
            move_id = self.account_moves.create(move)

        return move_id, partner_id

    def create_move_line_dict(self, move, import_config):
        move_line_dict = {
            'company_id': import_config['company_id'],
            'partner_id': move['partner_id'],
            'credit': str(move['credit']),
            'debit': str(move['debit']),
            'journal_id': import_config.get('journal_id', False),
            'account_id': move['account_id'],
            'date': move['date'],
            'name': move['name'],
            'move_id': move['move_id'],
            'ecofi_account_counterpart': move['ecofi_account_counterpart'],
            'ecofi_tax_id': move.get('ecofi_tax_id', False),
            'amount_currency': move.get('amount_currency', False),
            'currency_id': move.get('currency_id', False),
            'date_maturity': move.get('date_maturity', False),
            'analytic_account_id': False,
            'quantity': 1.0,
            'datev_posting_key': move.get('datev_posting_key', ''),
            'product_id': False,
        }
        return move_line_dict

    def compute_currency(self, move_line, line, import_config):
        cur_obj = self.env['res.currency']
        cur = False
        if type(line['wkz']) == str and line['wkz'] != import_config['company_currency_id'].name:
            context = self.env.context.copy()
            context.update({'date': line['belegdatum'] or fields.Date.today()})
            if 'wkz' in line and line['wkz']:
                cur = self.env['res.currency'].search([('name', '=', line['wkz'])])
            move_line['currency_id'] = cur[0].id if cur and cur[0] else cur
            move_line['amount_currency'] = move_line['debit'] - move_line['credit']
            move_line['debit'] = Decimal(str(cur_obj.with_context(context).compute(float(move_line['debit']), import_config['company_currency_id'])))
            move_line['credit'] = Decimal(str(cur_obj.with_context(context).compute(float(move_line['credit']), import_config['company_currency_id'])))
        return move_line

    def create_main_lines(self, line, thismove, partner_id, import_config, import_struct, move_lines=None):
        """ Create the Main booking Lines

        :param line: Import Line
        :param thismove: MoveID
        :param move_lines: MoveLines
        """
        tax_id = None
        if move_lines is None:
            move_lines = []
        if not line.get('sollhaben'):
            line['sollhaben'] = import_struct['sollhaben']['default']
        if line['sollhaben'].upper() == 'S':
            debit = line.get('umsatz', Decimal('0.0'))
            credit = Decimal('0.0')
        else:
            debit = Decimal('0.0')
            credit = line.get('umsatz', Decimal('0.0'))
        gegenmove = {
            'credit': debit,
            'debit': credit,
            'account_id': line['gegenkonto_object'].id,
            'date': line['belegdatum'],
            'move_id': thismove,
            'name': 'Gegenbuchung',
            'partner_id': partner_id,
            'ecofi_account_counterpart': line['gegenkonto_object'].id,
        }
        mainmove = {
            'credit': credit,
            'debit': debit,
            'account_id': line['konto_object'].id,
            'date': line['belegdatum'],
            'move_id': thismove,
            'name': 'Buchung',
            'partner_id': partner_id,
            'ecofi_account_counterpart': line['gegenkonto_object'].id,
        }
        if line['konto_object'].datev_automatic_account and not line.get('buschluessel'):
            line['buschluessel'] = line['konto_object'].datev_tax_ids[0].l10n_de_datev_code or False
        if line.get('buschluessel') or line.get('konto_object') or line.get('gegenkonto_object'):
            # if not isinstance(line['buschluessel'], int):
            #     # We don't need the correction-key part of the booking key
            #     line['buschluessel'] = line['buschluessel'][-1]
            mainmove, taxmoves, tax_id = self.create_tax_line(mainmove, import_config, line)
            for taxmove in taxmoves:
                move_lines.append(self.compute_currency(taxmove, line, import_config))
        gegenmove = self.compute_currency(gegenmove, line, import_config)
        mainmove = self.compute_currency(mainmove, line, import_config)
        move_lines.append(self.create_move_line_dict(gegenmove, import_config))
        move_lines.append(self.create_move_line_dict(mainmove, import_config))

        self.add_tax_info_to_lines(move_lines, tax_id)
        return move_lines

    def add_tax_info_to_lines(self, move_lines, tax_id):
        if tax_id:
            user_type_list = self.env.ref('account.data_account_type_receivable') + self.env.ref('account.data_account_type_payable')
            accounts = self.env['account.account'].search([('user_type_id', 'in', user_type_list.ids)])
            taxes = self.env['account.tax'].search([])
            for tax in taxes:
                accounts = accounts | tax.invoice_repartition_line_ids.account_id
                accounts = accounts | tax.refund_repartition_line_ids.account_id
            no_tax_on_this_account_ids = accounts.ids
            for move_line in move_lines:
                account_id = move_line.get('account_id', False)
                if account_id and account_id not in no_tax_on_this_account_ids:
                    move_line.update({
                        'ecofi_tax_id': tax_id.id,
                        'tax_ids': [(6, 0, [tax_id.id])],
                    })

    def create_tax_line(self, mainmove, import_config, line):
        taxmoves = []
        tax_id = None

        user_type_list = self.env.ref('account.data_account_type_receivable') + self.env.ref('account.data_account_type_payable')

        # Check account to Receivable or Payable
        konto_obj = line.get('konto_object', False)
        gegenkonto_obj = line.get('gegenkonto_object', False)
        if konto_obj and gegenkonto_obj:
            konto_obj_is_rec_or_pay = konto_obj.user_type_id in user_type_list
            gegenkonto_obj_is_rec_or_pay = gegenkonto_obj.user_type_id in user_type_list
            # check konto or gegenkonto is not receivable or payable
            if not konto_obj_is_rec_or_pay or not gegenkonto_obj_is_rec_or_pay:
                if konto_obj.datev_automatic_account and not tax_id:  # check konto automatic
                    tax_id = konto_obj.datev_tax_ids and konto_obj.datev_tax_ids[0] or False
                elif gegenkonto_obj.datev_automatic_account and not tax_id:  # check gegenkonto automatic
                    tax_id = gegenkonto_obj.datev_tax_ids and gegenkonto_obj.datev_tax_ids[0] or False
                elif line.get('buschluessel'):
                    if line['buschluessel'] in ['40', 'SD']:
                        mainmove['ecofi_bu'] = line['buschluessel']
                        mainmove['ecofi_tax_id'] = konto_obj.datev_tax_ids and konto_obj.datev_tax_ids[0].id or False
                        tax_id = None
                    else:
                        tax_id = self.env['account.tax'].search([('l10n_de_datev_code', '=', int(line['buschluessel']))], limit=1)

        total = float(mainmove['debit'] + mainmove['credit'])

        if tax_id:
            # We need a tax object that has the right amount and the right calculation method
            # And because we do not want to create a new tax in the database we just create a
            # temporary tax object with the data of the tax with the corresponding booking key
            values = tax_id.copy_data()[0]
            values['price_include'] = True
            tmp_tax_id = tax_id.new(values)

            for tax in tmp_tax_id.compute_all(total).get('taxes'):
                if mainmove['credit'] == Decimal('0.00'):
                    tax_credit = 0.00
                    tax_debit = tax['amount']
                else:
                    tax_credit = tax['amount']
                    tax_debit = 0.00
                data = {
                    'move_id': mainmove['move_id'],
                    'name': ' '.join([x for x in [mainmove['name'], tax['name']] if x]),
                    'date': mainmove['date'],
                    'partner_id': mainmove['partner_id'],
                    'tax_ids': False,
                    'account_id': tax['account_id'],
                    'credit': tax_credit,
                    'debit': tax_debit,
                    'ecofi_account_counterpart': line['gegenkonto_object'].id,
                }
                mainmove['credit'] -= Decimal(str(data['credit']))
                mainmove['debit'] -= Decimal(str(data['debit']))
                taxmoves.append(data)
        return mainmove, taxmoves, tax_id

    def do_import(self):
        """ Method to Start the Import of the Datev ASCII File Containing the Datev Moves """
        errorlist = []
        for datev_import in self:
            import_config, import_struct = self.get_import_defaults(datev_import)
            self.reset_import()
            self.log_line.create({
                'parent_id': datev_import.id,
                'name': _('Import started!'),
                'state': 'info',
            })
            if datev_import.datev_ascii_file:
                importcsv = base64.decodebytes(datev_import.datev_ascii_file)
                vorlauf, errorlist = self.convert_value(importcsv, import_config, import_struct, errorlist,
                                                        datev_import.start_date, datev_import.end_date)
                if len(errorlist) == 0:
                    linecounter = 0
                    thismove = False
                    for line in vorlauf:
                        if 'buchungstext' in line and line['buchungstext'] in import_struct['buchungstext']['skipon']:
                            continue
                        linecounter += 1
                        line['gegenkonto_object'] = self.env['account.account'].search([
                            ('code', '=', '{:04}'.format(int(line['gegenkonto']))),
                            ('company_id', '=', self.env.user.company_id.id)
                        ])
                        line['konto_object'] = self.env['account.account'].search([
                            ('code', '=', '{:04}'.format(int(line['konto']))),
                            ('company_id', '=', self.env.user.company_id.id)
                        ])
                        if not line['konto_object']:
                            errorlist.append({
                                'line': linecounter,
                                'name': _('Attribute could not be converted!'),
                                'beschreibung': _('Account {account} could not be found in Odoo!'.format(account=line['konto']))
                            })
                        if not line['gegenkonto_object']:
                            errorlist.append({
                                'line': linecounter,
                                'name': _('Attribute could not be converted!'),
                                'beschreibung': _('Account {account} could not be found in Odoo!'.format(account=line['gegenkonto']))
                            })

                        thismove = thismove if datev_import.one_move else False
                        manual = not datev_import.one_move
                        next_seq = datev_import.journal_id.sequence_id.next_by_id()
                        line['name'] = next_seq
                        if not line.get('wkz', False):
                            currency_id = datev_import.journal_id.currency_id or datev_import.company_id.currency_id
                            line['wkz'] = currency_id.id
                        if not errorlist:
                            thismove, partner_id = self.create_account_move(
                                datev_import,
                                import_config,
                                line,
                                linecounter,
                                move_id=thismove,
                                manual=manual
                            )
                            move_lines = self.create_main_lines(
                                line,
                                thismove,
                                partner_id,
                                import_config,
                                import_struct
                            )
                            for move in move_lines:
                                move['credit'] = Decimal(move['credit'])
                                move['debit'] = Decimal(move['debit'])
                                move_line_ids_obj = move['move_id'].line_ids
                                move['move_id'] = move['move_id'].id
                                # skip validity check until all lines are created
                                move_line_ids_obj.with_context(check_move_validity=False).create(move)
                            # catch up validity check after all lines are created
                            thismove._check_balanced()
                            self.log_line.create({
                                'parent_id': datev_import.id,
                                'name': _('Line: {line} has been imported').format(line=linecounter + import_config['header_row']),
                                'state': 'standard',
                            })
                            datev_import.write({'state': 'imported'})
                        else:
                            for line in errorlist:
                                self.log_line.create({
                                    'parent_id': datev_import.id,
                                    'name': _('{desc} Line: {line}').format(desc=line['beschreibung'], line=line['line']),
                                    'state': 'error',
                                })
                            datev_import.write({'state': 'error'})
                else:
                    for line in errorlist:
                        self.log_line.create({
                            'parent_id': datev_import.id,
                            'name': _('{desc} Line: {line}').format(desc=line['beschreibung'], line=line['line']),
                            'state': 'error',
                        })
                    datev_import.write({'state': 'error'})
        return True

    def confirm_booking(self):
        """ Confirm the booking after all moves have been imported
        """
        for this_import in self:
            error = False
            for move in this_import.account_moves.filtered(lambda r: r.state == 'draft'):
                try:
                    move.post()
                    self.log_line.create({
                        'parent_id': this_import.id,
                        'name': _('{name} booked successful.').format(name=move.name),
                        'state': 'standard',
                    })
                except:
                    self.log_line.create({
                        'parent_id': this_import.id,
                        'name': _('{name} could not be booked, Odoo ERROR: {error}').format(name=move.name, error=traceback.format_exc()),
                        'state': 'error',
                    })
                    error = True
            this_import.state = 'booking_error' if error else 'booked'
        return True


class ImportDatevLog(models.Model):
    _name = 'import.datev.log'
    _order = 'id desc'

    name = fields.Text(string='Name')
    parent_id = fields.Many2one(comodel_name='import.datev', string='Import', ondelete='cascade')
    date = fields.Datetime(string='Time', readonly=True, default=lambda *a: fields.Datetime.today())
    state = fields.Selection(
        selection=[
            ('info', 'Info'),
            ('error', 'Error'),
            ('standard', 'Ok')
        ],
        string='State', select=True, readonly=True, default='info'
    )
