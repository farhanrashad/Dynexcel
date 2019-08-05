# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from datetime import datetime

class HrAttendanceDuration(models.Model):
	_inherit = 'hr.attendance'

	att_duration = fields.Float("Duration", compute='_compute_duration')

	# find employee working time duration
	@api.multi
	def _compute_duration(self):
		for rec in self:
			if rec.check_out and rec.check_in:
				date1 = str(rec.check_in)
				datetime_format = '%Y-%m-%d %H:%M:%S'
				date2 = str(rec.check_out)
				date11 = datetime.strptime(date1, datetime_format)
				date12 = datetime.strptime(date2,datetime_format)
				timedelta = date12 - date11 
				tot_sec = timedelta.total_seconds()
				h = tot_sec//3600
				m = (tot_sec%3600) // 60
				duration_hour = ("%d.%d" %(h,m))
				rec.att_duration =  float(duration_hour)
