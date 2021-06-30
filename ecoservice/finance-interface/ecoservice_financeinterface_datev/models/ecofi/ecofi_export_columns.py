# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from datetime import datetime, timedelta

from odoo import _, api, exceptions, models


class EcofiExportColumns(models.AbstractModel):
    _name = 'ecofi.export.columns'
    _description = 'Structure and meta data for the export csv file'

    def get_legal_datev_header(self, ecofi):
        """
        Get the required legal header for finance tax authorities.

        See "DATEV Schnittstellen-Entwicklungsleitfaden" for details
        """

        create_date = datetime.now().strftime('%Y%m%d%H%M%S000')
        date_from = ecofi.date_from.strftime('%Y%m%d')
        date_to = ecofi.date_to.strftime('%Y%m%d')

        if not ecofi.company_id.currency_id.name:
            raise exceptions.UserError(_(
                'Please ensure that your company has a valid currency set.',
            ))

        if not ecofi.company_id.sudo().chart_template_id:
            raise exceptions.UserError(_(
                'Please ensure that your company has'
                ' a valid account chart set.',
            ))

        if (
            not ecofi.company_id.l10n_de_datev_client_number
            or not ecofi.company_id.l10n_de_datev_consultant_number
        ):
            raise exceptions.UserError(_(
                'Please set a client and consultant number'
                ' in the DATEV settings.',
            ))

        # Calculate the current fiscal date
        str_fiscal_date = '{year}-{month}-{day}'.format(
            year=datetime.now().strftime('%Y'),
            month=self.env.company.fiscalyear_last_month,
            day=self.env.company.fiscalyear_last_day
        )
        fiscal_date = (
            datetime.strptime(str_fiscal_date, '%Y-%m-%d')
            + timedelta(days=1)
        )
        if fiscal_date > datetime.now():
            str_fiscal_date = '{year}-{month}-{day}'.format(
                year=int(datetime.now().strftime('%Y')) - 1,
                month=self.env.company.fiscalyear_last_month,
                day=self.env.company.fiscalyear_last_day
            )
            fiscal_date = (
                datetime.strptime(str_fiscal_date, '%Y-%m-%d')
                + timedelta(days=1)
            )

        # Get SKR No.
        skr_03 = self.env.ref('l10n_de_skr03.l10n_de_chart_template', False)
        skr_04 = self.env.ref('l10n_de_skr04.l10n_chart_de_skr04', False)
        chart_of_accounts = ecofi.sudo().company_id.chart_template_id
        skr_no = (
            skr_03 and chart_of_accounts == skr_03 and '03'
            or skr_04 and chart_of_accounts == skr_04 and '04'
            or ''
        )

        # Datetime-Format: JJJJMMTTHHMMSS | Trennzeichen: Semicolon
        return [
            'EXTF',  # External Format [length: 4, type: string] # noqa: E501
            '700',  # DATEV Version Number [length: 3, type: int] # noqa: E501
            '21',  # Data-Category [length: 2, type: int] # noqa: E501
            'Buchungsstapel',  # Formatname [length: X, type: string] # noqa: E501
            '9',  # Formatversion [length: 1, type: int] # noqa: E501
            create_date,  # Creation date [type: datetime] # noqa: E501
            '',  # Import date [type: datetime] # noqa: E501
            '',  # Source [type: string] # noqa: E501
            '',  # Exported by [length: X, type: string] # noqa: E501
            '',  # Imported by [type: string] # noqa: E501
            str(ecofi.company_id.l10n_de_datev_consultant_number),  # Consultant Number von [length: 7, type: int] # noqa: E501
            str(ecofi.company_id.l10n_de_datev_client_number),  # Client number [length: 5, type: int] # noqa: E501
            fiscal_date.strftime('%Y%m%d'),  # Wirtschaftsjahresbeginn [type: datetime] noqa: E501
            str(ecofi.company_id.account_code_digits),  # Sachkontennummernlänge [length: 1, type: int] # noqa: E501
            date_from,  # Date from [type: datetime] # noqa: E501
            date_to,  # Date to [type: datetime] # noqa: E501
            '',  # Description [length: 30, type: string] # noqa: E501
            '',  # Diktatkürzel [length: 2, type: string] # noqa: E501
            '',  # Booking type [length: 1, type: int] # noqa: E501
            '',  # Rechnungslegungszweck [length: 2, type: int] # noqa: E501
            '0',  # Festschreibung [length: 1, type: int-bool] # noqa: E501
            ecofi.company_id.currency_id.name,  # Currency [length: 3, type: string] # noqa: E501
            '',  # Reserved [type: int] # noqa: E501
            '',  # Derivatskennzeichen [type: string] # noqa: E501
            '',  # Reserved [type: int] # noqa: E501
            '',  # Reserved [type: int] # noqa: E501
            skr_no,  # SKR [type: string, z.B. 03] # noqa: E501
            '',  # Branchen-lösung-Id [type: int] # noqa: E501
            '',  # Reserved [type: int] # noqa: E501
            '',  # Reserved [ype: int] # noqa: E501
            '',  # Anwendungsinformation [length: 16, type: string] # noqa: E501
        ]

    @api.model
    def get_datev_column_headings(self):
        """
        Create the Datev CSV header line.
        """
        return [
            'Umsatz (ohne Soll-/Haben-Kennzeichen)',
            'Soll-/Haben-Kennzeichen',
            'WKZ Umsatz',
            'Kurs',
            'Basisumsatz',
            'WKZ Basisumsatz',
            'Konto',
            'Gegenkonto (ohne BU-Schlüssel)',
            'BU-Schlüssel',
            'Belegdatum',
            'Belegfeld 1',
            'Belegfeld 2',
            'Skonto',
            'Buchungstext',
            'Postensperre',
            'Diverse Adressnummer',
            'Geschäftspartnerbank',
            'Sachverhalt',
            'Zinssperre',
            'Beleglink',
            'Beleginfo - Art 1',
            'Beleginfo - Inhalt 1',
            'Beleginfo - Art 2',
            'Beleginfo - Inhalt 2',
            'Beleginfo - Art 3',
            'Beleginfo - Inhalt 3',
            'Beleginfo - Art 4',
            'Beleginfo - Inhalt 4',
            'Beleginfo - Art 5',
            'Beleginfo - Inhalt 5',
            'Beleginfo - Art 6',
            'Beleginfo - Inhalt 6',
            'Beleginfo - Art 7',
            'Beleginfo - Inhalt 7',
            'Beleginfo - Art 8',
            'Beleginfo - Inhalt 8',
            'KOST1 - Kostenstelle',
            'KOST2 - Kostenstelle',
            'Kost-Menge',
            'EU-Land u. UStID',
            'EU-Steuersatz',
            'Abw. Versteuerungsart',
            'Sachverhalt L+L',
            'Funktionsergänzung L+L',
            'BU 49 Hauptfunktionstyp',
            'BU 49 Hauptfunktionsnummer',
            'BU 49 Funktionsergänzung',
            'Zusatzinformation - Art 1',
            'Zusatzinformation- Inhalt 1',
            'Zusatzinformation - Art 2',
            'Zusatzinformation- Inhalt 2',
            'Zusatzinformation - Art 3',
            'Zusatzinformation- Inhalt 3',
            'Zusatzinformation - Art 4',
            'Zusatzinformation- Inhalt 4',
            'Zusatzinformation - Art 5',
            'Zusatzinformation- Inhalt 5',
            'Zusatzinformation - Art 6',
            'Zusatzinformation- Inhalt 6',
            'Zusatzinformation - Art 7',
            'Zusatzinformation- Inhalt 7',
            'Zusatzinformation - Art 8',
            'Zusatzinformation- Inhalt 8',
            'Zusatzinformation - Art 9',
            'Zusatzinformation- Inhalt 9',
            'Zusatzinformation - Art 10',
            'Zusatzinformation- Inhalt 10',
            'Zusatzinformation - Art 11',
            'Zusatzinformation- Inhalt 11',
            'Zusatzinformation - Art 12',
            'Zusatzinformation- Inhalt 12',
            'Zusatzinformation - Art 13',
            'Zusatzinformation- Inhalt 13',
            'Zusatzinformation - Art 14',
            'Zusatzinformation- Inhalt 14',
            'Zusatzinformation - Art 15',
            'Zusatzinformation- Inhalt 15',
            'Zusatzinformation - Art 16',
            'Zusatzinformation- Inhalt 16',
            'Zusatzinformation - Art 17',
            'Zusatzinformation- Inhalt 17',
            'Zusatzinformation - Art 18',
            'Zusatzinformation- Inhalt 18',
            'Zusatzinformation - Art 19',
            'Zusatzinformation- Inhalt 19',
            'Zusatzinformation - Art 20',
            'Zusatzinformation- Inhalt 20',
            'Stück',
            'Gewicht',
            'Zahlweise',
            'Forderungsart',
            'Veranlagungsjahr',
            'Zugeordnete Fälligkeit',
            'Skontotyp',
            'Auftragsnummer',
            'Buchungstyp',
            'Ust-Schlüssel (Anzahlungen)',
            'EU-Land (Anzahlungen)',
            'Sachverhalt L+L (Anzahlungen)',
            'EU-Steuersatz (Anzahlungen)',
            'Erlöskonto (Anzahlungen)',
            'Herkunft-Kz',
            'Leerfeld',
            'KOST-Datum',
            'Mandatsreferenz',
            'Skontosperre',
            'Gesellschaftername',
            'Beteiligtennummer',
            'Identifikationsnummer',
            'Zeichnernummer',
            'Postensperre bis',
            'Bezeichnung SoBil-Sachverhalt',
            'Kennzeichen SoBil-Buchung',
            'Festschreibung',
            'Leistungsdatum',
            'Datum Zuord.Steuerperiode'
        ]

    @api.model
    def get_datev_export_line(self, datev_dict):
        return [
            datev_dict['Umsatz'] or '',
            datev_dict['Sollhaben'] or '',
            datev_dict['Waehrung'] or '',
            datev_dict['Kurs'] or '',
            datev_dict['Basiswaehrungsbetrag'] or '',
            datev_dict['Basiswaehrungskennung'] or '',
            datev_dict['Konto'] or '',
            datev_dict['Gegenkonto'] or '',
            datev_dict['Buschluessel'] or '',
            datev_dict['Datum'] or '',
            datev_dict['Beleg1'] or '',
            datev_dict['Beleg2'] or '',
            datev_dict['Skonto'] or '',
            datev_dict['Buchungstext'] or '',
            '',  # Postensperre
            '',  # Diverse Adressnummer
            '',  # Geschäftspartnerbank
            '',  # Sachverhalt
            '',  # Zinssperre
            '',  # Beleglink
            '',  # Beleginfo - Art 1
            '',  # Beleginfo - Inhalt 1
            '',  # Beleginfo - Art 2
            '',  # Beleginfo - Inhalt 2
            '',  # Beleginfo - Art 3
            '',  # Beleginfo - Inhalt 3
            '',  # Beleginfo - Art 4
            '',  # Beleginfo - Inhalt 4
            '',  # Beleginfo - Art 5
            '',  # Beleginfo - Inhalt 5
            '',  # Beleginfo - Art 6
            '',  # Beleginfo - Inhalt 6
            '',  # Beleginfo - Art 7
            '',  # Beleginfo - Inhalt 7
            '',  # Beleginfo - Art 8
            '',  # Beleginfo - Inhalt 8
            datev_dict['Kost1'] or '',
            datev_dict['Kost2'] or '',
            datev_dict['Kostmenge'] or '',
            datev_dict['EulandUSTID'] or '',
            datev_dict['EUSteuer'] or '',
            '',  # Abw. Versteuerungsart
            '',  # Sachverhalt L+L
            '',  # Funktionsergänzung L+L
            '',  # BU 49 Hauptfunktionstyp
            '',  # BU 49 Hauptfunktionsnummer
            '',  # BU 49 Funktionsergänzung
            '',  # Zusatzinformation - Art 1
            '',  # Zusatzinformation- Inhalt 1
            '',  # Zusatzinformation - Art 2
            '',  # Zusatzinformation- Inhalt 2
            '',  # Zusatzinformation - Art 3
            '',  # Zusatzinformation- Inhalt 3
            '',  # Zusatzinformation - Art 4
            '',  # Zusatzinformation- Inhalt 4
            '',  # Zusatzinformation - Art 5
            '',  # Zusatzinformation- Inhalt 5
            '',  # Zusatzinformation - Art 6
            '',  # Zusatzinformation- Inhalt 6
            '',  # Zusatzinformation - Art 7
            '',  # Zusatzinformation- Inhalt 7
            '',  # Zusatzinformation - Art 8
            '',  # Zusatzinformation- Inhalt 8
            '',  # Zusatzinformation - Art 9
            '',  # Zusatzinformation- Inhalt 9
            '',  # Zusatzinformation - Art 10
            '',  # Zusatzinformation- Inhalt 10
            '',  # Zusatzinformation - Art 11
            '',  # Zusatzinformation- Inhalt 11
            '',  # Zusatzinformation - Art 12
            '',  # Zusatzinformation- Inhalt 12
            '',  # Zusatzinformation - Art 13
            '',  # Zusatzinformation- Inhalt 13
            '',  # Zusatzinformation - Art 14
            '',  # Zusatzinformation- Inhalt 14
            '',  # Zusatzinformation - Art 15
            '',  # Zusatzinformation- Inhalt 15
            '',  # Zusatzinformation - Art 16
            '',  # Zusatzinformation- Inhalt 16
            '',  # Zusatzinformation - Art 17
            '',  # Zusatzinformation- Inhalt 17
            '',  # Zusatzinformation - Art 18
            '',  # Zusatzinformation- Inhalt 18
            '',  # Zusatzinformation - Art 19
            '',  # Zusatzinformation- Inhalt 19
            '',  # Zusatzinformation - Art 20
            '',  # Zusatzinformation- Inhalt 20
            '',  # Stück
            '',  # Gewicht
            '',  # Zahlweise
            '',  # Forderungsart
            '',  # Veranlagungsjahr
            '',  # Zugeordnete Fälligkeit
            '',  # Skontotyp
            '',  # Auftragsnummer
            '',  # Buchungstyp
            '',  # Ust-Schlüssel (Anzahlungen)
            '',  # EU-Land (Anzahlungen)
            '',  # Sachverhalt L+L (Anzahlungen)
            '',  # EU-Steuersatz (Anzahlungen)
            '',  # Erlöskonto (Anzahlungen)
            '',  # Herkunft-Kz
            '',  # Leerfeld
            '',  # KOST-Datum
            '',  # Mandatsreferenz
            '',  # Skontosperre
            '',  # Gesellschaftername
            '',  # Beteiligtennummer
            '',  # Identifikationsnummer
            '',  # Zeichnernummer
            '',  # Postensperre bis
            '',  # Bezeichnung SoBil-Sachverhalt
            '',  # Kennzeichen SoBil-Buchung
            datev_dict['Festschreibung'] or '',  # Festschreibung
            '',  # Leistungsdatum
            ''   # Datum Zuord.Steuerperiode
        ]
