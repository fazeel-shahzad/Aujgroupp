from odoo import models, fields, api, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    
    
                                 
        


    checkin_device_id = fields.Many2one('attendance.device', string='Checkin Device', readonly=True, index=True,
                                        help='The device with which user took check in action')
    checkout_device_id = fields.Many2one('attendance.device', string='Checkout Device', readonly=True, index=True,
                                         help='The device with which user took check out action')
    activity_id = fields.Many2one('attendance.activity', string='Attendance Activity',
                                  help='This field is to group attendance into multiple Activity (e.g. Overtime, Normal Working, etc)')
    employee_batch_id = fields.Char(related='employee_id.barcode', store=True)
    
    
    
 
    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        if not self.env.context.get('synch_ignore_constraints', False):
            super(HrAttendance, self)._check_validity()
            
            
    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """ Verifies the validity of the attendance record compared to the others from the same employee.
            For the same employee we must have :
                * maximum 1 "open" attendance record (without check_out)
                * no overlapping time slices with previous employee records
        """
        for attendance in self:
            # we take the latest attendance before our check_in time and check it doesn't overlap with ours
            last_attendance_before_check_in = self.env['hr.attendance'].search([
                ('employee_id', '=', attendance.employee_id.id),
                ('check_in', '<=', attendance.check_in),
                ('id', '!=', attendance.id),
            ], order='check_in desc', limit=1)
            if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
                raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                    'empl_name': attendance.employee_id.name,
                    'datetime': format_datetime(self.env, attendance.check_in, dt_format=False),
                })

            if not attendance.check_out:
                # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
                no_check_out_attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_out', '=', False),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if no_check_out_attendances:
                    pass
            else:
                # we verify that the latest attendance with check_in time before our check_out time
                # is the same as the one before our check_in time computed before, otherwise it overlaps
                last_attendance_before_check_out = self.env['hr.attendance'].search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '<', attendance.check_out),
                    ('id', '!=', attendance.id),
                ], order='check_in desc', limit=1)
                if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
                    raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
                        'empl_name': attendance.employee_id.name,
                        'datetime': format_datetime(self.env, last_attendance_before_check_out.check_in, dt_format=False),
                    })        
            
    
    

