frappe.pages['erpenxt-chat-bot'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'ERPNEXT chat bot',
		single_column: true
	});
}