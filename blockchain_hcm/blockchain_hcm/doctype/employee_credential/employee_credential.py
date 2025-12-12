# Copyright (c) 2025, Danar IT and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import hashlib
import json


class EmployeeCredential(Document):
	def validate(self):
		"""Validate the credential before saving"""
		self.validate_dates()
		self.update_verification_status()
	
	def before_save(self):
		"""Generate blockchain hash before saving"""
		if not self.blockchain_hash:
			self.blockchain_hash = self.generate_blockchain_hash()
	
	def validate_dates(self):
		"""Validate issue date and expiry date"""
		if self.expiry_date and self.issue_date:
			if self.expiry_date < self.issue_date:
				frappe.throw("Expiry Date cannot be before Issue Date")
	
	def update_verification_status(self):
		"""Update verification status based on expiry date"""
		if self.expiry_date:
			from frappe.utils import getdate, nowdate
			if getdate(self.expiry_date) < getdate(nowdate()):
				if self.verification_status != "Revoked":
					self.verification_status = "Expired"
	
	def generate_blockchain_hash(self):
		"""Generate a simple blockchain hash for the credential"""
		data = {
			"credential_name": self.credential_name,
			"employee": self.employee,
			"credential_type": self.credential_type,
			"issue_date": str(self.issue_date),
			"timestamp": str(frappe.utils.now())
		}
		hash_string = json.dumps(data, sort_keys=True)
		return hashlib.sha256(hash_string.encode()).hexdigest()


@frappe.whitelist()
def verify_credential(credential_name):
	"""Verify a credential and update its status"""
	doc = frappe.get_doc("Employee Credential", credential_name)
	doc.verification_status = "Verified"
	doc.save()
	frappe.msgprint(f"Credential {credential_name} has been verified")
	return doc


@frappe.whitelist()
def revoke_credential(credential_name):
	"""Revoke a credential"""
	doc = frappe.get_doc("Employee Credential", credential_name)
	doc.verification_status = "Revoked"
	doc.save()
	frappe.msgprint(f"Credential {credential_name} has been revoked")
	return doc
