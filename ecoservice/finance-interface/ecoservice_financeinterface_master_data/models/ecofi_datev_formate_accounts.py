# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

from ast import literal_eval

from mako.template import Template as MakoTemplate

from odoo import _, fields, models


class EcofiDatevFormateAccounts(models.Model):
    _inherit = 'ecofi.datev.formate'

    # region Fields

    datev_type = fields.Selection(
        selection_add=[
            ('account_receivable', 'Accounts Receivable'),
            ('account_payable', 'Accounts Payable'),
        ],
        string='Exporttype',
    )

    # endregion

    def get_partners(self, account_id):
        """Get partner objects for the corresponding account_id."""

        # Get all partners that got the requested account
        domain = []
        if account_id.user_type_id.type == 'receivable':
            domain.append(('property_account_receivable_id', '=', account_id.id))
        elif account_id.user_type_id.type == 'payable':
            domain.append(('property_account_payable_id', '=', account_id.id))

        if not domain:
            return self.sudo().env['res.partner']

        domain.extend([
            ('parent_id', '=', False),
            ('company_id', 'in', [False, self.env.company.id]),
            '|', ('customer_rank', '>', 0), ('supplier_rank', '>', 0)
        ])
        return self.sudo().env['res.partner'].search(domain)

    def getfields_defaults(self, template):
        """
        Return the default MakeHelp and CSV Template File.
        """
        res = super().getfields_defaults(template)

        if template.datev_type == 'account_receivable':
            res.update({
                'csv_template': 'static/csv/datev_accounts_receivable.csv',
                'module': 'ecoservice_financeinterface_master_data',
                'mako_help': _(
                    'Possible Mako Object account and partner\n\n'
                    'If you want to export the Code of the account and the Name of the Partner use:\n'  # noqa: E501
                    '${account.code} and ${partner.name} as Makotext.'
                ),
            })
        elif template.datev_type == 'account_payable':
            res.update({
                'csv_template': 'static/csv/datev_accounts_payable.csv',
                'module': 'ecoservice_financeinterface_master_data',
                'mako_help': _(
                    'Possible Mako Object account and partner\n\n'
                    'If you want to export the Code of the account and the Name of the Partner use:\n'  # noqa: E501
                    '${account.code} and ${partner.name} as Makotext.'
                ),
            })

        return res

    def generate_export_csv(self, export, ecofi_csv):
        """
        Fill the CSV Export.
        """

        res = super().generate_export_csv(export, ecofi_csv)
        if (
            export.datev_type == 'account_receivable'
            or export.datev_type == 'account_payable'
        ):
            try:
                domain = literal_eval(export.datev_domain)
            # noqa: B902 as unknown now what the initial purpose was
            # TODO: refactor with specific exception
            except Exception:  # noqa: B902
                domain = []

            ecofi_csv.writerow(self.get_csv_headline(export.csv_spalten))

            csv_columns = self.get_csv_columns(export.csv_spalten)
            log = []

            accounts = self.env['account.account'].sudo().search(
                domain,
                order='code asc',
            )
            for account in accounts:
                for partner in self.get_partners(account):
                    line = []
                    for column in csv_columns:
                        reply = MakoTemplate(column.mako).render_unicode(  # nosec
                            account=account,
                            partner=partner,
                        )
                        if not reply or reply == 'False':
                            line.append('')
                            continue

                        converted_value = self.convert_value(column.typ, reply)
                        if converted_value['value']:
                            line.append(converted_value['value'])
                        else:
                            log.append(_(
                                'Account: {code} {fieldname} could not be exported!\n'
                                '\t{log}\n'
                            )).format(
                                code=account.code,
                                fieldname=column.feldname,
                                log=converted_value['log'],
                            )
                            break
                    else:
                        ecofi_csv.writerow(line)

            res['log'] += '\n'.join(log)
        return res
