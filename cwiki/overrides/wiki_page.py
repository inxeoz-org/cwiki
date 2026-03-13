# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt


from urllib.parse import urlencode

import frappe
from wiki.wiki.doctype.wiki_page.wiki_page import WikiPage


class CustomWikiPage(WikiPage):
	def verify_permission(self):
		wiki_settings = frappe.get_single("Wiki Settings")
		user_is_guest = frappe.session.user == "Guest"

		disable_guest_access = False
		if wiki_settings.disable_guest_access and user_is_guest:
			disable_guest_access = True

		access_permitted = self.allow_guest or not user_is_guest

		if not access_permitted or disable_guest_access:
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "/login?" + urlencode({"redirect-to": frappe.request.url})
			raise frappe.Redirect

		user_roles = frappe.get_roles(frappe.session.user)
		allowed_role = False

		if self.custom_read_role and self.custom_read_role in user_roles:
			allowed_role = True

		if not allowed_role and self.custom_edit_role and self.custom_edit_role in user_roles:
			allowed_role = True

		if not allowed_role:
			frappe.local.response.http_status_code = 403
			frappe.throw(_(f"You are not permitted to access this page {self.title}"), frappe.PermissionError)

	def get_sidebar_items(self):
		wiki_sidebar = frappe.get_doc("Wiki Space", {"route": self.get_space_route()}).wiki_sidebars
		sidebar = {}

		user_roles = frappe.get_roles(frappe.session.user)

		for sidebar_item in wiki_sidebar:
			if sidebar_item.hide_on_sidebar:
				continue

			wiki_page = frappe.get_cached_doc("Wiki Page", sidebar_item.wiki_page)

			allowed_role = False

			if wiki_page.custom_read_role and wiki_page.custom_read_role in user_roles:
				allowed_role = True

			if not allowed_role and wiki_page.custom_edit_role and wiki_page.custom_edit_role in user_roles:
				allowed_role = True

			if not allowed_role:
				continue

			if sidebar_item.parent_label not in sidebar:
				sidebar[sidebar_item.parent_label] = [
					{
						"name": wiki_page.name,
						"type": "Wiki Page",
						"title": wiki_page.title,
						"route": wiki_page.route,
						"group_name": sidebar_item.parent_label,
					}
				]
			else:
				sidebar[sidebar_item.parent_label] += [
					{
						"name": wiki_page.name,
						"type": "Wiki Page",
						"title": wiki_page.title,
						"route": wiki_page.route,
						"group_name": sidebar_item.parent_label,
					}
				]

		return self.get_items(sidebar)
