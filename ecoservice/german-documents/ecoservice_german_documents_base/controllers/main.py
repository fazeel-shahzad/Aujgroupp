# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

import json
import time

from werkzeug import url_decode

from odoo import http
from odoo.http import request
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval

from odoo.addons.web.controllers.main import (
    ReportController,
    _serialize_exception,
    content_disposition,
)


class ReportControllerGermanDocuments(ReportController):

    @http.route(['/report/download'], type='http', auth='user')  # noqa: C901
    def report_download(self, data, token, context=None):
        request_content = json.loads(data)
        url, content_type = request_content[0], request_content[1]

        if content_type not in ['qweb-pdf', 'qweb-text']:
            return

        if content_type == 'qweb-pdf':
            converter = 'pdf'
            extension = 'pdf'
            pattern = '/report/pdf/'
        else:
            converter = 'text'
            extension = 'txt'
            pattern = '/report/text/'

        try:
            reportname = url.split(pattern)[1].split('?')[0]

            docids = None
            if '/' in reportname:
                reportname, docids = reportname.split('/')

            if docids:
                # Generic report:
                response = self.report_routes(
                    reportname,
                    docids=docids,
                    converter=converter,
                    context=context,
                )
            else:
                # Particular report:
                data = dict(url_decode(url.split('?')[1]).items())
                if 'context' in data:
                    context, data_context = (
                        json.loads(context or '{}'),  # noqa: P103
                        json.loads(data.pop('context'))
                    )
                    context = json.dumps({**context, **data_context})
                response = self.report_routes(
                    reportname,
                    converter=converter,
                    context=context,
                    **data,
                )

            report = request.env['ir.actions.report']._get_report_from_name(reportname)

            report_name = report.name

            if docids:
                ids = [int(x) for x in docids.split(',')]
                obj = request.env[report.model].browse(ids)

                # change: Special file names provided by German Documents
                if hasattr(obj, 'eco_report_name'):
                    report_name = '{name}'.format(
                        name=obj.with_context(
                            lang=obj[0].partner_id.lang,
                            report_xml_id=reportname,
                        ).eco_report_name(),
                    )
                elif report.print_report_name and not len(obj) > 1:
                    report_name = safe_eval(
                        report.print_report_name,
                        {
                            'object': obj,
                            'time': time,
                        }
                    )

            # change: Odoo cannot handle too long file names
            filename = '{name:.100}.{extension}'.format(
                name=report_name,
                extension=extension,
            )

            response.headers.add(
                'Content-Disposition',
                content_disposition(filename),
            )
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se,
            }
            return request.make_response(html_escape(json.dumps(error)))
