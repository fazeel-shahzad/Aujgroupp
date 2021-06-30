# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import _, exceptions, fields, models


class EcofiMoveMigration(models.TransientModel):
    _name = 'ecofi.move.migration'
    _description = (
        'Wizard to set the taxes and counter accounts for the DATEV export'
    )

    migrate_all_companies = fields.Boolean(
        string='Migrate account moves of all companies',
        help='If not set only the moves of the current company will'
             ' be migrated.',
    )
    taxes_are_configured = fields.Boolean(
        required=True,
        help='Check this if you have configured the taxes with the correct tax'
             ' keys according to the guide or the official SKR Documentation.'
             "If you have checked 'Migrate account moves of all companies'"
             ' please make sure that you have configured the taxes for all'
             ' appropriate companies.',
    )
    accounts_are_configured = fields.Boolean(
        required=True,
        help='Check this if you have configured the accounts according to the'
             ' guide or the official SKR Documentation. If you have checked'
             " 'Migrate account moves of all companies' please make sure that"
             ' you have configured the accounts for all appropriate companies.',
    )

    companies = fields.Char()
    to_check_counter = fields.Integer()

    def action_migrate(self):
        if not (self.taxes_are_configured and self.accounts_are_configured):
            raise exceptions.UserError(_(
                "Both Checkboxes 'Taxes are configured' and 'Accounts are"
                " configured' must be checked in order to proceed!",
            ))

        sesu = self.sudo().with_context(logs={'to_check_counter': 0})

        companies = sesu._get_companies_with_skr()
        if not self.migrate_all_companies:
            companies &= self.env.company

        if not companies:
            return

        sesu._migrate_accounts(companies)
        sesu._migrate_taxes(companies)

        return sesu._show_result(companies)

    def _get_companies_with_skr(self):
        skr = self._get_available_skr_charts()
        company_model = self.env['res.company']

        if not skr:
            return company_model

        companies = company_model.search([('chart_template_id', 'in', skr)])

        return companies

    def _get_available_skr_charts(self):
        skr03 = self.env.ref('l10n_de_skr03.l10n_de_chart_template', False)
        skr04 = self.env.ref('l10n_de_skr04.l10n_chart_de_skr04', False)

        return [skr.id for skr in [skr03, skr04] if skr]

    def _migrate_accounts(self, companies):
        journals = self.env['account.journal'].search([
            ('company_id', 'in', companies.ids),
        ])
        for journal in journals:
            handle_fn = '_handle_journal_{}'.format(journal.type)
            getattr(
                self.with_context(force_company=journal.company_id.id),
                handle_fn
            )(journal)

    def _migrate_taxes(self, companies):
        accounts_with_taxes = self.env['account.account'].search([
            ('datev_tax_ids', '!=', False),
            ('company_id', 'in', companies.ids),
        ])
        for account in accounts_with_taxes.with_context(active_test=False):
            move_lines = self.env['account.move.line'].search([
                ('account_id', '=', account.id),
                ('move_id.state', '=', 'posted'),
            ])
            move_lines.write({
                'ecofi_tax_id': account.datev_tax_ids[0].id,
            })

        lines_with_taxes = self.env['account.move.line'].search([
            ('tax_ids', '!=', False),
            ('ecofi_tax_id', '=', False),
            ('company_id', 'in', companies.ids),
            ('move_id.state', '=', 'posted'),
        ])
        for line in lines_with_taxes.with_context(active_test=False):
            line.ecofi_tax_id = line.tax_ids[0]

    def _handle_journal_sale(self, journal):
        self._set_counter_account_from_invoice(journal)

    def _handle_journal_purchase(self, journal):
        self._set_counter_account_from_invoice(journal)

    def _handle_journal_cash(self, journal):
        self._set_counter_account_from_journal(journal)

    def _handle_journal_bank(self, journal):
        self._set_counter_account_from_journal(journal)

    def _handle_journal_general(self, journal):
        moves = self.env['account.move'].search([
            ('journal_id', '=', journal.id),
            ('state', '=', 'posted'),
        ])
        for move in moves:
            # Fewer than two move lines? This is not valid according to
            # Double-Entry Accounting
            if len(move.line_ids) < 2:
                self.env.context['logs']['to_check_counter'] += 1
                move.write({
                    'ecofi_to_check': True,
                })

            # If the move hast more than two lines we can check for the
            # amount of credit and debit accounts.
            # We could also check for the special case of exactly two move lines
            # but that would be more code with doubtful performance improvements
            credit_lines = move.line_ids.filtered('credit')
            debit_lines = move.line_ids.filtered('debit')

            # If there is only one line where the debit amount is set: use it.
            # Also true for len(move.line_ids) == 2
            if len(debit_lines) == 1:
                move.line_ids.write({
                    'ecofi_account_counterpart': debit_lines.account_id.id,
                })
            # Alternatively, if there is only one line where the credit amount
            # is set: Use this one instead
            elif len(credit_lines) == 1:
                move.line_ids.write({
                    'ecofi_account_counterpart': credit_lines.account_id.id,
                })
            else:
                accounts = move.line_ids.mapped('account_id')
                if len(accounts) == 2:
                    move.line_ids.write({
                        'ecofi_account_counterpart': accounts[0].id,
                    })
                # We can't do funny cases automatically (yet),
                # so the user has to do it manually
                else:
                    self.env.context['logs']['to_check_counter'] += 1
                    move.write({
                        'ecofi_to_check': True,
                    })

    def _set_counter_account_from_journal(self, journal):
        account = journal.default_debit_account_id
        moves = self.env['account.move'].search([
            ('journal_id', '=', journal.id),
            ('state', '=', 'posted'),
        ])
        moves.mapped('line_ids').write({
            'ecofi_account_counterpart': account.id,
        })

    def _set_counter_account_from_invoice(self, journal):
        invoices = self.env['account.move'].search([
            ('journal_id', '=', journal.id),
            ('state', '=', 'posted'),
        ])
        if journal.type == 'sale':
            for invoice in invoices:
                invoice.mapped('line_ids').write({
                    'ecofi_account_counterpart':
                        invoice.partner_id.property_account_receivable_id.id,
                })
        else:
            for invoice in invoices:
                invoice.mapped('line_ids').write({
                    'ecofi_account_counterpart':
                        invoice.partner_id.property_account_payable_id.id,
                })

    def _show_result(self, companies):
        action = self.env.ref(
            'ecoservice_financeinterface_datev'
            '.action_ecofi_move_migration_result',
        ).read()[0]

        action['context'] = {
            'default_companies':
                ', '.join(companies.mapped('name')),
            'default_to_check_counter':
                self.env.context['logs']['to_check_counter'],
        }

        return action
