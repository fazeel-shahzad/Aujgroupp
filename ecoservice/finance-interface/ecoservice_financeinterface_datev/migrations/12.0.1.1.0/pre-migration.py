# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    old_cron_job = env.ref(
        'ecoservice_financeinterface_datev'
        '.ecofi_cron_update_line_autoaccounts_tax',
        False,
    )
    if old_cron_job:
        old_cron_job.unlink()
