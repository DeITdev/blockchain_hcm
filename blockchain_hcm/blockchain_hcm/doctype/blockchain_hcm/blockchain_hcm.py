# Copyright (c) 2025, Danar IT and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import hashlib
import json


class BlockchainHCM(Document):
	def before_save(self):
		"""Generate blockchain hash before saving"""
		if not self.blockchain_hash:
			self.blockchain_hash = self.generate_blockchain_hash()
	
	def generate_blockchain_hash(self):
		"""Generate a simple blockchain hash"""
		data = {
			"title": self.title,
			"status": self.status,
			"timestamp": str(frappe.utils.now())
		}
		hash_string = json.dumps(data, sort_keys=True)
		return hashlib.sha256(hash_string.encode()).hexdigest()

