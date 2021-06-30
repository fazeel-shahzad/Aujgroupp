# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

from ast import literal_eval

from mako.template import Template as MakoTemplate

from odoo import _, fields, models


class EcofiDatevFormatePaymentTerms(models.Model):
    _inherit = 'ecofi.datev.formate'

    # region Fields

    datev_type = fields.Selection(
        selection_add=[
            ('payment_term', 'Payment terms')
        ],
        string='Exporttype',
    )

    # endregion

    def getfields_defaults(self, template):
        """
        Return the Defaults MakeHelp and CSV Template File.
        """
        res = super().getfields_defaults(template)

        if template.datev_type == 'payment_term':
            res.update({
                'csv_template': 'static/csv/datev_payment_terms.csv',
                'module': 'ecoservice_financeinterface_master_data',
                'mako_help': _(
                    'Possible Mako Object paymentterm\n\n'
                    """Paymentterm Values:
    'number'
    'name'
    'typ'
    'netdays'
    'skonto1days'
    'skonto1percent'
    'skonto2days'
    'skonto2percent'
    'error'
    'log'"""
                ),
            })

        return res

    def generate_payment_terms(self, paymentterm):
        """
        Generate the Payment Term for Mako.
        """
        res = {
            'number': paymentterm.id,
            'name': paymentterm.name,
            'typ': 1,
            'netdays': False,
            'skonto1days': '',
            'skonto1percent': '',
            'skonto2days': '',
            'skonto2percent': '',
            'error': False,
            'log': ''
        }
        skonto_count = 0

        for line in paymentterm.line_ids:
            if line.value == 'balance':
                res['netdays'] = line.days
            elif line.value == 'procent':
                if skonto_count == 0:
                    res['skonto1days'] = line.days
                    res['skonto1percent'] = line.value_amount * 100
                elif skonto_count == 1:
                    res['skonto2days'] = line.days
                    res['skonto2percent'] = line.value_amount * 100
                skonto_count += 1

        if not res['netdays']:
            res['error'] = True
            res['log'] = _('Payment term {name} has no balance line').format(
                name=paymentterm.name,
            )

        if skonto_count > 1:
            res['error'] = True
            res['log'] = _('Payment term {name} has more than 2 percent lines').format(
                name=paymentterm.name,
            )

        return res

    def generate_export_csv(self, export, ecofi_csv):
        """
        Fill the CSV Export.
        """
        res = super().generate_export_csv(export, ecofi_csv)
        if export.datev_type == 'payment_term':
            try:
                domain = literal_eval(export.datev_domain)
            # noqa: B902 as unknown now what the initial purpose was
            # TODO: refactor with specific exception
            except Exception:  # noqa: B902
                domain = []

            paymentterm_ids = self.env['account.payment.term'].search(
                domain,
                order='id asc',
            )

            ecofi_csv.writerow(self.get_csv_headline(export.csv_spalten))

            csv_columns = self.get_csv_columns(export.csv_spalten)
            log = []

            for paymentterm in paymentterm_ids:
                line = []
                for column in csv_columns:
                    thispaymentterm = self.generate_payment_terms(paymentterm)
                    if thispaymentterm['error']:
                        log.append(
                            _(
                                'Payment term: {name} could not be exported!\n'
                                '\t{log}\n'
                            ).format(
                                name=paymentterm.name,
                                log=thispaymentterm['log'],
                            )
                        )
                        break

                    reply = MakoTemplate(  # nosec
                        column.mako,
                    ).render_unicode(
                        paymentterm=thispaymentterm,
                    )
                    if not reply or reply == 'False':
                        line.append('')
                        continue

                    converted_value = self.convert_value(column.typ, reply)
                    if converted_value['value']:
                        line.append(converted_value['value'])
                    else:
                        log.append(
                            _(
                                'Payment term: {name} could not be exported!\n'
                                '\t{log}\n'
                            ).format(
                                name=paymentterm.name,
                                log=converted_value['log'],
                            )
                        )
                        break
                else:
                    ecofi_csv.writerow(line)

            res['log'] += '\n'.join(log)
        return res
