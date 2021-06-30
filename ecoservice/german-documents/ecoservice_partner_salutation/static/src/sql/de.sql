--# Part of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
--# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

-- Madam
UPDATE res_partner_title
   SET salutation = 'Dear Mrs.'
 WHERE name = 'Madam';

INSERT INTO ir_translation (lang, src, name, type, module, state, value, res_id)
     VALUES ('de_DE', 'Dear Mrs.', 'res.partner.title,salutation', 'model', 'base', 'translated', 'Sehr geehrte Frau', 1)
     ON CONFLICT (type, name, lang, res_id, md5(src))
     DO UPDATE SET value='Sehr geehrte Frau';

-- Miss
UPDATE res_partner_title
   SET salutation = 'Dear Miss'
 WHERE name = 'Miss';

INSERT INTO ir_translation (lang, src, name, type, module, state, value, res_id)
     VALUES ('de_DE', 'Dear Miss', 'res.partner.title,salutation', 'model', 'base', 'translated', 'Sehr geehrte Frau', 2)
     ON CONFLICT (type, name, lang, res_id, md5(src))
     DO UPDATE SET value='Sehr geehrte Frau';

-- Mister
UPDATE res_partner_title
   SET salutation = 'Dear Mr.'
 WHERE name = 'Mister';

INSERT INTO ir_translation (lang, src, name, type, module, state, value, res_id)
     VALUES ('de_DE', 'Dear Mr.', 'res.partner.title,salutation', 'model', 'base', 'translated', 'Sehr geehrter Herr', 3)
     ON CONFLICT (type, name, lang, res_id, md5(src))
     DO UPDATE SET value='Sehr geehrter Herr';

-- Doctor
UPDATE res_partner_title
   SET salutation = 'Dear Dr.'
 WHERE name = 'Doctor';

INSERT INTO ir_translation (lang, src, name, type, module, state, value, res_id)
     VALUES ('de_DE', 'Dear Dr.', 'res.partner.title,salutation', 'model', 'base', 'translated', 'Sehr geehrter Herr Dr.', 4)
     ON CONFLICT (type, name, lang, res_id, md5(src))
     DO UPDATE SET value='Sehr geehrter Herr Dr.';

-- Professor
UPDATE res_partner_title
   SET salutation = 'Dear Professor'
 WHERE name = 'Professor';

INSERT INTO ir_translation (lang, src, name, type, module, state, value, res_id)
     VALUES ('de_DE', 'Dear Professor', 'res.partner.title,salutation', 'model', 'base', 'translated', 'Sehr geehrter Herr Professor', 5)
     ON CONFLICT (type, name, lang, res_id, md5(src))
     DO UPDATE SET value='Sehr geehrter Herr Professor';
