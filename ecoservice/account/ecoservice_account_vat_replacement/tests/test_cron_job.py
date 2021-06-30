# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from datetime import datetime, timedelta

from odoo.tests import SavepointCase


class TestCronJob(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.RU = cls.env['res.users'].with_context(tracking_disable=True)
        cls.VC = cls.env['vat.configuration']
        cls.CJ = cls.env['ir.cron']

        cls.user = cls.RU.create({
            'name': 'Account Manager',
            'login': 'account_manager',
            'groups_id': [(6, 0, [cls.env.ref('account.group_account_manager').id])],
        })

    def test_cron_creation(self):
        # create configuration
        configuration = self.VC.with_user(self.user.id).create({
            'company_id': self.env.company.id,
            'description': 'desc',
            'execution_time': datetime.now() + timedelta(hours=1),
        })

        # execute schedule button
        configuration.action_cron()

        # check if cron is created
        self.assertTrue(configuration.scheduled_cron_job)
        cron = configuration.scheduled_cron_job
        self.assertEqual(cron.nextcall, configuration.execution_time)
        self.assertEqual(cron.numbercall, 1)
        self.assertEqual(cron.model_id.model, 'vat.configuration')

    def test_cron_with_xml_id(self):
        # create configuration
        configuration = self.VC.with_user(self.user.id).create({
            'company_id': self.env.company.id,
            'description': 'desc2',
            'execution_time': datetime.now() + timedelta(hours=1),
        })

        # execute schedule button
        configuration.action_cron()

        # check if xmlid is created
        name = (
            'ecoservice_account_vat_replacement'
            '.schedule_replace_account_tax_{conf_id}'.format(
                conf_id=configuration.id,
            )
        )
        xmlid = self.env.ref(name, raise_if_not_found=False)
        self.assertTrue(xmlid)
        self.assertEqual('ecoservice_account_vat_replacement.' + xmlid.name, name)

    def test_unlink_cronjob_on_unlink_configuration(self):
        # create configuration
        configuration = self.VC.with_user(self.user.id).create({
            'company_id': self.env.company.id,
            'description': 'desc3',
            'execution_time': datetime.now() + timedelta(hours=1),
        })

        # execute schedule button
        configuration.action_cron()

        # check if cron is created
        self.assertTrue(configuration.scheduled_cron_job)
        cron = configuration.scheduled_cron_job

        # unlink configuration
        configuration.unlink()

        # check if cronjob exists
        self.assertFalse(cron.exists())
