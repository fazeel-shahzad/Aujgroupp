# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

import logging
import re
from decimal import Decimal

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class Ecofi(models.Model):
    _name = 'ecofi'
    _inherit = [
        'ecofi',
        'ecofi.export.columns',
    ]

    def field_config(  # noqa: C901
        self,
        move,
        line,
        errorcount,
        partnererror,
        thislog,
        thismovename,
        faelligkeit,
        datevdict,
    ):
        """
        Generate the values for the different Datev columns.

        :param move: account_move
        :param line: account_move_line
        :param errorcount: Errorcount
        :param partnererror: Partnererror
        :param thislog: Log
        :param thismovename: Movename
        :param faelligkeit: Fälligkeit
        """
        datevdict['Datum'] = move.date.strftime('%d%m')

        if move.journal_id.type in ['purchase', 'bank'] and move.ref:
            datevdict['Beleg1'] = move.ref
        elif move.name:
            datevdict['Beleg1'] = move.name

        if faelligkeit:
            datevdict['Beleg2'] = faelligkeit

        datevdict['Waehrung'], datevdict['Kurs'] = self.with_context(
            lang='de_DE',
            date=move.date,
        ).format_waehrung(line)

        if move.ecofi_buchungstext:
            datevdict['Buchungstext'] = move.ecofi_buchungstext

        if line.name and line.name not in ['/', '<p><br></p>', '<p><br/></p>']:
            line_name = (
                line.name
                    .replace('<p>', '')
                    .replace('</p>', '')
                    .replace('<br/>', '')
                    .replace('<br>', '')
            )

            if datevdict.get('Buchungstext'):
                datevdict['Buchungstext'] = '{m_bu}, {l_bu}'.format(
                    m_bu=datevdict['Buchungstext'],
                    l_bu=line_name,
                )
            else:
                datevdict['Buchungstext'] = line_name

        if line.account_id.datev_vat_handover:
            if move.partner_id:
                if move.partner_id.vat:
                    datevdict['EulandUSTID'] = move.partner_id.vat
            if datevdict['EulandUSTID'] == '':
                errorcount += 1
                partnererror.append(move.partner_id.id)
                thislog = '{log} {name} {text} \n'.format(
                    log=thislog,
                    name=thismovename,
                    text=_(
                        'Error! No sales tax identification number stored'
                        ' in the partner!',
                    ),
                )
        return errorcount, partnererror, thislog, thismovename, datevdict

    def format_umsatz(self, lineumsatz):
        """
        Return the formatted amount.

        :param lineumsatz: amountC
        """
        soll_haben = 's' if lineumsatz > 0 else 'h'
        umsatz = str(abs(lineumsatz)).replace('.', ',')
        return umsatz, soll_haben

    def format_waehrung(self, line):
        """
        Format the currency for the export.

        :param line: account_move_line
        """
        factor = ''
        company = line.company_id or self.env.company
        currency = line.company_currency_id or company.currency_id

        if not self.env.context.get('datev_ignore_currency'):
            if line.currency_id.name != currency.name:
                currency = line.currency_id
                rate = self.env['res.currency.rate'].sudo().search([
                    ('currency_id', '=', currency.id),
                    ('name', '=', line.date),
                ])
                factor = str(
                    rate.rate if rate else currency.rate
                ).replace('.', ',')

        return currency.name if currency else '', factor

    def generate_csv(self, ecofi_csv, bookingdict, log):
        """
        Implement the generate_csv method for the datev interface.
        """
        ecofi_csv.writerow(bookingdict['datevheader'])
        ecofi_csv.writerow(bookingdict['buchungsheader'])
        for buchungsatz in bookingdict['buchungen']:
            ecofi_csv.writerow(buchungsatz)
        return super(Ecofi, self).generate_csv(ecofi_csv, bookingdict, log)

    def generate_csv_move_lines(  # noqa: C901
        self,
        move,
        buchungserror,
        errorcount,
        thislog,
        thismovename,
        export_method,
        partnererror,
        buchungszeilencount,
        bookingdict
    ):
        """
        Implement the generate_csv_move_lines method for the datev interface.
        """
        if 'buchungen' not in bookingdict:
            bookingdict['buchungen'] = []
        if 'buchungsheader' not in bookingdict:
            bookingdict['buchungsheader'] = (
                self.env['ecofi.export.columns'].get_datev_column_headings()
            )
        if 'datevheader' not in bookingdict:
            bookingdict['datevheader'] = (
                self.get_legal_datev_header(move.vorlauf_id)
            )

        faelligkeit = False
        move_tax_lines = 0
        grouped_line = {}

        for line in move.line_ids:
            if line.debit == 0 and line.credit == 0:
                continue

            datevkonto = line.account_id.code
            datevgegenkonto = line.ecofi_account_counterpart.code
            if datevgegenkonto == datevkonto:
                if line.date_maturity:
                    faelligkeit = line.date_maturity.strftime('%d%m%y')
                continue
            currency = (
                not self.env.context.get('datev_ignore_currency')
                and bool(line.amount_currency)
            )
            line_total = (
                Decimal(str(line.amount_currency))
                if currency else
                Decimal(str(line.debit)) - Decimal(str(line.credit))
            )
            buschluessel = ''
            if export_method == 'gross':
                if (
                    line.account_id.is_tax_account()
                    and not line.datev_posting_key == 'SD'
                ):
                    move_tax_lines += 1
                    continue
                if line.datev_posting_key == '40':
                    buschluessel = '40'
                else:
                    linetax = line.get_tax()
                    tax_multiplicator = (
                        Decimal(str(1.0 + (linetax.amount / 100)))
                    )
                    gross_value = (
                        round(line_total * tax_multiplicator, 2)
                        if linetax else
                        line_total
                    )
                    line_total = Decimal(str(gross_value))

                    if (
                        not line.account_id.datev_automatic_account
                        and linetax
                    ):
                        buschluessel = str(linetax.l10n_de_datev_code)

            # Ugly as fuck, but a rounding error is uglier
            umsatz, sollhaben = self.format_umsatz(
                Decimal(str(round(Decimal(str(line_total)), 2))),
            )

            # Fixes rounding mistakes
            if line.datev_export_value:
                # Ugly as fuck, but a rounding error is uglier
                umsatz = self.format_umsatz(
                    Decimal(str(round(
                        Decimal(str(line.datev_export_value)), 2),
                    ))
                )[0]

            datevdict = {
                'Sollhaben': sollhaben,
                'Umsatz': umsatz,
                'Gegenkonto': datevgegenkonto,
                'Konto': datevkonto or '',
                'Buschluessel': buschluessel,
                'Movename': move.name,
                'Festschreibung': str(int(bool(
                    move.restrict_mode_hash_table and move.inalterable_hash
                ))),
            }

            (
                errorcount,
                partnererror,
                thislog,
                thismovename,
                datevdict
            ) = self.field_config(
                move,
                line,
                errorcount,
                partnererror,
                thislog,
                thismovename,
                faelligkeit,
                datevdict,
            )

            datevdict = self._get_datev_dict(**datevdict)

            # ! TODO grouping does not work properly.
            # ! grouping adds 2*len(lines) lines with the
            # total of the move (2* = s+h each)
            if self.env.user.company_id.datev_group_lines:
                if self.env.user.company_id.datev_group_sh:
                    self._datev_grouping_combined(
                        grouped_line,
                        line,
                        sollhaben,
                        umsatz,
                        datevdict,
                    )
                else:
                    self._datev_grouping(
                        grouped_line,
                        line,
                        sollhaben,
                        umsatz,
                        datevdict,
                    )
            else:
                grouped_line[line.id] = datevdict

            buchungszeilencount += 1
        bookingdict['move_bookings'] = [
            self._create_export_line(datevdict)
            for datevdict in grouped_line.values()
            if self._decimal(datevdict.get('Umsatz'))
        ]
        return (
            buchungserror,
            errorcount,
            thislog,
            partnererror,
            buchungszeilencount,
            bookingdict,
            move_tax_lines
        )

    def _datev_grouping(self, grouped, line, s_h, turnover, datev_dict):
        key = '{account_id}:{tax_id}:{s_h}'.format(
            account_id=line.account_id.id,
            tax_id=line.ecofi_tax_id.id,
            s_h=s_h,
        )

        if key not in grouped:
            grouped[key] = datev_dict
            return

        grp_turnover = self._decimal(grouped[key]['Umsatz'])
        new_turnover = self._decimal(turnover)
        grp_turnover += new_turnover

        grouped[key]['Umsatz'], _ = self.format_umsatz(grp_turnover)

        if line.name != '/' and grouped.get(key, {}).get('Buchungstext'):
            grouped[key]['Buchungstext'] = '{bu_text}, {nbu_text}'.format(
                bu_text=grouped[key]['Buchungstext'],
                nbu_text=line.name,
            )

    def _datev_grouping_combined(
        self,
        grouped,
        line,
        s_h,
        turnover,
        datev_dict
    ):
        key = '{account_id}:{tax_id}'.format(
            account_id=line.account_id.id,
            tax_id=line.ecofi_tax_id.id,
        )

        if key not in grouped:
            grouped[key] = datev_dict
            return

        grp_turnover = self._decimal(grouped[key]['Umsatz'])
        new_turnover = self._decimal(turnover)

        if grouped[key]['Sollhaben'] != s_h:
            new_turnover = -new_turnover

        grp_turnover += new_turnover

        if grp_turnover < 0.0:
            grouped[key]['Sollhaben'] = (
                's'
                if grouped[key]['Sollhaben'] == 'h' else
                'h'
            )

        grouped[key]['Umsatz'], _ = self.format_umsatz(grp_turnover)

        if line.name != '/' and grouped.get(key, {}).get('Buchungstext'):
            grouped[key]['Buchungstext'] = '{bu_text}, {nbu_text}'.format(
                bu_text=grouped[key]['Buchungstext'],
                nbu_text=line.name,
            )

    @staticmethod
    def _get_datev_dict(**kwargs) -> dict:
        return {
            'Sollhaben': kwargs.get('Sollhaben', ''),
            'Umsatz': kwargs.get('Umsatz', ''),
            'Gegenkonto': kwargs.get('Gegenkonto', ''),
            'Datum': kwargs.get('Datum', ''),
            'Konto': kwargs.get('Konto', ''),
            'Beleg1': kwargs.get('Beleg1', ''),
            'Beleg2': kwargs.get('Beleg2', ''),
            'Waehrung': kwargs.get('Waehrung', ''),
            'Buschluessel': kwargs.get('Buschluessel', ''),
            'Kost1': kwargs.get('Kost1', ''),
            'Kost2': kwargs.get('Kost2', ''),
            'Kostmenge': kwargs.get('Kostmenge', ''),
            'Skonto': kwargs.get('Skonto', ''),
            'Buchungstext': kwargs.get('Buchungstext', ''),
            'EulandUSTID': kwargs.get('EulandUSTID', ''),
            'EUSteuer': kwargs.get('EUSteuer', ''),
            'Basiswaehrungsbetrag': kwargs.get('Basiswaehrungsbetrag', ''),
            'Basiswaehrungskennung': kwargs.get('Basiswaehrungskennung', ''),
            'Kurs': kwargs.get('Kurs', ''),
            'Movename': kwargs.get('Movename', ''),
            'Festschreibung': kwargs.get('Festschreibung', ''),
        }

    @api.model
    def _create_export_line(self, datev_dict: dict):
        """
        Create the datev csv move line.
        """
        return self.env['ecofi.export.columns'].get_datev_export_line(
            self._normalize_datev_dict(datev_dict),
        )

    def _decimal(self, value):
        """Return decimal type of the provided value."""
        if not value:
            value = '0'

        return Decimal(
            str(value).replace(',', '.')
        )

    def _normalize_datev_dict(self, datev_dict: dict) -> dict:
        normalized_dict = dict(datev_dict)

        if normalized_dict.get('Buschluessel') == '0':
            normalized_dict['Buschluessel'] = ''

        normalized_dict['Sollhaben'] = normalized_dict['Sollhaben'].upper()

        if normalized_dict.get('Buchungstext'):
            normalized_dict['Buchungstext'] = '{:.60}'.format(
                normalized_dict['Buchungstext'],
            )

        if normalized_dict.get('Beleg1'):
            normalized_dict['Beleg1'] = '{}'.format(
                re.sub(
                    '[^{}]'.format(Ecofi._get_valid_chars()),
                    '',
                    normalized_dict['Beleg1'],
                ),
            )[-36:]

        if normalized_dict.get('Beleg2'):
            normalized_dict['Beleg2'] = '{}'.format(
                re.sub(
                    '[^{}]'.format(Ecofi._get_valid_chars()),
                    '',
                    normalized_dict['Beleg2'],
                ),
            )[-36:]

        return normalized_dict

    def ecofi_buchungen(self, journal_ids, date_from, date_to):
        return super(Ecofi, self.with_context(
            datev_ignore_currency=self.env.company.datev_ignore_currency,
        )).ecofi_buchungen(journal_ids, date_from, date_to)

    @staticmethod
    def _get_valid_chars(additional_chars=None):
        """
        Get valid chars for Belegfeld 1 and Belegfeld 2.

        Those can be used e.g. in a RegEx.

        :param str additional_chars:
        :return: a string containing valid chars
        :rtype: str
        """
        chars = r'a-zA-Z0-9$%&*+\-/'

        if additional_chars and isinstance(additional_chars, str):
            chars += additional_chars

        return chars
